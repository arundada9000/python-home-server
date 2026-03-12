# Security Policy

## Supported Versions

SajiloCloud is proprietary software under active development. Only the latest
release on the `main` branch receives security fixes.

| Version | Supported |
|---------|-----------|
| `main` (current) | ✅ |
| Older releases | ❌ |

## Reporting a Vulnerability

**Do not open a public issue for security problems.** Report vulnerabilities
privately to the maintainer:

- **Email:** [arunneupane0000@gmail.com](mailto:arunneupane0000@gmail.com)
- **GitHub:** https://github.com/arundada9000

Include in your report:

1. A description of the vulnerability and its impact.
2. Steps to reproduce (without exposing sensitive data).
3. Affected endpoints/files, if known.
4. Your contact details (optional).

You will receive a response within **7 days**. We ask that you do not disclose
the issue publicly until it has been addressed.

## Security Notes for Users

SajiloCloud is designed for **trusted local networks only**.

- The server binds to `0.0.0.0` — anything on your LAN can reach it.
- `config.json` contains the **admin key** and must **never** be committed or shared.
- The admin key (`show_hidden` parameter) grants visibility of hidden folders.
- There is **no TLS** — do not expose the server to the public internet without
  putting it behind a reverse proxy (HTTPS), a VPN, and proper authentication.
- Deleting to the recycle bin is reversible; **purge** is permanent.
- If you expose this software remotely, you do so **at your own risk** and are
  responsible for additional hardening (see [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)).

## Secrets in This Repo

The following files contain or can contain sensitive values and are
**git-ignored** — verify with `git status` that none are ever staged:

| File | Contains |
|------|----------|
| `config.json` | `admin_key` (password) |
| `data/activity_log.json` | Access history |
| `data/comments.json` | User comments |
| `Home/qr.png` | LAN QR code (not secret, but generated) |

If you believe a secret was accidentally committed, rotate it and contact the
maintainer immediately.
