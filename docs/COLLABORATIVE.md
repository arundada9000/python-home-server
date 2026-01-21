# Collaborative Tools

Real-time, multi-user whiteboards and scratchpads — built into SajiloCloud.

> Requires the **WebSocket server** to be running (`python websocket_server.py`),
> or use `start_servers.bat` to launch both servers together.

---

## What you get

| Tool | What it is |
|------|------------|
| **Canvas** | A shared drawing whiteboard. Everyone sees strokes as they happen, each user in their own color. |
| **Scratchpad** | A shared markdown/text document. Everyone sees edits live, versioned. |

Both work across **any device on the same Wi-Fi** — a phone and a laptop can
collaborate in real time.

---

## Starting

```bash
# Terminal 1 — collaboration server
python websocket_server.py

# Terminal 2 — main server
python server.py
```

On Windows, just double-click **`start_servers.bat`**.

The WebSocket server listens on **`ws://<host>:4143`**.

---

## Using the Canvas

1. Open the file manager → open the **Collaborative** section (or navigate to the
   collaborative UI from the sidebar).
2. **Create a new canvas** — a session ID like `canvas_1700000000000` is created.
3. Share the session ID (or the page URL) with friends on the same network.
4. Draw. Strokes appear on everyone's screen instantly.
   - Your strokes are tinted your assigned color.
   - A name is shown with each session so you know who drew what.
5. **Clear** wipes the board for everyone.
6. **Snapshot** saves a PNG of the board (stored in `Home/.collaborative/canvases/`).

### Persistence

- Strokes are saved as JSON: `Home/.collaborative/canvases/<id>.json`
- A PNG snapshot is saved alongside when you export: `<id>.png`
- Sessions persist across server restarts and appear in the session list.

---

## Using the Scratchpad

1. Open **Scratchpads** in the collaborative section.
2. **Create a new scratchpad** — a session ID like `scratchpad_1700000000000`.
3. Start typing. Edits sync live to everyone in the room.
4. Content is saved as markdown: `Home/.collaborative/scratchpads/<id>.md`
   - Metadata (name, timestamps) in `<id>.meta.json`.

---

## How real-time sync works (short version)

```
Device A ──ws://host:4143──► WebSocket Server ──broadcast──► Device B
   drawing                       rooms[canvas_123]              sees it live
```

- Each session = a **room**. Clients in the same room get every event.
- The server keeps connected clients, user names, and colors in memory.
- On join, a client receives the room's current state (existing strokes/content).
- Changes are saved to disk so nothing is lost when the server restarts.

Full protocol details: [API.md → WebSocket API](API.md#websocket-api--wshost4143).

---

## Tips

- **Use names** — tell everyone to set a name so the color coding is meaningful.
- **Save before you leave** — sessions auto-persist, but the UI also has a
  manual save (via `POST /api/collaborative/save`).
- **Recycle vs. delete** — deleting a session removes its files from
  `Home/.collaborative/` permanently; use it carefully.
- **Hidden folder** — `.collaborative/` is hidden from the normal file browser
  (it's in `hidden_folders`), so session files stay tidy.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| "Cannot connect" / no live updates | WebSocket server not running → start `websocket_server.py` |
| Works locally, not on phone | Same Wi-Fi? Firewall allows port `4143`? |
| Port conflict on `4143` | Stop whatever uses it; the port is fixed in code for now |
| Lost after restart | Sessions should persist; check `Home/.collaborative/` exists |
