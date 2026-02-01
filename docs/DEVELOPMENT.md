# Developer Guide

For anyone granted permission to work on the SajiloCloud codebase.

> **First, read [CONTRIBUTING.md](../CONTRIBUTING.md).** SajiloCloud is
> proprietary — you need explicit written permission from the maintainer before
> modifying or contributing.

---

## Repository layout

```
server.py                  # Entry point — HTTP server, routing, static files
websocket_server.py        # Entry point — real-time collaboration server
api_handlers.py            # REST API handlers (one function per endpoint)
collaborative_manager.py   # Canvas/scratchpad persistence (JSON on disk)
dns_service.py             # mDNS (.local) registration via zeroconf
audit_logger.py            # Writes data/activity_log.json (last 100 entries)
temp_handler.py            # Portal data helper (used by api_handlers)
server_control_panel.py    # Desktop GUI (Tkinter) that spawns the servers
repro_mdns.py              # Standalone mDNS repro/debug script
app.js                     # Frontend logic (vanilla ES6+)
index.html                 # SPA shell
styles.css                 # All styling (glassmorphism, dark/light)
modules/collaborative/     # Canvas + scratchpad frontend modules
images/icons/              # Favicons & site icons
Home/                      # Runtime user data (git-ignored)
data/                      # Runtime logs (git-ignored)
docs/                      # Documentation
```

---

## Core concepts

### 1. No frameworks — small, explicit handlers

`server.py` subclasses `SimpleHTTPRequestHandler`. Routing is a chain of
`if / elif` on the path:

```python
if path == "/api/list":
    api_handlers.handle_list(self, parsed, UPLOAD_ROOT, ADMIN_KEY, HIDDEN_FOLDERS, safe_join)
```

Every handler in `api_handlers.py` is a standalone function — easy to read, easy
to test.

### 2. Path safety is non-negotiable

All user-supplied paths go through `safe_join()` (server.py):

```python
def safe_join(base, *paths):
    final_path = os.path.normpath(os.path.join(base, *paths))
    if not final_path.startswith(base):        # (Windows uses .lower())
        raise ValueError(...)
```

**Never** write a handler that builds a filesystem path from user input without
going through `safe_join`. This is the main defense against path-traversal.

### 3. Everything important is git-ignored

`config.json`, `Home/**`, `data/*` are runtime data. The repo must always boot
from a fresh clone with defaults. If you add new runtime artifacts, ignore them.

### 4. Shared manager for persistence

`CollaborativeManager` owns `Home/.collaborative/` — both servers use the same
class, so HTTP saves and WebSocket sessions stay consistent.

---

## Environment setup

```bash
git clone https://github.com/arundada9000/sajilocloud.git
cd sajilocloud
pip install -r requirements.txt
```

---

## Running during development

```bash
# HTTP server (auto-reload by restarting)
python server.py

# WebSocket server (for collaborative features)
python websocket_server.py
```

There's no auto-reloader — restart the process after Python changes. For frontend
changes, just refresh the browser (no build step).

---

## Testing

There is **no test framework** currently. Before you submit anything, at minimum:

1. **Boot test** — both servers start with no errors:
   ```bash
   python server.py
   python websocket_server.py
   ```
2. **Sanity test** — from a fresh clone, delete `config.json` and confirm the
   server still starts (defaults).
3. **Path test** — hit `/api/list?path=../../etc` and confirm a `500`/`404`,
   never a file leak.
4. **Smoke test** — upload → rename → delete → restore → purge through the UI.

A CI workflow runs a syntax check on every push — see
[`.github/workflows/ci.yml`](../.github/workflows/ci.yml).

---

## Code style

- **Python:** 4-space indent, stdlib-first, `black`-adjacent formatting.
- **JavaScript:** 2-space indent, vanilla ES6+, template literals.
- **HTML/CSS:** follow `styles.css` conventions (CSS variables, classes).
- **Comments:** only when they explain *why*.
- **Error handling:** handlers catch `Exception`, log via `print`, and return a
  meaningful status — follow that pattern.

---

## Adding an API endpoint (checklist)

1. Add a handler function in `api_handlers.py` (e.g. `handle_my_thing`).
2. Route it in `server.py` — add `elif` branches in `do_GET` and/or `do_POST`.
3. Pass only what it needs (`UPLOAD_ROOT`, `safe_join`, managers).
4. Use `safe_join` for any path input.
5. Document it in [API.md](API.md).
6. Boot-test both servers, then run the sanity tests above.

---

## Adding a collaborative feature

1. Persistence: add a method to `CollaborativeManager`.
2. WebSocket: extend `websocket_server.py` message handling (rooms/broadcast).
3. Frontend: extend `modules/collaborative/`.
4. Optional HTTP save endpoint: `handle_collaborative_save` pattern in `api_handlers.py`.
5. Document in [COLLABORATIVE.md](COLLABORATIVE.md).

---

## Dependency policy

Keep the dependency list minimal (see `requirements.txt` / `pyproject.toml`):

| Package | Where used | Required? |
|---------|-----------|-----------|
| `qrcode[pil]` | QR generation | yes |
| `psutil` | system stats | yes |
| `websockets` | collaboration server | yes (that feature) |
| `zeroconf` | `.local` domains | no (degrades gracefully) |

Prefer the Python standard library for everything else.

---

## Commit & PR flow

1. Branch from `main`: `git checkout -b feat/your-feature`
2. Commit with [conventional prefixes](../CONTRIBUTING.md#commit-convention).
3. Open a PR using the [template](../.github/PULL_REQUEST_TEMPLATE.md).

> ⚠️ Remember: this project is **proprietary**. Only contribute what the
> maintainer has explicitly approved.
