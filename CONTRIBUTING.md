# BotOS — 開発の進め方

rds9team の [OPERATIONS](https://github.com/rds9team/.github-private/blob/main/docs/OPERATIONS.md) に沿った最小フローです。

## 1. 始める前に

1. GitHub Issue を作成する（何を・なぜ・完了条件）
2. `dev` または `feature/短い説明` ブランチで作業する
3. 変更は Pull Request で `dev` 向けに出す（`main` への直接 push はしない）

## 2. 初回セットアップ

```bash
cp .env.example .env
# .env に DISCORD_BOT_TOKEN 等を入れる（トークンはコミットしない）

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

## 3. よく使うコマンド

```bash
make help          # 一覧
make api           # FastAPI（:8000）
make core          # Discord Core（要 DISCORD_BOT_TOKEN）
make check         # 静的チェック（ruff）
```

詳細は [docs/DEV.md](docs/DEV.md) を参照。

## 4. どこに何を書くか

| やりたいこと | 置き場所 |
|-------------|----------|
| スラッシュコマンド・イベント・サンドボックス | `core/botos_core/` |
| REST / OAuth / DB | `api/botos_api/` |
| ダッシュボード UI | `web/`（未実装の場合は README の手順） |
| 同梱プラグイン例 | `plugins/standard/` |
| 仕様の変更 | `docs/` + Issue で合意 |

## 5. レビュー前チェック

- [ ] `make check` が通る
- [ ] 秘密情報が diff に含まれていない
- [ ] PR 説明に「動作確認したこと / していないこと」を書いた

AI が生成したコードも、**マージ前に人間が diff を読む**（チーム AGENTS 方針）。
