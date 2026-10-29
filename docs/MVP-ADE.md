## OAuth (A)

1. `GET /api/auth/discord/login` → `{authorize_url}`
2. Browser → Discord → callback `GET /api/auth/discord/callback?code=&state=`
3. Response JSON: `{access_token, token_type, guilds, user}`
4. API calls: `Authorization: Bearer <jwt>`

## Install plugin + sync (E)

```http
POST /api/guilds/{guild_id}/plugins/botos.standard.ping
Authorization: Bearer <jwt>
Content-Type: application/json

{"guild_name": "My Server"}
```

Core worker reads `guild_sync_requests` and syncs guild commands from DB.

## Ping plugin (D)

`plugins/standard/ping/ping.botos.json` includes `generated_code` with `on_command_ping`.
