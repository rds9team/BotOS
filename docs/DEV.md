# BotOS — ローカル開発

## リポジトリ構成

```text
BotOS/
├── core/botos_core/     Discord 本体・プラグイン実行（discord.py）
├── api/botos_api/       Web 向け API（FastAPI）
├── web/                 管理 UI（Next.js・骨組みのみ）
├── plugins/standard/    同梱プラグイン例
├── docs/                仕様
└── scripts/             起動用ショートカット
```

## 環境変数

`.env.example` を `.env` にコピーして編集する。

| 変数 | 用途 |
|------|------|
| `DISCORD_BOT_TOKEN` | Core 起動に必須 |
| `DATABASE_URL` | API の DB（デフォルト SQLite） |
| `JWT_SECRET` | API セッション（本番は必ず差し替え） |
| `NEXT_PUBLIC_API_URL` | Web から API への URL |

## API 単体

```bash
source .venv/bin/activate
make api
```

- http://localhost:8000/health
- http://localhost:8000/api/health
- http://localhost:8000/docs （OpenAPI）

## Core 単体

Bot を Discord に接続する。トークン未設定の場合は即終了し、メッセージを表示する。

```bash
make core
```

## 拡張の入口（実装順の目安）

1. `api/botos_api/routes/guilds.py` — ギルド・プラグイン CRUD
2. `core/botos_core/guild_sync.py` — `bot.tree.sync(guild=...)`
3. `core/botos_core/sandbox/runner.py` — ユーザーコード実行
4. `core/botos_core/plugin_manager.py` — `.botos.json` の読み込み

仕様の正本は `docs/architecture.md` と `docs/plugin-draft.md`（統合作業中の項目は Issue 参照）。
