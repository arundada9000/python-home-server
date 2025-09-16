# Configuration

SajiloCloud reads a single JSON file: **`config.json`** (in the project root).

- If the file is **missing**, safe defaults are used - the server runs with zero setup.
- If the file is **invalid JSON**, defaults are used and the error is swallowed.
- `config.json` is **git-ignored** (it contains a secret key). Use
 [`config.json.example`](../config.json.example) as a safe template.

---

## Full reference

```json
{
 "admin_key": "your-secret-key",
 "port": 4142,
 "upload_root": "Home",
 "hidden_folders": [
 "images",
 ".recycle_bin",
 "server-icons",
 "useful-info",
 ".collaborative",
 "commands"
 ],
 "aliases": [
 "sajilo", "server", "arun", "arundada9000"
 ]
}
```

---

## `admin_key` - string

The secret key that unlocks **hidden folders**.

- Passed as `?show_hidden=<admin_key>` to the list API.
- Any unknown value -> hidden folders stay hidden.
- **Never** commit this to git. Change it from the default!

```json
"admin_key": "pooju"
```

> This is effectively the server's master password for hidden content.
> Pick something long and random.

---

## `port` - number

The HTTP server port (the WebSocket port is fixed at `4143`).

| Value | Result |
|-------|--------|
| `4142` (default) | Normal, no admin rights needed |
| `80` | `http://sajilo.local` with no `:port` - requires admin/root on most OSes |
| `8080` / `3000` / anything free | Fine |

```json
"port": 4142
```

> Ports below `1024` (like `80`) usually need administrator privileges on
> Windows/macOS and `sudo` on Linux.

---

## `upload_root` - string

The folder where uploaded files are stored and served from.

```json
"upload_root": "Home"
```

- Relative paths are resolved against the project root.
- The folder is auto-created if missing.
- The default `Home/` is correct for most setups - **you usually don't touch this.**

---

## `hidden_folders` - array of strings

Folders that are **hidden from the file browser** unless the viewer knows the
admin key. They still exist on disk and are still served if accessed directly.

```json
"hidden_folders": [
 "images",
 ".recycle_bin",
 "server-icons",
 "useful-info",
 ".collaborative",
 "commands"
]
```

| Entry | Why it's hidden |
|-------|-----------------|
| `images` | Site assets - not user files |
| `.recycle_bin` | Deleted items (restore/purge lives here) |
| `server-icons` | UI icon set |
| `useful-info` | App data (`PortalData.json`) |
| `.collaborative` | Canvas/scratchpad session storage |
| `commands` | Command-reference data |

---

## `aliases` - array of strings

mDNS hostname aliases. Each becomes `http://<alias>.local` on your network.

```json
"aliases": ["sajilo", "server", "arun", "arundada9000"]
```

- Requires the optional `zeroconf` package; if missing, `.local` names just don't register.
- Aliases only resolve **while the server runs** and **on the same network**.
- See [NETWORK.md](NETWORK.md) for the full domain list and behavior.

---

## Example: low-privilege setup (port 80)

```json
{
 "admin_key": "A-very-long-unguessable-key-9f2c",
 "port": 80,
 "upload_root": "Home",
 "hidden_folders": [".recycle_bin", "server-icons", "useful-info", ".collaborative"],
 "aliases": ["sajilo", "server"]
}
```

## Example: quick test setup

```json
{
 "admin_key": "test",
 "port": 4142,
 "upload_root": "Home",
 "hidden_folders": [],
 "aliases": []
}
```

---

## Creating your own config

```bash
cp config.json.example config.json
```

Then edit with any text editor. **Restart the server** after changes - config is
read once at startup.

## Gotchas

- Invalid JSON -> defaults, silently.
- `admin_key` empty string still hides folders (any non-empty match required).
- The WebSocket port (`4143`) is **not** configurable yet - hardcoded in
 `websocket_server.py`.
