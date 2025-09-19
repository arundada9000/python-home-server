# Deployment

Taking SajiloCloud from "runs on my laptop" to "runs reliably on my always-on
machine" - plus firewall, VPN, and remote-access options.

> **Security warning:** SajiloCloud has **no TLS and no user authentication**.
> It trusts its network. Only expose it to the internet behind a VPN and/or a
> hardened reverse proxy, at your own risk. See [SECURITY.md](../SECURITY.md).

---

## 1. Pick a host machine

Any always-on device with Python works:

- Old laptop / mini PC / Raspberry Pi
- Windows / macOS / Linux

Install Python + dependencies ([INSTALLATION.md](INSTALLATION.md)), then set a
static IP (router DHCP reservation) so the address never changes.

---

## 2. Firewall rules

Clients on the LAN need access to the server's ports.

### Windows Firewall

1. Press `Win` -> type **"Windows Defender Firewall with Advanced Security"** -> open it.
2. **Inbound Rules** -> **New Rule...**
3. **Port** -> **TCP** -> **Specific local ports:** `4142,4143`
4. **Allow the connection** -> Profile: **Private** (and Public if you trust the network).
5. Name it `SajiloCloud`.

> First run usually prompts *"Allow Python to accept incoming connections?"*
> -> click **Allow** - that often adds the rule automatically.

### Linux (UFW)

```bash
sudo ufw allow 4142/tcp
sudo ufw allow 4143/tcp
sudo ufw reload
```

### macOS

System Settings -> Network -> Firewall -> Options -> **Allow incoming connections**
for the Python process.

---

## 3. Run as a background service

So the server survives reboots and you don't need an open terminal.

### Windows - Task Scheduler

1. Create a `.bat` (e.g. `sajilocloud.bat`):
 ```bat
 @echo off
 cd /d "C:\path\to\sajilocloud"
 python server.py
 ```
2. Task Scheduler -> Create Basic Task -> Trigger: **At startup** -> Action:
 **Start a program** -> pick the `.bat` -> enable **"Run with highest privileges"**
 (needed if `port` is 80).

### Linux - systemd

```ini
# /etc/systemd/system/sajilocloud.service
[Unit]
Description=SajiloCloud File Server
After=network.target

[Service]
WorkingDirectory=/opt/sajilocloud
ExecStart=/usr/bin/python3 server.py
Restart=always
User=sajilocloud

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now sajilocloud
```

---

## 4. Static IP & DNS

- **DHCP reservation** on your router -> the machine always gets the same IP.
- **mDNS** (`http://<alias>.local`) means you rarely need the IP at all - but it
 only works on the LAN and only while the server runs.

---

## 5. Port forwarding (port 80)

If you run with `"port": 80`, LAN clients can use `http://<alias>.local` with no
`:port` suffix. Port 80 needs admin/root privileges (Task Scheduler -> highest
privileges, or `sudo`).

Keeping the default `4142` avoids all that - the URL just includes the port.

---

## 6. Remote access (port forwarding / VPN)

By default the internet can't reach SajiloCloud. Two ways to change that:

### Option A - VPN (recommended)

WireGuard or Tailscale on the server + each device. Remote clients join your
virtual LAN and reach `http://<server>:4142` exactly as if they were home.

- No internet exposure, no TLS worries, no extra auth needed.
- mDNS `.local` names still work inside the VPN.

### Option B - Port forward + reverse proxy (not recommended without hardening)

1. Router -> port forward `WAN:4142 -> <server-ip>:4142`.
2. Put a reverse proxy (Caddy/Nginx) in front with **HTTPS** and an allow-list /
 basic-auth if possible.
3. Understand you are now exposing an **unauthenticated file server** to the
 internet. If the admin key leaks or the proxy is misconfigured, anyone can
 read/delete your files.

**You are fully responsible for anything that happens with remote access.**

---

## 7. Hardening checklist

- [ ] Change `admin_key` to something long and random (see [CONFIGURATION.md](CONFIGURATION.md)).
- [ ] Keep `config.json` out of git (already ignored).
- [ ] Use a VPN for remote access instead of port forwarding.
- [ ] If port-forwarding anyway: HTTPS + auth via reverse proxy.
- [ ] Don't set `"upload_root"` to a system directory.
- [ ] Back up `Home/` (the actual data) regularly - a stray `purge` or disk error
 is permanent.
- [ ] Run as a low-privilege user, not root/Administrator, if you can.

---

## Backups

Everything important lives under `Home/` plus `data/`:

```bash
# Example: nightly tar to an external disk
tar -czf /backup/sajilocloud-$(date +%F).tar.gz Home/ data/
```

The code itself can be re-cloned from git; the files in `Home/` cannot.
