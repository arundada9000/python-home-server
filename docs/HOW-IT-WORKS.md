# How It Works

An end-to-end tour of SajiloCloud's architecture, from terminal to browser tab.

---

## System overview

SajiloCloud is made of **two Python servers** plus a **vanilla-JS frontend**:

```
┌────────────────────────────────────────────────────────────┐
│                       YOUR COMPUTER                        │
│                                                            │
│  ┌─────────────────────┐      ┌──────────────────────────┐ │
│  │  HTTP Server        │      │  WebSocket Server        │ │
│  │  server.py :4142    │      │  websocket_server.py     │ │
│  │                     │      │            :4143         │ │
│  │  • static files     │      │  • collab rooms          │ │
│  │  • REST API         │      │  • broadcast events      │ │
│  │  • file operations  │      │  • session persistence   │ │
│  └─────────┬───────────┘      └──────────┬───────────────┘ │
│            │                            │                 │
│            ▼                            ▼                 │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Shared data                                        │   │
│  │  Home/          → user files                        │   │
│  │  data/          → activity log, comments            │   │
│  │  Home/.recycle_bin/  → soft-deleted items           │   │
│  │  Home/.collaborative/ → canvases & scratchpads      │   │
│  └────────────────────────────────────────────────────┘   │
│                                                            │
│  mDNS: dns_service.py registers http://<alias>.local       │
└────────────────────────────────────────────────────────────┘
```

---

## Startup sequence

When you run `python server.py`:

1. `load_config()` reads `config.json` (or falls back to defaults).
2. Constants are derived — `UPLOAD_ROOT` (`Home/`), `QR_FILE`, `RECYCLE_BIN`.
3. Missing folders are auto-created:
   - `Home/` (upload root)
   - `Home/.recycle_bin/` (recycle bin)
   - `Home/.collaborative/canvases` & `scratchpads` (via `CollaborativeManager`)
4. A **QR code** is generated and saved to `Home/qr.png`.
5. If `zeroconf` is installed and `aliases` exist, each alias is registered as
   `http://<alias>.local`.
6. The threaded HTTP server starts listening on `0.0.0.0:<port>`.

No database, no migrations, no external services. If it can create folders, it runs.

---

## Request flow — a page load

```
Browser  ──GET /────────────────────────────────────────────►  server.py
                                                              │
                                                              ▼
                                          rel_path = "index.html"
                                    serve_static_file(index.html) ── 200 OK
Browser ◄────────────────────────── html + css + js ──────────┘
```

Static files are looked up in this order:
1. Project root (e.g. `/app.js`, `/styles.css`)
2. `Home/` upload root (e.g. `/some-uploaded-file.png`)

---

## Request flow — the file browser

```
Browser ──GET /api/list?path=docs&show_hidden=<key>──►  server.py
                                                        │
                                                        ▼
                                              api_handlers.handle_list()
                                              • safe_join prevents path escapes
                                              • scandir reads entries
                                              • hidden folders filtered (unless
                                                show_hidden matches admin_key)
                                                        │
                        JSON {path, items:[...]}        │
Browser ◄───────────────────────────────────────────────┘
```

The key security detail: **every** path is passed through `safe_join()`, which
normalizes the path and rejects anything that escapes `UPLOAD_ROOT` — so
`../..` tricks can't read files outside `Home/`.

---

## File operations map

| UI action | REST call | What happens on disk |
|-----------|-----------|----------------------|
| Upload | `POST /api/upload` | Writes to `Home/<path>`; duplicate names get a timestamp suffix |
| Delete | `POST /api/delete` | `shutil.move` → `Home/.recycle_bin/` (soft delete) |
| Batch delete | `POST /api/batch_delete` | Same, for many items |
| Restore | `POST /api/restore` | Moves back, stripping the timestamp prefix |
| Purge | `POST /api/purge` | **Permanently** removes from recycle bin |
| Rename/Move | `POST /api/rename` | `os.rename` (+ creates target dir) |
| Zip | `POST /api/zip` | Streams a ZIP directly to the browser |
| Save JSON | `POST /api/save_json` | Writes the editor's content to `Home/` |

Every mutation logs to `data/activity_log.json` via `audit_logger`.

---

## Real-time collaboration flow

```
Phone & Laptop on same Wi-Fi
      │                                  ┌─────────────────────────────┐
      │  HTTP /collaborative/*           │  WebSocket :4143            │
      ├─────────────────────────────────►│  websocket_server.py        │
      │  ws://<host>:4143                │                             │
      ├─────────────────────────────────►│  • rooms: set of sockets    │
      │                                  │  • on message → broadcast   │
      │  stroke / text edits             │    to everyone in the room  │
      ├─────────────────────────────────►│                             │
      │                                  │  • periodic/on-demand save  │
      │                                  │    → Home/.collaborative/   │
      └──────────────────────────────────┴─────────────────────────────┘
```

- Every connected user gets a color so strokes are identifiable.
- Sessions persist as JSON in `Home/.collaborative/`.
- The WebSocket server re-uses `CollaborativeManager` for storage.

See [COLLABORATIVE.md](COLLABORATIVE.md) for usage and [API.md](API.md) for messages.

---

## Data layout

| Path | Purpose | Git status |
|------|---------|------------|
| `config.json` | Settings + secret | ignored |
| `Home/` | Uploaded user files | ignored (except app pages) |
| `Home/.recycle_bin/` | Soft-deleted files | ignored |
| `Home/.collaborative/` | Canvas/scratchpad sessions | ignored |
| `Home/qr.png` | Generated QR | ignored |
| `data/activity_log.json` | Last 100 audit entries | ignored |
| `data/comments.json` | File comments | ignored |

Everything the server needs to *run* is re-creatable; everything *user-created*
is git-ignored. That's why a fresh clone boots cleanly.

---

## Technology notes

- **Zero heavy frameworks** — `http.server` + `ThreadingMixIn` gives concurrency
  without Flask/Django.
- **Vanilla JS frontend** — no build step; open the source and edit.
- **JSON persistence** — simple, human-readable, no DB to install.
- **Optional mDNS** — degrades gracefully: no `zeroconf` → no `.local` names,
  everything else still works.
