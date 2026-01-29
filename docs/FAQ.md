# FAQ

## General

**What is SajiloCloud?**
A self-hosted file manager and real-time collaboration server you run on your own
computer. It's a "mini cloud" for your home/office network.

**Is it free?**
No. SajiloCloud is **proprietary**. Every use requires explicit written permission
from the copyright holder — see [LICENSE](../LICENSE) and [SECURITY.md](../SECURITY.md).

**Does it need the internet?**
No. It's fully local. The only internet dependency is the frontend loading a few
icons and the Monaco editor from CDNs — if you're fully offline, the UI may lose
those niceties, but the file server works.

---

## Networking

**Why does it only work on the same Wi-Fi?**
The server binds to `0.0.0.0` on the host machine and exposes plain HTTP on a LAN
port. Routers block inbound connections from the internet by default, so only
devices on the same network can reach it. That's the intended "trusted network"
design.

**Can I access it from outside my house?**
Not by default. You'd need a VPN or port forwarding — both documented, with heavy
warnings, in [DEPLOYMENT.md → Remote access](DEPLOYMENT.md#6-remote-access-port-forwarding--vpn).

**What's the difference between localhost, the IP, and the `.local` name?**

| Address | Works from | Notes |
|---------|-----------|-------|
| `http://localhost:4142` | the server machine only | always works |
| `http://192.168.x.x:4142` | any same-network device | always works |
| `http://arun.local` | any same-network device | only while server runs, needs `zeroconf` |

**What port does it use?** HTTP `4142` (default, configurable), WebSocket `4143` (fixed).

**What are all these `.local` domains?**
They come from the `aliases` list in `config.json` — see the full domain list in
[NETWORK.md](NETWORK.md#domains-registered-in-this-repos-config).

**How do I connect my phone?** Connect to the same Wi-Fi, then scan the QR code
(the terminal or `Home/qr.png`).

---

## Usage

**Where are my uploaded files stored?** In the `Home/` folder of the project
(plus `.recycle_bin/` for deleted items).

**Is delete reversible?** Normal delete → yes, it goes to the recycle bin
(restore from the Recycle Bin view). **Purge** → no, it's permanent.

**Can multiple people edit at once?** Yes — canvases and scratchpads sync live
over WebSockets (run `websocket_server.py` too).

**Can I edit code files?** Yes — click any code/text file and the Monaco editor
opens in the browser.

**Does it have user accounts?** No. It trusts the local network. The only secret
is the admin key, which reveals hidden folders. (User accounts are on the
roadmap.)

---

## Configuration

**Where is the config?** `config.json` in the project root. It's git-ignored and
auto-defaults if missing. Start from `config.json.example`.

**Do I need to restart after editing config?** Yes — config is read once at startup.

**Can I change the port?** Yes — `config.json` → `"port"`. The WebSocket port
(`4143`) is currently hardcoded.

**What's the admin key for?** Passing `?show_hidden=<admin_key>` to the file-list
API reveals hidden folders (recycle bin, app data, etc.).

---

## Troubleshooting

**The page won't load from my phone.** Same Wi-Fi? Correct address/IP? Firewall
allowed ports `4142`/`4143`? See [TROUBLESHOOTING.md](TROUBLESHOOTING.md#4-localhost4142-works-on-my-pc-but-other-devices-cant-connect).

**`ModuleNotFoundError`?** Run `pip install -r requirements.txt`.

**Port already in use?** Change `"port"` in config, or kill the conflicting process.

**Why is the QR code a pile of `#` in the terminal?** That *is* the QR code —
`qrcode.print_ascii()` renders it in text. Scan it or use `Home/qr.png`.

---

## Project & licensing

**Who made this?** [Arun Neupane](https://github.com/arundada9000), CTO & Lead
Architect at [Sajilo Digital Pvt. Ltd.](https://sajilodigital.com.np)

**Can I contribute?** Only with explicit written permission — see
[CONTRIBUTING.md](../CONTRIBUTING.md).

**Where's the roadmap?** See [CHANGELOG.md](../CHANGELOG.md) → "Backlog (planned)".
