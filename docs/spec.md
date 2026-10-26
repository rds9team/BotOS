# BotOS — MVP Specification

## 1. 概要

BotOSは、Discord Botを「プラグイン方式」で拡張できるプラットフォーム。

一般的なDiscord Botのように、機能ごとに別Botを作るのではなく、1つのBotOS本体に複数のプラグインをインストールすることで、必要な機能だけを追加できるようにする。

### コンセプト

> Discord Botを「完成品」ではなく「OS + アプリ」のように扱う。

MinecraftのMod / Pluginシステムに近いUXを目指す。

---

# 2. MVPで実現すること

最低限、以下を一通り動作させる。

- BotOS Discord Bot
- Web管理画面
- ユーザー認証
- Discordサーバー選択
- プラグイン一覧
- プラグインインストール
- プラグイン有効化 / 無効化
- プラグイン設定
- プラグインのアンインストール
- プラグイン実行
- プラグインAPI
- サーバーごとのプラグイン状態管理
- 基本的な権限管理
- プラグイン開発用の仕様
- GitHubを利用したプラグイン公開

---

# 3. 全体構成

```text
                    ┌──────────────────┐
                    │   BotOS Web UI   │
                    │                  │
                    │ Plugin Store     │
                    │ Server Settings  │
                    │ Plugin Settings  │
                    └────────┬─────────┘
                             │ API
                             ▼
┌───────────────┐     ┌──────────────────┐
│    Discord    │◀───▶│   BotOS Core     │
└───────────────┘     │                  │
                      │ Plugin Manager   │
                      │ Permission       │
                      │ Config Manager   │
                      │ Event Manager    │
                      └────────┬─────────┘
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
           Plugin A        Plugin B        Plugin C
           Moderation      Ticket          Minecraft
```

---

# 4. BotOS Core

BotOS Coreはプラグインを管理・実行する本体。

## 4.1 Plugin Manager

以下を担当する。

- プラグイン検出
- プラグイン読み込み
- プラグイン有効化
- プラグイン無効化
- プラグインアンロード
- プラグインバージョン管理
- 依存関係確認
- プラグイン設定読み込み

### ライフサイクル

```text
Installed
   ↓
Loaded
   ↓
Enabled
   ↓
Disabled
   ↓
Unloaded
```

---

# 5. プラグイン仕様

プラグインはBotOS専用のmanifestを持つ。

例:

```json
{
  "id": "example.moderation",
  "name": "Moderation",
  "version": "1.0.0",
  "author": "example",
  "description": "Moderation commands for Discord.",
  "main": "plugin.py",
  "botos_version": ">=1.0.0",
  "permissions": [
    "discord.moderation"
  ]
}
```

## 必須項目

- `id`
- `name`
- `version`
- `author`
- `description`
- `main`
- `botos_version`

## 推奨項目

- `homepage`
- `repository`
- `license`
- `dependencies`
- `permissions`
- `config_schema`

---

# 6. Plugin API

プラグインからBotOS Coreの機能を利用できるようにする。

例:

```python
class Plugin:

    async def on_load(self):
        pass

    async def on_enable(self):
        pass

    async def on_disable(self):
        pass

    async def on_unload(self):
        pass
```

Discord関連API:

```python
bot.command(...)
bot.event(...)
bot.get_guild(...)
bot.send_message(...)
```

ただし、プラグインからBotOS内部を直接自由に操作させず、可能な限りBotOS API経由でアクセスする。

---

# 7. Event System

BotOS Coreからプラグインへイベントを送信する。

例:

```text
guild_join
guild_remove
message_create
member_join
member_leave
interaction
command
plugin_enable
plugin_disable
```

プラグイン側:

```python
@event("member_join")
async def on_member_join(member):
    ...
```

---

# 8. Discord Command System

プラグインごとにSlash Commandを登録できる。

例:

```text
/moderation ban
/moderation kick
/ticket create
/ticket close
/minecraft stats
```

BotOS Coreがコマンド登録を管理する。

---

# 9. Plugin Configuration

プラグインごとに設定を持てる。

例:

