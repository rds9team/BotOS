# BotOS — プラグイン仕様書 (Unified Plugin Specification)

## 1. 概要
Webパネル上でブロックまたはPythonコードにより定義されたプラグインの構造、マニフェスト、および実行仕様。
本形式（`.botos.json` / `botos.plugin.json`）は、Web定義型（Blockly）および配布型（Pythonコード）の双方に対応する統一スキーマである。

## 2. プラグインデータ構造 (`.botos.json`)

```json
{
  "$schema": "https://botos.rds9.net/schemas/plugin.v1.json",
  "id": "com.example.custom-mod",
  "name": "Custom Moderation",
  "version": "1.0.0",
  "description": "モデレーションおよびメッセージ管理",
  "author_id": "00000000-0000-0000-0000-000000000000",
  "is_public": true,
  "type": "blockly",
  "entrypoint": {
    "engine": "blockly",
    "workspace": {
      "blocks": {}
    },
    "generated_code": ""
  },
  "permissions": [
    "kick_members"
  ],
  "commands": [
    {
      "name": "kick",
      "description": "メンバーをキックします",
      "options": [
        {
          "name": "target",
          "description": "対象ユーザー",
          "type": "user",
          "required": true
        },
        {
          "name": "reason",
          "description": "理由",
          "type": "string",
          "required": false
        }
      ]
    }
  ],
  "events": [
    "on_member_join"
  ],
  "config_schema": {
    "log_channel_id": {
      "type": "channel",
      "label": "ログチャンネル",
      "required": false
    }
  }
}
```

※ `$schema` のドメイン（`botos.rds9.net`）は将来の公式ホスティング予定URLです。開発・ローカル検証時はリポジトリ内スキーマ定義を正として扱います。

### Pythonプラグインの場合の entrypoint 例
`type` が `"python"` の場合、`entrypoint` は以下のように指定します:

```json
{
  "type": "python",
  "entrypoint": {
    "engine": "python",
    "file": "plugin.py",
    "class": "Plugin"
  }
}
```

## 3. サンドボックス & ラッパー仕様

### 3.1 制限事項
- 危険な標準モジュール（`os`, `sys`, `subprocess`, `socket`, `ctypes`, `threading`, `multiprocessing`, `importlib` など）の利用禁止。
- タイムアウト制限: 1コマンド/イベントあたり最大3.0秒。
- メモリ制限: プロセス隔離またはAST事前検証による制限（MVPフェーズ1: AST検証+軽量プロセス分離、フェーズ2: cgroups/コンテナによる64MB上限）。

### 3.2 ラッパーオブジェクト API (Python)
生の `discord.py` オブジェクトには直接アクセスさせず、BotOSが提供する安全なラッパーオブジェクト経由でのみ操作します。

```python
async def on_command_kick(ctx, target, reason="なし"):
    # ctx.author は制限されたラッパーオブジェクト
    if not ctx.author.guild_permissions.kick_members:
        await ctx.reply("権限がありません", ephemeral=True)
        return

    # target は制限された Member ラッパーオブジェクト
    await target.kick(reason=reason)
    await ctx.reply(f"{target.name} をキックしました: {reason}")
```

## 4. ギルドごとのコマンド同期

1. ギルド内で有効化されているプラグインのコマンド総数を算出（上限: 標準30件）。
2. 上限を超過した場合は登録処理を中断し、Webパネルへエラーを通知。
3. 有効なコマンドのみを対象ギルドのDiscord APIへ即時同期 (`POST /api/guilds/{guild_id}/sync` -> `bot.tree.sync(guild=...)`)。
