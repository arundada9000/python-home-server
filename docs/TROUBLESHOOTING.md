# Troubleshooting

A fix-it list for the problems people actually hit. Start here before opening an
issue.

---

## 1. `'python' is not recognized as an internal or external command`

Python isn't on your PATH.

**Fix:** Reinstall Python and tick **"Add Python to PATH"**. Restart the terminal.
Verify with `python --version`.

---

## 2. `ModuleNotFoundError: No module named 'qrcode'` (or `psutil` / `websockets` / `zeroconf`)

Dependencies not installed.

**Fix:**
```bash
pip install -r requirements.txt
```

> `zeroconf` is optional - without it the server still runs, it just won't
> register `.local` domains.

---

## 3. `[Errno 98] Address already in use` / `OSError: [WinError 10048]`

Another program is using the port (default `4142`, WebSocket `4143`).

**Fix options:**
1. Change the HTTP port in `config.json` -> `"port": 8080` (see [CONFIGURATION.md](CONFIGURATION.md)).
2. Find and stop the conflicting program:
 - Windows: `netstat -ano | findstr :4142` -> note PID -> `taskkill /PID <pid> /F`
 - Linux: `sudo lsof -i :4142`

The WebSocket port (`4143`) is currently fixed in `websocket_server.py`.

---

## 4. `localhost:4142` works on my PC, but other devices can't connect

Almost always a **firewall** issue (or wrong network).

1. Confirm the other device is on the **same Wi-Fi / LAN**.
2. Confirm you're using the right address: `http://<server-local-ip>:4142` (the
 IP printed at startup), or scan the QR.
3. Allow ports `4142` and `4143` through the firewall:
 - [Windows](DEPLOYMENT.md#windows-firewall)
 - [Linux/macOS](DEPLOYMENT.md#2-firewall-rules)
4. Try `ping <server-ip>` from the other device. If it fails -> network isolation
 (guest Wi-Fi, client isolation) or firewall.

---

## 5. The QR code doesn't open anything

1. The camera needs to recognize it - zoom out a bit, better lighting.
2. The QR encodes the server's **local IP**. If you're not on the same network
 (e.g. mobile data), it won't work.
3. Or just type the URL manually: `http://<ip>:<port>`.
4. `Home/qr.png` is regenerated each start - refresh if it's stale.

---

## 6. `.local` domains (like `http://arun.local`) don't resolve

- The server must be running (mDNS only registers while it runs).
- You need the optional `zeroconf` package:
 ```bash
 pip install zeroconf
 ```
- mDNS doesn't cross networks - server and client must share the LAN.
- Some Android browsers take a few seconds; retry, or use the IP.

---

## 7. File upload fails or says "413"/connection reset

- Very large files: HTTP uploads are streamed, but a slow network or browser
 timeout can kill big uploads. Try smaller files or a wired connection.
- Disk full? `api/sysinfo` shows disk usage.

---

## 8. Video won't play / seeking is broken

SajiloCloud supports HTTP Range requests (`206`), which most players need.
If a player misbehaves, try downloading the file instead, or a different browser.

---

## 9. Hidden folders visible / not visible when they should be

Hidden folders show only when the list URL includes the correct admin key:

```
GET /api/list?path=...&show_hidden=<admin_key>
```

- Wrong key -> hidden folders stay hidden.
- `admin_key` is read from `config.json` at **startup** - change it and restart.

---

## 10. Server starts but page is blank / broken UI

1. Hard-refresh (`Ctrl+Shift+R`) to bust the browser cache.
2. Check the browser console (`F12`) for CDN errors - Lucide, Monaco, Marked,
 and Highlight.js load from CDNs and need internet.
3. Confirm you opened the right port.

---

## 11. The control panel (`Start App.bat`) does nothing

Run it in a terminal to see the error:

```bash
python server_control_panel.py
```

If you see a Tkinter error, your Python install lacks `tkinter` (rare on
Windows) - use `python server.py` directly instead.

---

## 12. I deleted something by accident

- Normal delete = **soft delete** -> it's in `Home/.recycle_bin/` and restorable
 from the **Recycle Bin** view in the UI.
- **Purge** is permanent. No undo. That's by design.

---

## 13. Still stuck?

Gather this info before asking for help:

1. OS + Python version (`python --version`)
2. What you ran (exact command or which `.bat`)
3. The full error/terminal output
4. Whether `localhost` works and whether other devices can connect

Then open a [bug report](../.github/ISSUE_TEMPLATE/bug_report.md) or contact the
maintainer.
