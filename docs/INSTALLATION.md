# Installation Guide

Detailed, platform-by-platform installation for SajiloCloud.

## Prerequisites

| Requirement | Minimum | Notes |
|-------------|---------|-------|
| Python | 3.7 | 3.10+ recommended |
| OS | Windows 10/11, macOS, or Linux | Any OS with Python works |
| Network | Wi-Fi or Ethernet LAN | Devices must share the network |
| `pip` | included with Python | Verify with `pip --version` |

> SajiloCloud is **proprietary software** — by installing and running it you
> acknowledge the [LICENSE](../LICENSE) terms and that use requires written
> permission from the copyright holder.

---

## 1. Install Python

### Windows
1. Download from https://www.python.org/downloads/
2. Run the installer and **tick "Add Python to PATH"**.
3. Verify:
   ```cmd
   python --version
   ```

### macOS
```bash
brew install python3
# or
python3 --version
```

### Linux (Debian/Ubuntu)
```bash
sudo apt update && sudo apt install -y python3 python3-pip
python3 --version
```

---

## 2. Get the code

```bash
git clone https://github.com/arundada9000/sajilocloud.git
cd sajilocloud
```

Or download & extract the ZIP from GitHub.

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

This installs:

| Package | Why it's needed |
|---------|-----------------|
| `qrcode[pil]` | Generates the QR code + saves it to `Home/qr.png` |
| `psutil` | CPU / RAM / disk monitoring on the dashboard |
| `websockets` | Real-time collaborative canvas/scratchpad server |
| `zeroconf` | Registers friendly `.local` domains (mDNS) |

> **Optional packages** — if `zeroconf` is missing, the server still runs; it
> simply won't register `.local` names. Everything else is required.

---

## 4. Create your config (recommended)

The server runs with sane defaults even with **no** `config.json`. But to set
your own port, admin key, and domain aliases:

```bash
cp config.json.example config.json
```

Then edit `config.json` — see the [Configuration reference](CONFIGURATION.md).

> ⚠️ `config.json` contains a **secret admin key** and is git-ignored. Never
> commit it.

---

## 5. Verify the installation

```bash
python server.py
```

Expected output:

```
Scan to connect to the server:
[Q R code drawn with letters]
[21:00:00] Server started at http://192.168.1.5:4142
```

Open `http://localhost:4142`. If the page loads, **installation succeeded**.
Press `Ctrl+C` in the terminal to stop.

---

## Next steps

- ▶️ **Run it properly** → [Running the Server](RUNNING.md)
- 📱 **Connect your phone** → [Networking & Domains](NETWORK.md)
- ⚙️ **Tune the config** → [Configuration](CONFIGURATION.md)
