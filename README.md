# BotOS

Webパネル上でモジュールを組み合わせ、自分専用のカスタムDiscord Botを構築できるノーコード/ローコードプラットフォーム。

従来のBotのように固定の機能を使うのではなく、必要なプラグインのみを選択・作成して導入する。MinecraftのModシステムに近い運用モデルを採用している。

## 主な機能

### Webパネル
- **プラグイン導入・管理**: ストアや自作プラグインから選択してサーバーへ導入可能
- **ビジュアルプログラミング (Blockly / Scratch形式)**: ノードやブロックを組み立ててノーコードでコマンドやイベント処理を作成
- **コード編集 (Python)**: 専用の安全なラッパーオブジェクトを用いたローコード開発に対応（MVPはPython/discord.pyを対象とし、他言語は将来検討）
- **サンドボックス実行**: 危険なシステムコールや不正アクセスを防止した隔離環境での動作
- **JSON形式での入出力**: 作成したプラグインはJSON形式でインポート・エクスポート可能
- **マーケットプレイス**: 作成したプラグインをパブリックに共有可能（初期MVPは完全無料）
- **公開範囲設定**: プライベート / パブリックの切り替え
- **ログ・デバッグ機能**: 実行エラーや動作ログをパネル上で確認可能

### Bot・同期システム
- **ギルドごとのコマンド同期**: 導入されたプラグインに応じて、サーバー単位でスラッシュコマンドを即時同期
- **コマンド数上限管理**: 1ギルドあたり標準30コマンドまで（申請により拡張可能）

## アーキテクチャ

```text
                     +---------------------------------------+
                     |             BotOS Web UI              |
                     |  - Blockly (ノーコード) / Monaco Editor |
                     |  - Plugin Store / Dashboard           |
                     +-------------------+-------------------+
                                         |
                                         | REST / WebSocket
                                         v
                     +---------------------------------------+
                     |           BotOS API Gateway           |
                     |  - FastAPI (OAuth2 / 認可 / プラグイン管理) |
                     +-------------------+-------------------+
                                         |
                                         | Redis Pub/Sub or IPC
                                         v
+---------------+    +---------------------------------------+
|    Discord    |<-->|              BotOS Core               |
+---------------+    |  - discord.py (Gateway 接続)          |
                     |  - Sandbox Runner (制限コンテキスト実行) |
                     |  - Dynamic Guild Sync (30コマンド制限)  |
                     +-------------------+-------------------+
                                         |
                          +--------------+--------------+
                          |              |              |
                          v              v              v
                     Plugin A       Plugin B       Plugin C
                     (Blockly)      (Python)       (Store)
```

## プラグイン形式 (`.botos.json`)

作成したプラグインは単一のJSON形式で保存・エクスポート・共有される。

```json
{
  "id": "custom.welcome-bot",
  "name": "Custom Welcome",
  "version": "1.0.0",
  "type": "blockly",
  "author_id": "00000000-0000-0000-0000-000000000000",
  "is_public": false,
  "entrypoint": {
    "engine": "blockly",
    "workspace": {},
    "generated_code": ""
  },
  "permissions": [
    "send_messages"
  ],
  "commands": [
    {
      "name": "hello",
      "description": "あいさつを返します"
    }
  ],
  "events": [
    "on_member_join"
  ],
  "config_schema": {}
}
```

## ディレクトリ構成

```text
BotOS/
├── core/       # Discord Bot本体、サンドボックス、ギルド同期エンジン
├── api/        # Webパネル向けバックエンドAPI (FastAPI)
├── web/        # ダッシュボード・エディタ（Next.js — 骨組みのみ）
├── plugins/    # 標準プラグイン
├── scripts/    # ローカル起動
├── docs/       # 仕様書・設計ドキュメント
├── CONTRIBUTING.md
└── Makefile    # make api / make core / make check
```

`core/` / `api/` / `plugins/` は骨組み実装済み。`web/` は [web/README.md](web/README.md) の手順で Next.js を追加する。

ローカル開発は [docs/DEV.md](docs/DEV.md) と [CONTRIBUTING.md](CONTRIBUTING.md) を参照。
