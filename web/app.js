/* BotOS dashboard wiring:
   - token intake: #token=... hash (OAuth web flow), localStorage fallback
   - API: /api/auth/me, /api/guilds, /api/guilds/{id}/plugins, install POST
   - mock mode: ?mock=1 renders fixture data without any backend
*/
(() => {
  "use strict";

  const TOKEN_KEY = "botos_token";
  const MOCK_MODE = new URLSearchParams(location.search).has("mock");
  const API_BASE = locateApiBase();
  const state = { user: null, guilds: [], pluginsByGuild: new Map(), busy: false };

  const el = (id) => document.getElementById(id);
  const show = (id, on = true) => { el(id).hidden = !on; };
  const setText = (id, text) => { el(id).textContent = text; };

  function locateApiBase() {
    if (location.search.includes("api=")) return new URLSearchParams(location.search).get("api").replace(/\/+$/, "");
    return "";
  }

  function api(path, options = {}) {
    const token = localStorage.getItem(TOKEN_KEY) || "";
    return fetch(`${API_BASE}${path}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...(options.headers || {}),
      },
    });
  }

  /* ---------- token intake ---------- */

  function intakeTokenFromHash() {
    const hash = location.hash.startsWith("#") ? location.hash.slice(1) : "";
    if (!hash) return;
    const params = new URLSearchParams(hash);
    const token = params.get("token");
    if (token) {
      localStorage.setItem(TOKEN_KEY, token);
      if (window.opener) {
        window.opener.postMessage({ type: "botos_auth", token }, "*");
      }
    }
    history.replaceState(null, "", location.pathname + location.search);
  }

  window.addEventListener("message", (event) => {
    if (event.origin !== location.origin) return;
    if (event.data && event.data.type === "botos_auth" && event.data.token) {
      localStorage.setItem(TOKEN_KEY, event.data.token);
      render().catch(console.error);
    }
  });

  /* ---------- login ---------- */

  async function startLogin() {
    const err = el("login-error");
    err.hidden = true;
    try {
      const res = await api("/api/auth/discord/login?kind=web");
      if (!res.ok) throw new Error(`login endpoint failed (${res.status})`);
      const payload = await res.json();
      window.location.href = payload.authorize_url;
    } catch (e) {
      err.textContent = `ログイン開始に失敗しました: ${e.message}`;
      err.hidden = false;
    }
  }

  /* ---------- dashboard logic ---------- */

  async function fetchMock() {
    const guilds = [
      { id: "111111111111111111", name: "開発用サーバー(モック)", icon: null },
      { id: "222222222222222222", name: "ゲームコミュニティ(モック)", icon: null },
      { id: "333333333333333333", name: "検証用サンドボックス(モック)", icon: null },
    ];
    state.user = { username: "mock-user" };
    state.guilds = guilds;
    state.pluginsByGuild.set(guilds[0].id, [
      { plugin_id: "botos.standard.ping", is_enabled: true, name: "Ping" },
    ]);
    state.pluginsByGuild.set(guilds[1].id, []);
    state.pluginsByGuild.set(guilds[2].id, []);
    return;
  }

  async function fetchRuntime() {
    if (!localStorage.getItem(TOKEN_KEY)) {
      return { needsLogin: true };
    }
    const me = await api("/api/auth/me");
    if (me.status === 401 || me.status === 403) {
      return { needsLogin: true };
    }
    if (!me.ok) throw new Error(`認証情報の取得に失敗しました (${me.status})`);
    state.user = await me.json();

    const res = await api("/api/guilds");
    if (!res.ok) throw new Error(`サーバー一覧の取得に失敗しました (${res.status})`);
    const payload = await res.json();
    state.guilds = Array.isArray(payload.guilds) ? payload.guilds : [];

    await Promise.all(state.guilds.map(async (g) => {
      state.pluginsByGuild.set(g.id, await fetchGuildPlugins(g.id, g.name));
    }));
    return {};
  }

  async function fetchGuildPlugins(guildId, guildName) {
    try {
      const res = await api(`/api/guilds/${encodeURIComponent(guildId)}/plugins`);
      if (!res.ok) return [];
      const payload = await res.json();
      return Array.isArray(payload.plugins) ? payload.plugins : [];
    } catch (e) {
      console.error("plugin list failed", guildId, e);
      return [];
    }
  }

  async function installDefaultPlugin(guild) {
    const res = await api(
      `/api/guilds/${encodeURIComponent(guild.id)}/plugins/botos.standard.ping`,
      { method: "POST", body: JSON.stringify({ guild_name: guild.name }) },
    );
    if (!res.ok) {
      const detail = await res.json().catch(() => ({}));
      throw new Error(detail.detail || `導入リクエストに失敗しました (${res.status})`);
    }
    state.pluginsByGuild.set(guild.id, await fetchGuildPlugins(guild.id, guild.name));
  }

  function renderTopbar() {
    const chip = el("user-chip");
    if (state.user && state.user.username) {
      chip.innerHTML = "";
      chip.append(Object.assign(document.createElement("span"), { textContent: "ログイン中: " }));
      chip.append(Object.assign(document.createElement("strong"), { textContent: state.user.username }));
      show("user-chip", true);
    } else {
      show("user-chip", false);
    }
  }

  function inviteUrlFor(guildId, authorizeUrl) {
    const authUrl = new URL(authorizeUrl);
    const clientId = authUrl.searchParams.get("client_id");
    if (!clientId) return null;
    const params = new URLSearchParams({
      client_id: clientId,
      scope: "bot applications.commands",
      permissions: "0",
      guild_id: guildId,
    });
    return `https://discord.com/oauth2/authorize?${params}`;
  }

  function renderCards() {
    const grid = el("guild-grid");
    grid.innerHTML = "";
    if (!state.guilds.length) {
      const empty = document.createElement("div");
      empty.className = "empty-state";
      empty.textContent = "管理権限のあるサーバーが見つかりませんでした。";
      grid.append(empty);
      return;
    }

    setText("guild-summary", `${state.guilds.length} サーバー` + (MOCK_MODE ? "(モックデータ)" : ""));

    for (const guild of state.guilds) {
      const plugins = state.pluginsByGuild.get(guild.id) || [];
      const installed = plugins.length > 0;
      const card = document.createElement("article");
      card.className = "card";

      const top = document.createElement("div");
      top.className = "card-top";
      const icon = renderIcon(guild);
      const names = document.createElement("div");
      names.append(
        Object.assign(document.createElement("div"), { className: "guild-name", textContent: guild.name || "(名称未設定)" }),
        Object.assign(document.createElement("div"), { className: "guild-id", textContent: guild.id }),
      );
      top.append(icon, names);

      const body = document.createElement("div");
      body.className = "card-body";
      body.append(
        Object.assign(document.createElement("div"), {
          textContent: installed ? "Bot 導入済み" : "Bot 未導入",
          className: installed ? "state-ok" : "state-none",
        }),
        Object.assign(document.createElement("div"), {
          textContent: installed ? `プラグイン ${plugins.length} 件 有効` : "まず Bot を追加してください",
        }),
      );

      const actions = document.createElement("div");
      actions.className = "card-actions";

      if (installed) {
        const manage = Object.assign(document.createElement("button"), {
          className: "btn btn-primary btn-small",
          textContent: "管理する",
        });
        manage.addEventListener("click", () => openPluginDialog(guild, plugins));
        actions.append(manage);

        const addPlugin = Object.assign(document.createElement("button"), {
          className: "btn btn-ghost btn-small",
          textContent: "プラグイン追加",
        });
        addPlugin.disabled = state.busy;
        addPlugin.addEventListener("click", async () => {
          try {
            setBusy(true, addPlugin);
            await installDefaultPlugin(guild);
            await render();
          } catch (e) {
            showDashError(e.message);
          } finally {
            setBusy(false, addPlugin);
          }
        });
        actions.append(addPlugin);
      } else {
        const install = Object.assign(document.createElement("button"), {
          className: "btn btn-primary btn-small",
          textContent: "導入する",
        });
        install.disabled = state.busy;
        install.addEventListener("click", async () => {
          try {
            setBusy(true, install);
            await installDefaultPlugin(guild);
            window.open(inviteUrlFor(guild.id, await cachedAuthorizeUrl()), "_blank", "noopener");
            await render();
          } catch (e) {
            showDashError(e.message);
          } finally {
            setBusy(false, install);
          }
        });
        actions.append(install);
      }

      card.append(top, body, actions);
      grid.append(card);
    }
  }

  const memoizedAuthorizeUrl = { value: null };
  async function cachedAuthorizeUrl() {
    if (memoizedAuthorizeUrl.value) return memoizedAuthorizeUrl.value;
    try {
      const res = await api("/api/auth/discord/login");
      const payload = await res.json();
      memoizedAuthorizeUrl.value = payload.authorize_url || "";
    } catch (e) {
      memoizedAuthorizeUrl.value = "";
    }
    return memoizedAuthorizeUrl.value;
  }

  function renderIcon(guild) {
    if (guild.icon) {
      const image = document.createElement("img");
      image.className = "guild-icon";
      image.alt = "";
      image.src = `https://cdn.discordapp.com/icons/${guild.id}/${guild.icon}.png?size=64`;
      image.addEventListener("error", () => image.replaceWith(makeFallbackIcon(guild)));
      return image;
    }
    return makeFallbackIcon(guild);
  }

  function makeFallbackIcon(guild) {
    const span = document.createElement("div");
    span.className = "guild-icon";
    span.textContent = (guild.name || "?").slice(0, 1);
    return span;
  }

  function openPluginDialog(guild, plugins) {
    el("plugin-dialog-title").textContent = `${guild.name} のプラグイン`;
    const list = el("plugin-list");
    list.innerHTML = "";
    if (!plugins.length) {
      list.append(Object.assign(document.createElement("li"), { textContent: "インストール済みのプラグインはありません。" }));
    }
    for (const p of plugins) {
      const item = document.createElement("li");
      item.append(
        Object.assign(document.createElement("span"), { textContent: p.name || p.plugin_id }),
        Object.assign(document.createElement("span"), {
          className: "p-state",
          textContent: p.is_enabled ? "有効" : "無効",
        }),
      );
      list.append(item);
    }
    el("plugin-dialog").showModal();
  }

  function setBusy(on, button) {
    state.busy = on;
    for (const node of document.querySelectorAll(".card-actions button")) node.disabled = on;
    if (button) button.disabled = on;
  }

  function showDashError(message) {
    const err = el("dash-error");
    err.textContent = message;
    err.hidden = false;
  }

  async function render() {
    show("loading", true);
    show("auth-gate", false);
    show("dash", false);
    el("dash-error").hidden = true;
    try {
      if (MOCK_MODE) {
        await fetchMock();
        renderTopbar();
        show("dash", true);
        renderCards();
      } else {
        const { needsLogin } = await fetchRuntime();
        if (needsLogin) {
          show("auth-gate", true);
        } else {
          renderTopbar();
          show("dash", true);
          renderCards();
        }
      }
    } catch (e) {
      showDashError(e.message);
      show("auth-gate", !localStorage.getItem(TOKEN_KEY));
      show("dash", !!localStorage.getItem(TOKEN_KEY));
    } finally {
      show("loading", false);
    }
  }

  function bindEvents() {
    el("login-btn").addEventListener("click", startLogin);
    el("reload-btn").addEventListener("click", () => render().catch(console.error));
  }

  intakeTokenFromHash();
  bindEvents();
  setText("api-base", MOCK_MODE ? "mock mode" : (API_BASE || location.origin));
  show("mock-badge", MOCK_MODE);
  render().catch(console.error);
})();
