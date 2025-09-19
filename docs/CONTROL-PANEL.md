# Control Panel & Batch Files

SajiloCloud ships with a small desktop GUI and three Windows launchers so you
never have to type a command.

---

## The Control Panel (`server_control_panel.py`)

A tiny Tkinter window that manages the server for you. Python's standard library
ships Tkinter with most Windows/macOS installs - no extra install needed.

### Launch

```bash
python server_control_panel.py
```

Or on Windows, double-click **`Start App.bat`**.

### What it shows

| Area | What it does |
|------|--------------|
| **Status line** | Server running? On what IP/port |
| ** Start** | Launches the HTTP server (and WebSocket server) as background processes |
| **# Stop** | Kills the running servers |
| **Open in Browser** | Opens `http://<local-ip>:<port>` |
| **Log panel** | Live console output from the servers |
| **QR code** | Shows the connect QR for phones |

### How it works

The panel spawns `server.py` / `websocket_server.py` as subprocesses and tails
their output into the log window. It keeps server state in a small JSON file so
it can detect a server that was started outside the panel.

---

## The batch files

All three live in the project root.

### `Start App.bat`

```bat
@echo off
start "" pythonw server_control_panel.py
exit
```

- Launches the **control panel GUI** in the background (no console window).
- Uses `pythonw` so no black terminal window appears.
- Run this from the project folder (or double-click it - same thing).

### `start_server.bat`

```bat
@echo off
cd /d "%~dp0"
python server.py
pause
```

- Runs the **HTTP server only** (files + API).
- `cd /d "%~dp0"` makes it work from **anywhere** - it changes into the folder
 the `.bat` lives in.
- `pause` keeps the window open so you can read errors.
- Press `Ctrl+C` or close the window to stop.

### `start_servers.bat`

```bat
@echo off
start "WebSocket Server" cmd /k "python websocket_server.py"
timeout /t 2 /nobreak > nul
python server.py
```

- Opens a **new window** running the WebSocket server (`cmd /k` keeps it open).
- Waits 2 seconds for it to boot.
- Then runs the HTTP server in the current window.
- Run this from the project root (it uses relative `python` calls).

### Which one should I use?

| You want... | Use |
|-----------|-----|
| Just file management, no collaboration | `start_server.bat` |
| Files + collaborative canvas/scratchpad | `start_servers.bat` |
| A clickable GUI with buttons | `Start App.bat` -> then press Start |
| To type commands yourself | `python server.py` in a terminal |

---

## Troubleshooting the launchers

| Problem | Fix |
|---------|-----|
| `'python' is not recognized` | Python not on PATH -> reinstall with "Add to PATH". |
| `ModuleNotFoundError` | `pip install -r requirements.txt` first. |
| Window flashes and closes | Likely a startup error -> run `python server.py` in a normal terminal to see it. |
| `pythonw` opens nothing | Check the control panel didn't fail silently -> run `python server_control_panel.py` in a terminal instead. |
| `start_servers.bat` "file not found" | Run it from the project root (it uses relative paths). |
