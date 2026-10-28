# BotOS Core

Discord 接続・プラグイン実行・ギルド同期の本体。

## 実行

リポジトリルートから:

```bash
make core
```

## 主要モジュール

| ファイル | 役割 |
|----------|------|
| `main.py` | 起動・組み込み `/botos_ping` |
| `plugin_manager.py` | `plugins/standard` の `.botos.json` 読み込み |
| `guild_sync.py` | ギルド単位スラッシュ同期（未配線） |
| `sandbox/runner.py` | ユーザーコード実行（未実装） |

## 拡張時の注意

- Core は API 経由で設定を受け取る想定（Redis/IPC は `docs/architecture.md`）
- プラグインから discord.py を直接触らせない（`docs/sandbox-spec.md`）
