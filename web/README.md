# BotOS Web（管理 UI）

**現状:** `package.json` のみ。Next.js プロジェクトは未生成。

## 人間が UI を始めるとき

1. Issue で UI スコープを決める
2. チームの UI 規約（hallmark 等）を確認
3. リポジトリルートで `.env` の `NEXT_PUBLIC_API_URL` を合わせる
4. このディレクトリで Next.js を初期化する（例）:

```bash
cd web
npx create-next-app@latest . --typescript --tailwind --app --no-src-dir
```

5. Blockly / Monaco は `docs/blockly-spec.md` に従って別 PR で追加

API のベース URL は `http://localhost:8000`（開発時）。
