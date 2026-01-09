# 🐣 Dummy-Proof Quickstart

> This guide assumes you have **never** used a terminal, never installed Python,
> and have no idea what "port" means. If you follow it exactly, you'll have your
> own file server running in about 10 minutes.

---

## What are we building?

A **mini cloud that runs on your own computer**. You open a web page, and anyone
on your **same Wi-Fi** can upload, download, and edit files through that page.
No internet company involved. Your computer is the server.

---

## Step 1 — Install Python

1. Go to https://www.python.org/downloads/
2. Click the big yellow **"Download Python 3.x"** button.
3. Run the downloaded file.
4. **IMPORTANT:** Check the box that says **"Add Python to PATH"** at the bottom.
5. Click **Install Now** and wait.
6. Done. You now have Python.

To check it worked, search for "cmd" in the Start menu and open **Command Prompt**.
Type:

```cmd
python --version
```

You should see something like `Python 3.12.x`. If you see an error, the "Add to PATH"
box was probably unticked — reinstall Python and tick it.

---

## Step 2 — Get the code

You need a copy of this project on your computer.

### If you have the ZIP file (simplest)
1. Unzip the folder anywhere, e.g. `C:\Users\YourName\sajilocloud`.
2. Remember the path.

### If you know Git
```cmd
git clone https://github.com/arundada9000/sajilocloud.git
cd sajilocloud
```

---

## Step 3 — Install the dependencies (one-time)

These are extra pieces of code the server needs. Open **Command Prompt** and type:

```cmd
cd C:\Users\YourName\sajilocloud
pip install -r requirements.txt
```

Replace the path with wherever you put the project. Wait until it finishes — you
should see `Successfully installed ...`.

> This is the only time you need to install dependencies (unless you reinstall Python).

---

## Step 4 — Start the server

Still in Command Prompt, type:

```cmd
python server.py
```

You'll see something like:

```
Scan to connect to the server:
[Q R code drawn with letters]
[21:00:00] Server started at http://192.168.1.5:4142
```

**DO NOT close this window.** That window *is* the server. Closing it stops
everything.

---

## Step 5 — Open it

### On the same computer
Open Chrome/Edge/Firefox and go to:

```
http://localhost:4142
```

### On your phone (same Wi-Fi!)
1. Make sure your phone is connected to the **same Wi-Fi** as the computer.
2. Open the camera app and point it at the **QR code** drawn in the terminal.
   (It's also saved as `Home/qr.png` in the project folder.)
3. Tap the link that appears.
4. You're in! 🎉

---

## Step 6 — What can you do?

- **Upload:** drag files from your phone/laptop into the page.
- **Download:** click any file.
- **Edit:** click a `.js`/`.py`/`.html`/`.txt`/`.json` file — a code editor opens.
- **Search:** press `/` on the keyboard.
- **Share with friends:** give them the IP URL or scan the QR — if they're on the
  same Wi-Fi, they're in.

---

## Everyday routine (after the first time)

1. Open Command Prompt.
2. `cd` to the project folder.
3. `python server.py`

That's it. (Windows users: double-click **`start_servers.bat`** to skip all typing —
see [RUNNING.md](RUNNING.md).)

---

## If something goes wrong

| Problem | Fix |
|---------|-----|
| `'python' is not recognized` | Python not on PATH → reinstall with "Add to PATH" ticked. |
| `ModuleNotFoundError` | You skipped Step 3 → run `pip install -r requirements.txt`. |
| "Can't reach this page" | Server window is closed → start it again (Step 4). |
| Phone can't connect | Phone must be on the **same Wi-Fi** as the computer. |
| Port already in use | Another program uses port 4142 → change `port` in `config.json` (see [CONFIGURATION.md](CONFIGURATION.md)). |

More fixes: **[Troubleshooting](TROUBLESHOOTING.md)** and **[FAQ](FAQ.md)**.

---

*Still stuck? That's what the [FAQ](FAQ.md) is for — or email the maintainer at
[arunneupane0000@gmail.com](mailto:arunneupane0000@gmail.com).*
