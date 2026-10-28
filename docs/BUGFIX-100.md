# BotOS BUG-001 .. BUG-100

`tests/test_bugfixes_100.py` が BUG-001〜100 を 1:1 で回帰テストする。  
それ以前のセッションで入れた修正（tree sync、DB dispose 等）は別途 `tests/test_regressions.py`。

| ID | 概要 | 主な修正箇所 |
|----|------|----------------|
| BUG-001..020 | Discord snowflake 検証不足 | `core/botos_core/validation.py` |
| BUG-021..040 | plugin id パストラバーサル・形式 | `validation.py`, `api/botos_api/validation.py` |
| BUG-041..055 | スラッシュコマンド名規則 | `validation.py` |
| BUG-056..065 | semver 緩すぎ（`1.0.0.0` 等） | `validation.py` fullmatch + サフィックス規則 |
| BUG-066..075 | イベント名規則 | `validation.py` |
| BUG-076..085 | API guild/plugin/quota 検証 | `api/botos_api/validation.py` |
| BUG-086..095 | サンドボックス未検査の import/eval | `core/botos_core/sandbox/runner.py` |
| BUG-096 | `/api/guilds` ルート不一致 | `routes/guilds.py` `GET /` |
| BUG-097 | health に Cache-Control なし | `routes/health.py` |
| BUG-098 | セキュリティヘッダ欠落 | `api/botos_api/main.py` middleware |
| BUG-099 | 標準 ping プラグイン読込失敗 | `plugin_manager.py` + manifest 検証 |
| BUG-100 | コマンド数集計なし | `PluginManager.total_command_count()` |

## 追加で直した実装バグ（テスト番号外だが同梱）

- `.env` CWD 依存 → `repo_root()` 固定
- API 終了時 engine 未 dispose
- `guild_plugins` に UNIQUE(guild_id, plugin_id) なし
- `Plugin` / `GuildPlugin` の JSON 列欠落
- `command_quota_requests` モデル欠落
- `stats.guilds_managed` 固定 0 / DB 例外未処理
- `uvicorn --reload` 常時 ON → `BOTOS_RELOAD`
- JWT 短すぎ / `.` を plugin id 禁止していた API バリデーション
- テスト間 DB エンジン汚染 → `tests/conftest.py` + `:memory:`

## 検証

```bash
make test   # 105 passed（ regressions 5 + bugfixes 100 ）
```