```json
{
  "enabled": true,
  "log_channel": "123456789",
  "prefix": "!",
  "auto_mod": true
}
```

設定は**Discordサーバー単位**で管理する。

```text
Server A
 ├─ Moderation
 │   ├─ enabled
 │   └─ log_channel
 │
 └─ Ticket
     ├─ enabled
     └─ category

Server B
 └─ Moderation
     └─ enabled
```

---

# 10. Web Dashboard

Web UIからBotOSを管理する。

## Dashboard

表示する情報:

- ユーザー情報
- 管理可能なDiscordサーバー
- インストール済みプラグイン
- BotOSの状態

---

## Server Page

```text
Server Name

Installed Plugins

[Moderation]     ON
[Ticket]         ON
[Welcome]        OFF

[Plugin Store]
```

---

## Plugin Page

```text
Moderation

Version: 1.0.0
Author: example

Description:
Discord moderation plugin.

[Install]
```

インストール後:

```text
[Enabled]
[Disable]
[Uninstall]

Settings
```

---

# 11. Authentication

Discord OAuth2を使用する。

```text
User
 ↓
Discord OAuth2
 ↓
BotOS
 ↓
User Account
```

ユーザーが管理権限を持っているDiscordサーバーだけを管理対象として表示する。

Botが参加していないサーバーについては、必要に応じてBot招待導線を表示する。

---

# 12. Permission System

MVPでは最低限の権限管理を実装する。

## ユーザー権限

```text
Owner
Admin
User
```

## Plugin Permission

例:

```text
discord.send_message
discord.manage_channels
discord.manage_roles
discord.moderation
```

プラグインはmanifestで必要権限を宣言する。

ユーザーには、

```text
このプラグインは以下の権限を要求しています。

✓ メッセージ送信
✓ チャンネル管理
✗ ロール管理

[Install]
```

のように表示する。

---

# 13. Plugin Repository

MVPではGitHubをプラグイン配布元として利用する。

```text
GitHub Repository
        ↓
plugin.json
        ↓
BotOS Plugin Registry
        ↓
Web Store
```

プラグイン作者がGitHub上に公開する。

BotOS側ではRegistryに登録されたプラグインを表示する。

---

# 14. Plugin Store

ストアでは以下を表示する。

- Plugin Name
- Icon
- Description
- Author
- Version
- Downloads
- Rating
- GitHub Repository
- Required Permissions
- BotOS Version

カテゴリ例:

```text
Moderation
Utility
Entertainment
Music
Minecraft
Administration
AI
Other
```

---

# 15. Plugin Approval

将来的にプラグインへ認証ステータスを付与する。

基準例:

- 動作確認済み
- 悪意のあるコードがない
- manifestが正しい
- 権限要求が妥当
- 一定期間の動作実績

MVPでは審査システムそのものを作り込まず、DB上にステータスを持てればよい。

```text
pending
approved
rejected
verified
```

---

# 16. Database

最低限以下のデータを管理する。

## Users

```text
id
discord_id
username
created_at
```

## Servers

```text
id
discord_guild_id
name
owner_id
created_at
```

## Plugins

```text
id
name
version
author
repository
description
status
created_at
```

## InstalledPlugins

```text
id
server_id
plugin_id
version
enabled
installed_at
```

## PluginConfigs

```text
id
server_id
plugin_id
config
updated_at
```

---

# 17. API

Web UIとBotOS Core間のAPIを用意する。

例:

```text
GET    /api/servers
GET    /api/servers/:id/plugins

GET    /api/plugins
GET    /api/plugins/:id

POST   /api/servers/:id/plugins/:plugin/install
POST   /api/servers/:id/plugins/:plugin/enable
POST   /api/servers/:id/plugins/:plugin/disable
DELETE /api/servers/:id/plugins/:plugin

GET    /api/servers/:id/plugins/:plugin/config
PUT    /api/servers/:id/plugins/:plugin/config
```

認証済みユーザー以外はアクセスできないようにする。

---

# 18. Security

BotOSではプラグインが任意コードを実行できるため、ここは重要。

MVPでは最低限、

