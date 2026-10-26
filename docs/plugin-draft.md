# BotOS — プラグイン仕様ドラフト

## 1. 概要
Webパネル上でブロックまたはコードにより定義されたプラグインの構造、および実行仕様。

## 2. プラグインデータ構造 (`.botos.json`)

```json
{
  "$schema": "https://botos.rds9.net/schemas/plugin.v1.json",
  "id": "com.example.custom-mod",
  "name": "Custom Moderation",
  "version": "1.0.0",
  "description": "モデレーションおよびメッセージ管理",
  "author_id": "123456789012345678",
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

## 3. サンドボックス & ラッパー仕様

### 3.1 制限事項
- 危険な標準モジュール（`os`, `sys`, `subprocess`, `socket` など）の利用禁止。
- タイムアウト制限: 1コマンド/イベントあたり最大3秒。
- メモリ制限: プロセス隔離またはAST検証による制限。

### 3.2 ラッパーオブジェクト API (Python)
```python
async def on_command_kick(ctx, target, reason="なし"):
    if not ctx.author.guild_permissions.kick_members:
        await ctx.reply("権限がありません", ephemeral=True)
        return

    await target.kick(reason=reason)
    await ctx.reply(f"{target.name} をキックしました: {reason}")
```

## 4. ギルドごとのコマンド同期

1. ギルド内で有効化されているプラグインのコマンド総数を算出（上限: 30）。
2. 上限を超過した場合は登録処理を中断し、Webパネルへエラーを通知。
3. 有効なコマンドのみを対象ギルドのDiscord APIへ即時同期 (`guild_commands` 更新)。
