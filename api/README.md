# BotOS API

FastAPI バックエンド。Web パネルと Core の間に立つ層（`docs/architecture.md`）。

## 実行

```bash
make api
```

## ルート

| メソッド | パス | 状態 |
|----------|------|------|
| GET | `/health`, `/api/health` | 実装済 |
| GET | `/api/stats` | 骨組み |
| GET | `/api/guilds` | スタブ |
| POST | `/api/guilds/{id}/plugins/{id}` | 501 |

## 次に実装するファイル

1. `botos_api/auth/discord.py` — OAuth2
2. `botos_api/routes/guilds.py` — DB 連携
3. Core への sync イベント（Redis 等）