- Plugin IDの検証
- バージョン検証
- GitHub Repositoryの検証
- HTTPS
- OAuth2認証
- API認可
- Server IDの所有権確認
- 秘密情報をPluginから直接取得させない
- ログインユーザーの権限確認
- API Rate Limit
- Plugin権限の明示

を実装する。

## 特に重要

プラグインは基本的に**信頼できないコードとして扱う**。

理想的には将来的に、

```text
BotOS Core
   │
   ├── Sandbox Plugin A
   ├── Sandbox Plugin B
   └── Sandbox Plugin C
```

のような隔離環境を検討する。

MVPでは完全なSandbox実装を必須にしないが、Plugin APIを設計する段階から「Coreへの直接アクセスを避ける」構造にする。

---

# 19. MVP Plugin

最初から複雑なPluginを大量に作らない。

動作確認用として最低3つ程度作る。

### Plugin 1 — Ping

```text
/ping
```

BotOS Plugin Systemの基本動作確認用。

### Plugin 2 — Welcome

ユーザー参加時にWelcomeメッセージを送信。

設定:

```text
enabled
channel
message
```

### Plugin 3 — Moderation

最低限:

```text
/ban
/kick
/timeout
```

権限システムとPlugin APIの確認用。

---

# 20. Developer Experience

プラグイン開発者が簡単に作れることを重視する。

理想:

```bash
botos create my-plugin
```

↓

```text
my-plugin/
├── plugin.json
├── plugin.py
├── README.md
└── config.json
```

開発者はplugin.pyを編集してGitHubへ公開するだけ。

将来的にCLIを提供する。

---

# 21. CLI

MVP後に実装。

例:

```bash
botos login
botos create my-plugin
botos dev
botos validate
botos publish
```

`validate`では、

- manifest
- version
- required fields
- dependencies
- BotOS compatibility

などをチェックする。

---

# 22. 将来機能

MVPでは実装しなくてよい。

### Plugin Marketplace

- 有料Plugin
- 作者への収益還元
- ダウンロード数
- レビュー
- ランキング

### Plugin Update

```text
1.0.0 → 1.1.0
```

をWeb UIから更新。

### Dependency System

```text
Plugin A
 └─ requires Plugin B >= 1.2
```

### Automatic Update

Plugin更新を自動適用。

### Plugin Sandbox

Pluginをコンテナ等で隔離。

### Per-server Display Name

BotOS上のアカウント名とは別に、Discordサーバーごとに表示名を設定。

### Plugin Analytics

作者向けに、

- インストール数
- アクティブサーバー
- エラー数
- バージョン分布

などを表示。

---

# 23. MVP完成条件

以下が全部動けばBotOS MVP完成とする。

- [ ] Discord Botが起動する
- [ ] Discord OAuth2ログインができる
- [ ] 管理可能なDiscordサーバーを取得できる
- [ ] Web Dashboardが表示される
- [ ] Plugin Storeが表示される
- [ ] Pluginをインストールできる
- [ ] Pluginを有効化できる
- [ ] Pluginを無効化できる
- [ ] Pluginをアンインストールできる
- [ ] Pluginの設定を変更できる
- [ ] Slash CommandをPluginから登録できる
- [ ] EventをPluginから受け取れる
- [ ] Pluginごとの権限を管理できる
- [ ] GitHub由来Pluginを読み込める
- [ ] Pluginのバージョンを管理できる
- [ ] 基本的なAPI認証・認可が動作する
- [ ] Ping / Welcome / Moderation Pluginが動作する

---

# 24. 開発方針

まず「全部の機能を完璧に作る」のではなく、

```text
Discord
   ↓
BotOS Core
   ↓
Plugin
   ↓
Web Dashboard
   ↓
Plugin Store
```

という**一連の流れを最初から最後まで通す**。

最初の目標は、

> 「WebからPluginをインストールしたら、Discord上でそのPluginの機能が使える」

ところまで。

その後、

- セキュリティ強化
- Plugin API拡張
- UI改善
- Registry
- 審査
- CLI
- Marketplace

を段階的に追加する。
