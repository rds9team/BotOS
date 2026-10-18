# BotOS

> Discord Botを、OSのように。

BotOSは、Discord Botをプラグイン方式で拡張できるプラットフォームです。

従来の「全部入りBot」ではなく、BotOS本体に必要な機能だけをPluginとして追加していくことを目指します。

MinecraftのMod / Pluginに近い感覚で、Discord Botの機能を追加・管理できます。

## Features

### Plugin System

BotOSの最大の特徴です。

```text
BotOS
├── Moderation
├── Ticket
├── Welcome
├── Minecraft
└── AI
```

必要なPluginだけをインストールして使用できます。

- Pluginのインストール
- 有効化 / 無効化
- アンインストール
- バージョン管理
- サーバーごとの設定
- Pluginごとの権限管理

### Web Dashboard

WebブラウザからBotOSを管理できます。

予定している機能:

- Discord OAuth2ログイン
- Discordサーバー選択
- Plugin Store
- Plugin管理
- Plugin設定
- サーバー設定

### Plugin API

PluginからBotOSの機能を利用できます。

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

EventやSlash CommandなどもPluginから利用できるようにします。

### Plugin Store

GitHubを利用したPlugin配布を予定しています。

Pluginには以下のような情報を持たせます。

```json
{
  "id": "example.moderation",
  "name": "Moderation",
  "version": "1.0.0",
  "author": "example",
  "description": "Moderation commands for Discord.",
  "main": "plugin.py",
  "botos_version": ">=1.0.0"
}
```

将来的には以下の機能を予定しています。

- Plugin検索
- カテゴリ
- ダウンロード数
- 評価
- Verifiedバッジ
- Plugin更新
- Marketplace

## Architecture

```text
                         +------------------+
                         |   BotOS Web UI   |
                         |                  |
                         | Plugin Store     |
                         | Server Settings  |
                         | Plugin Settings  |
                         +--------+---------+
                                  |
                                  | API
                                  |
                                  v
+---------------+         +------------------+
|    Discord    |<------->|   BotOS Core     |
+---------------+         |                  |
                          | Plugin Manager   |
                          | Event Manager    |
                          | Permission       |
                          | Config Manager   |
                          +--------+---------+
                                   |
                    +--------------+--------------+
                    |              |              |
                    v              v              v
               Plugin A       Plugin B       Plugin C
               Moderation     Ticket         Minecraft
```

BotOS CoreがDiscordとの通信やPluginのライフサイクルを管理し、各機能をPluginとして分離します。

## Plugin Lifecycle

Pluginは以下のライフサイクルで管理されます。

```text
Installed
    |
    v
Loaded
    |
    v
Enabled
    |
    v
Disabled
    |
    v
Unloaded
```

Plugin Managerがロード、有効化、無効化、アンロードを管理します。

## Configuration

Pluginの設定はDiscordサーバー単位で管理します。

例えば、

```text
Server A
├── Moderation
│   ├── enabled
│   └── log_channel
│
└── Welcome
    ├── enabled
    └── channel

Server B
└── Moderation
    ├── enabled
    └── log_channel
```

同じPluginでも、サーバーごとに異なる設定を使用できます。

## Permissions

Pluginは必要な権限をmanifestで宣言します。

例:

```json
{
  "permissions": [
    "discord.send_message",
    "discord.manage_channels"
  ]
}
```

Pluginのインストール時に要求される権限を確認できるようにします。

BotOSでは、Pluginが必要以上の権限を取得しないことを重要な設計方針とします。

## Security

PluginはBotOS上でコードを実行するため、セキュリティを重要な設計要件として扱います。

MVPでは以下を実装対象とします。

- OAuth2認証
- API認証 / 認可
- Discordサーバー権限確認
- Plugin権限の明示
- Plugin IDの検証
- バージョン検証
- API Rate Limit
- 秘密情報への不要なアクセス防止
- PluginからCoreへの直接アクセス制限

将来的にはPlugin Sandboxの導入も検討します。

```text
BotOS Core
    |
    +-- Sandbox Plugin A
    +-- Sandbox Plugin B
    +-- Sandbox Plugin C
```

## Initial Plugins

開発初期では、BotOSの仕組みを検証するため以下のPluginを作成します。

### Ping

```text
/ping
```

Pluginの基本的なロードとCommand登録を検証します。

### Welcome

ユーザー参加時にWelcomeメッセージを送信します。

設定例:

```text
enabled
channel
message
```

### Moderation

最低限の管理機能を提供します。

```text
/ban
/kick
/timeout
```

Plugin Permission Systemの検証にも使用します。

## MVP

BotOS MVPでは、以下の一連の流れを完成させることを目標とします。

```text
Discord OAuth2
      |
      v
Web Dashboard
      |
      v
Discord Server
      |
      v
Plugin Store
      |
      v
Plugin Install
      |
      v
Plugin Enable
      |
      v
Discord Command
      |
      v
Plugin executes
```

### MVP Checklist

- [ ] Discord Bot起動
- [ ] Discord OAuth2
- [ ] Web Dashboard
- [ ] Discordサーバー一覧
- [ ] Plugin Store
- [ ] Plugin Install
- [ ] Plugin Enable / Disable
- [ ] Plugin Uninstall
- [ ] Plugin Configuration
- [ ] Plugin API
- [ ] Event System
- [ ] Slash Command System
- [ ] Permission System
- [ ] GitHub Plugin Registry
- [ ] Plugin Version Management
- [ ] API Authentication / Authorization
- [ ] Ping Plugin
- [ ] Welcome Plugin
- [ ] Moderation Plugin

## Development

BotOSは現在開発中です。

開発環境のセットアップ方法や各コンポーネントの詳細については、プロジェクト内のドキュメントを参照してください。

予定している構成:

```text
BotOS
├── core/
│   ├── plugin/
│   ├── events/
│   ├── permissions/
│   └── config/
│
├── api/
│
├── web/
│
├── plugins/
│   ├── ping/
│   ├── welcome/
│   └── moderation/
│
└── docs/
```

実際のディレクトリ構成は実装に合わせて変更されます。

## Roadmap

### Phase 1 — Core

- [ ] BotOS Core
- [ ] Plugin Loader
- [ ] Plugin Lifecycle
- [ ] Event System
- [ ] Command System
- [ ] Configuration System

### Phase 2 — Dashboard

- [ ] Discord OAuth2
- [ ] Server Management
- [ ] Plugin Management
- [ ] Plugin Configuration

### Phase 3 — Plugin Ecosystem

- [ ] Plugin Manifest
- [ ] GitHub Registry
- [ ] Plugin Store
- [ ] Plugin Validation
- [ ] Verified Badge

### Phase 4 — Advanced

- [ ] Plugin Updates
- [ ] Dependency System
- [ ] CLI
- [ ] Analytics
- [ ] Marketplace
- [ ] Plugin Sandbox

## Contributing

BotOSはPlugin開発者、デザイナー、テスターなど、さまざまな分野からの参加を想定しています。

Pluginを作成する場合は、BotOS Plugin APIおよびPlugin Manifestの仕様に従ってください。

開発ルールやContribution Guideは今後整備します。

## License

Licenseについてはプロジェクトのライセンスファイルを参照してください。

## Vision

BotOSが目指しているのは、

> 「Discord Botをインストールする」のではなく、「BotOSに必要な機能を追加する」

という新しいBotの使い方です。

1つのBotにすべての機能を詰め込むのではなく、ユーザーが必要な機能だけを選択できる。

そして、開発者はPluginを作るだけでBotOSのエコシステムに参加できる。

Discord Botを、もっと自由に。
