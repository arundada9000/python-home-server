# Networking & Domains

How SajiloCloud serves your files, why it works only on the **same network**,
and what all those `.local` domains mean.

---

## The big idea: it's a LAN server

SajiloCloud is **local-first**. It binds to `0.0.0.0` on the computer that runs
it, meaning it is reachable from **any device on the same network** — but not
from the internet (by default).

```
        YOUR HOME / OFFICE WI-FI
   ┌───────────────────────────────────────┐
   │                                       │
   │   ┌───────────┐   ┌───────────────┐   │
   │   │  PC        │   │  Phone        │   │
   │   │  (server)  │◄──┤  Laptop       │   │
   │   │ :4142      │   │  Tablet       │   │
   │   └───────────┘   └───────────────┘   │
   │                                       │
   │   Internet ── outside = NOT reachable │
   └───────────────────────────────────────┘
```

**Same network means:**
- Connected to the same Wi-Fi network, **or**
- Connected via Ethernet to the same router/LAN.

**Not reachable means:** someone on mobile data, or a friend on a different
network, cannot reach your server unless you set up remote access
([DEPLOYMENT.md](DEPLOYMENT.md) — at your own risk).

---

## The four ways devices find your server

| Method | How it works | Example |
|--------|--------------|---------|
| **Local IP** | The server prints its IP on startup | `http://192.168.1.5:4142` |
| **localhost** | The same computer | `http://localhost:4142` |
| **mDNS domain** | Friendly `.local` names via `zeroconf` | `http://arun.local` |
| **QR code** | Auto-generated at startup | scan with a phone camera |

---

## Ports

| Port | Service | Default |
|------|---------|---------|
| `4142` | HTTP server (web app + files + REST API) | from `config.json` |
| `4143` | WebSocket server (real-time collaboration) | fixed |

Both servers bind to `0.0.0.0` so any device on the network can connect.

---

## mDNS `.local` domains

When the server starts and `aliases` is non-empty in `config.json`, the mDNS
service (`dns_service.py`) registers each alias as a `_http._tcp.local.`
service. Each alias becomes a hostname:

```
http://<alias>.local
```

### Domains registered in this repo's config

The author's `config.json` defines these aliases — all resolve on the same
network while the server is running:

| Alias → Domain | Alias → Domain | Alias → Domain |
|----------------|----------------|----------------|
| `sajilo` → `http://sajilo.local` | `server` → `http://server.local` | `pooja` → `http://pooja.local` |
| `pooju` → `http://pooju.local` | `18` → `http://18.local` | `dattey` → `http://dattey.local` |
| `gayjay` → `http://gayjay.local` | `arun` → `http://arun.local` | `karuna` → `http://karuna.local` |
| `miss` → `http://miss.local` | `gaynil` → `http://gaynil.local` | `gunil` → `http://gunil.local` |
| `gay` → `http://gay.local` | `goban` → `http://goban.local` | `chikni` → `http://chikni.local` |
| `virat` → `http://virat.local` | `kohli` → `http://kohli.local` | `arundada9000` → `http://arundada9000.local` |
| `a` → `http://a.local` | `b` → `http://b.local` | |

**Important details:**
- `.local` names resolve **only while the server is running**.
- They resolve **only on the same network** (mDNS is broadcast, not routed).
- You can add/remove aliases anytime in `config.json` — see
  [CONFIGURATION.md](CONFIGURATION.md#aliases).
- Some Android devices need a tiny delay before `.local` resolves; using the IP
  or QR always works.

---

## The QR code

On startup, the server:
1. Generates a QR code encoding `http://<local-ip>:<port>`.
2. Prints it in the terminal.
3. Saves it to `Home/qr.png`.

To connect a phone: open the camera app → point at the QR (or open
`Home/qr.png` in the browser) → tap the link. Done.

> `Home/qr.png` is regenerated on every start, so it's git-ignored.

---

## Firewall notes

Windows/macOS may block Python the first time it listens. Allow it:

- **Windows:** see [DEPLOYMENT.md → Windows Firewall](DEPLOYMENT.md#windows-firewall).
- **macOS:** macOS will show *"Do you want to allow Python to accept incoming connections?"* → click **Allow**.

If other devices can't connect but localhost works, it's almost always a firewall
rule. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

---

## Getting your local IP (no server running)

- **Windows:** `ipconfig` → "IPv4 Address" (e.g. `192.168.1.5`)
- **macOS/Linux:** `ipconfig getifaddr en0` or `hostname -I`

These IPs start with `192.168.x.x`, `10.x.x.x`, or `172.16–31.x.x` — that's the
private LAN range.

---

## Can I access it from the internet?

Not by default — by design. If you *really* need remote access, read
[DEPLOYMENT.md → Remote access](DEPLOYMENT.md#remote-access-port-forwarding).
We strongly recommend a VPN over port forwarding.
