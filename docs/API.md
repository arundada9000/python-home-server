# API Reference

Complete reference for SajiloCloud's HTTP (REST) and WebSocket APIs.

- Base URL: `http://<host>:<port>` (HTTP)
- WebSocket URL: `ws://<host>:4143` (fixed port)

> **Auth note:** Most endpoints require no auth — SajiloCloud trusts its local
> network. The only secret is the **admin key**, used to reveal hidden folders
> via `?show_hidden=<admin_key>`. Treat this API as LAN-only.

---

## REST API

### `GET /api/list` — List directory contents

Query: `path` (relative to `Home/`), `show_hidden` (optional admin key)

```http
GET /api/list?path=docs&show_hidden=pooju
```

```json
{
  "path": "docs",
  "items": [
    { "name": "README.md", "is_dir": false, "size": 5120 },
    { "name": "images",    "is_dir": true,  "size": 0 }
  ]
}
```

Folders sort first, then alphabetically. Hidden folders are excluded unless
`show_hidden` matches the configured `admin_key`.

---

### `GET /api/search?q=...` — Global search

```http
GET /api/search?q=report
```

```json
[
  { "name": "report.docx", "path": "docs", "is_dir": false }
]
```

Case-insensitive substring search across all files/folders under `Home/`
(hidden folders excluded).

---

### `GET /api/sysinfo` — System stats

```http
GET /api/sysinfo
```

```json
{
  "disk": { "total": 500000000000, "used": 120000000000, "free": 380000000000, "percent": 24.0 },
  "cpu": 12.5,
  "ram": 63.2,
  "os": "Windows",
  "time": "2026-08-14 21:00:00"
}
```

Requires `psutil`.

---

### `GET /api/all_folders` — All folders (for move/zip dialogs)

```http
GET /api/all_folders
```

```json
["", "docs", "docs/images", "videos"]
```

Recursive walk of `Home/`, hidden folders pruned, relative paths with `/`.

---

### `GET /api/recycle_bin` — List deleted items

```http
GET /api/recycle_bin
```

```json
[
  { "name": "20260109_153747_devops.mp4", "is_dir": false, "size": 409600, "mtime": 1763000000.0 }
]
```

Sorted by deletion time, newest first.

---

### `GET /api/activity` — Recent activity

```http
GET /api/activity
```

```json
[
  { "timestamp": "2026-08-14 20:59:00", "action": "Upload", "filename": "2 files to docs", "ip": "192.168.1.3", "user": "Admin" }
]
```

Last 50 logged actions from `data/activity_log.json`.

---

### `GET /api/comments?path=docs/readme.md` — Get file comments

```http
GET /api/comments?path=notes.md
```

```json
[
  { "text": "update this later", "author": "Admin", "timestamp": "2026-08-14 19:00:00" }
]
```

---

### `GET /api/portal_data` — Portal page data

Returns the contents of `Home/useful-info/PortalData.json`, or `{"links":[]}`
if it doesn't exist.

---

### `GET /api/collaborative/sessions` — List collab sessions

```http
GET /api/collaborative/sessions
```

```json
{
  "canvases":     [ { "id": "...", "last_modified": "...", "stroke_count": 12, "has_image": false } ],
  "scratchpads":  [ { "id": "...", "last_modified": "...", "content_length": 240, "metadata": {} } ]
}
```

---

### `POST /api/upload?path=docs` — Upload files

Multipart/form-data, field name `file` (repeatable for multiple files).

```bash
curl -F "file=@report.docx" "http://192.168.1.5:4142/api/upload?path=docs"
```

Duplicate filenames get a timestamp suffix (`name_20260814_210000.ext`).

Response:
```json
{ "status": "ok", "saved": ["report.docx"] }
```

---

### `POST /api/mkdir` — Create a folder

```json
{ "path": "docs", "folder": "new-folder" }
```

Returns `200` (error if it already exists).

---

### `POST /api/delete` — Soft delete (to recycle bin)

```json
{ "path": "docs", "name": "old.txt" }
```

Moves the item to `Home/.recycle_bin/` with a `YYYYMMDD_HHMMSS_` prefix.

---

### `POST /api/restore` — Restore from recycle bin

```json
{ "name": "20260814_210000_old.txt" }
```

Restores to `Home/`, stripping the timestamp prefix.

---

### `POST /api/purge` — Permanent delete

```json
{ "name": "20260814_210000_old.txt" }
```

Removes the item forever. **Not recoverable.**

---

### `POST /api/rename` — Rename or move

```json
{ "path": "docs", "old_name": "old.txt", "new_name": "new.txt" }
```

To move into another folder, `new_name` may contain `/` (target dirs are created).

---

### `POST /api/save_json` — Save a JSON file from the editor

```json
{ "filename": "docs/data.json", "content": { "a": 1 }, "raw": false }
```

`raw: true` writes the content string verbatim; otherwise it's pretty-printed JSON.

---

### `POST /api/batch_delete` — Batch soft delete

```json
{ "items": [ { "path": "docs", "name": "a.txt" }, { "path": "", "name": "b.png" } ] }
```

---

### `POST /api/zip` — Zip selected items

```json
{ "items": [ { "path": "docs", "name": "report.docx" } ], "filename": "backup.zip" }
```

Streams an application/zip attachment.

---

### `POST /api/comments` — Add a comment

```json
{ "path": "notes.md", "text": "reviewed", "author": "Admin" }
```

---

### `POST /api/collaborative/save` — Save a session manually

Canvas:
```json
{ "type": "canvas", "id": "canvas_1700000000000", "data": { "strokes": [] } }
```

Scratchpad:
```json
{ "type": "scratchpad", "id": "scratchpad_1700000000000", "content": "# Hi", "metadata": {} }
```

---

## Static file serving

Any path that isn't `/api/` is served from disk:

1. Project root — `index.html`, `app.js`, `styles.css`, `images/`, `modules/`
2. `Home/` upload root — user files

Supports **HTTP Range requests** (`206 Partial Content`) for video/audio seeking.

---

## WebSocket API — `ws://<host>:4143`

Real-time collaboration protocol. The client opens a socket, identifies itself,
and joins a named room.

### Connection message

```json
{ "type": "join", "room": "canvas_1700000000000", "user": { "name": "Arun" } }
```

The server responds with user info (including an assigned `color`) and the room's
current state (existing strokes / content).

### Event messages (server → all in room)

```json
{ "type": "stroke", "room": "...", "user": { "name": "Arun", "color": "#4ade80" }, "stroke": { ... } }
{ "type": "clear", "room": "...", "user": { "name": "Arun" } }
{ "type": "content", "room": "...", "user": { "name": "Arun" }, "content": "...", "version": 3 }
```

Every message is broadcast to everyone in the room — that's the "live" part.

### Persistence

Sessions are saved to `Home/.collaborative/`:
- `canvases/<id>.json` (+ optional `<id>.png` snapshot)
- `scratchpads/<id>.md` + `<id>.meta.json`

Users are visually identified by per-connection colors from a fixed palette.

---

## Error handling

- `404` — unknown API route or missing file
- `500` — server/scan error (message included in the body)
- `400` — bad request (missing params, invalid JSON)

Responses are `application/json` unless otherwise noted.
