# Running the Server

There are several ways to start SajiloCloud. Pick whichever is easiest for you.

## Quick reference

| Method | What runs | Best for |
|--------|-----------|----------|
| `python server.py` | HTTP server (files + API) | Everyday use |
| `python websocket_server.py` | WebSocket server (collaboration) | Only needed for collab tools |
| `start_servers.bat` | Both, in separate windows | Windows one-click |
| `start_server.bat` | HTTP server only | Windows one-click |
| `Start App.bat` | Desktop control panel GUI | Windows GUI fans |
| `python server_control_panel.py` | Desktop control panel GUI | Anyone with a display |

---

## Ports

| Service | Port | Used by |
|---------|------|---------|
| HTTP server | **4142** (default) | Everything - the web app & files |
| WebSocket server | **4143** (fixed) | Real-time collaboration |

The HTTP port comes from `config.json -> port` (default `4142`). The WebSocket
port is hardcoded to `4143` in `websocket_server.py`.

---

## Option A - HTTP only (`python server.py`)

The core file manager needs only the HTTP server:

```bash
python server.py
```

Everything works except live multi-user canvas/scratchpad.

## Option B - Full stack (`python server.py` + `python websocket_server.py`)

For real-time collaboration, run **both** in two terminals:

```bash
# Terminal 1
python websocket_server.py

# Terminal 2
python server.py
```

Order doesn't matter much, but starting the WebSocket server first lets clients
connect instantly when the page loads.

## Option C - Windows: `start_servers.bat`

Double-click **`start_servers.bat`** from the project folder.

It opens **two** command windows:
1. "WebSocket Server" -> runs `websocket_server.py`
2. The HTTP server -> runs `server.py`

> Run this from the project folder (or double-click the file in Explorer).
> The script uses relative paths.

## Option D - Windows: `start_server.bat`

Double-click **`start_server.bat`** to run **only** the HTTP server. This script
`cd`s to its own directory automatically, so it works no matter where you put
the project.

## Option E - Windows: `Start App.bat` (Control Panel GUI)

Double-click **`Start App.bat`** to open the desktop control panel - a small GUI
window with Start / Stop buttons, status, and an "open in browser" shortcut.

```
Control Panel
+-------------------------------------------+
|  SajiloCloud                               |
|  Status: [running on 192.168.1.5:4142]     |
|  [ Start Servers ] [ Stop ]                |
|  [ Open in Browser ] [ QR Code ]           |
+-------------------------------------------+
```

See [Control Panel & Batch Files](CONTROL-PANEL.md) for every button.

---

## Verifying it's running

After starting, the terminal prints:

```
Scan to connect to the server:
[Q R code drawn with letters]
[21:00:00] Server started at http://192.168.1.5:4142
```

Check in your browser:

| URL | What you should see |
|-----|---------------------|
| `http://localhost:4142` | The SajiloCloud dashboard |
| `http://localhost:4142/api/sysinfo` | JSON with CPU/RAM/disk usage |
| `ws://localhost:4143` (via collab page) | Connected WebSocket session |

---

## Stopping the server

- In a terminal window: press **`Ctrl+C`**.
- From the control panel: press **Stop**.
- Closing the terminal window also kills it (that window *is* the server).

> No data is lost by stopping - files live on disk in `Home/`.

---

## Troubleshooting quick hits

- **"Address already in use"** - another program occupies the port. Change
 `port` in `config.json` (see [CONFIGURATION.md](CONFIGURATION.md)).
- **`ModuleNotFoundError`** - dependencies not installed:
 `pip install -r requirements.txt`.
- **Browser can't connect from another device** - check the [firewall rules](DEPLOYMENT.md#windows-firewall).
