# BotOS — データベーススキーマ仕様書

## 1. テーブル一覧

### 1.1 users
Webパネルにログインしたユーザー。
- `id` (UUID, PK)
- `discord_id` (VARCHAR(32), UNIQUE, INDEX): DiscordユーザーID
- `username` (VARCHAR(100)): ユーザー名
- `avatar_url` (TEXT): アイコンURL
- `created_at` (TIMESTAMP)

### 1.2 guilds
BotOSが導入されているDiscordサーバー。
- `id` (VARCHAR(32), PK): Discord Guild ID
- `name` (VARCHAR(100)): サーバー名
- `icon_url` (TEXT)
- `max_commands` (INT, DEFAULT 30): 登録可能コマンド数上限（初期値30）
- `created_at` (TIMESTAMP)

### 1.3 plugins
作成・公開されたプラグイン。
- `id` (VARCHAR(64), PK): プラグインID (例: `com.user.mod`)
- `name` (VARCHAR(100)): プラグイン名
- `description` (TEXT): 説明文
- `author_id` (UUID, FK -> users.id): 作成者
- `type` (VARCHAR(20)): `blockly` | `python` | `nodejs`
- `is_public` (BOOLEAN, DEFAULT FALSE): 公開フラグ
- `manifest` (JSON): コマンド定義、権限、設定スキーマ
- `content` (JSON): Blocklyワークスペースデータまたはコード本文
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

### 1.4 guild_plugins
各サーバーにインストール・有効化されているプラグイン。
- `id` (UUID, PK)
- `guild_id` (VARCHAR(32), FK -> guilds.id)
- `plugin_id` (VARCHAR(64), FK -> plugins.id)
- `is_enabled` (BOOLEAN, DEFAULT TRUE)
- `config` (JSON): サーバーごとの個別設定値
- `installed_at` (TIMESTAMP)

### 1.5 command_quota_requests
1ギルド30コマンドの上限拡張申請。
- `id` (UUID, PK)
- `guild_id` (VARCHAR(32), FK -> guilds.id)
- `requested_by` (UUID, FK -> users.id)
- `requested_quota` (INT): 希望上限数
- `reason` (TEXT): 申請理由
- `status` (VARCHAR(20)): `pending` | `approved` | `rejected`
- `created_at` (TIMESTAMP)
