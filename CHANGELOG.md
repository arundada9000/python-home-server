# Changelog

All notable changes to **SajiloCloud** are documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project is **proprietary** — see [LICENSE](LICENSE).

---

## [Unreleased]

### Added
- Initial public repository release of SajiloCloud.
- Complete documentation suite under `docs/`:
  - Dummy-proof quickstart, installation, and running guides
  - Networking & `.local` domains guide
  - Full configuration and API references
  - Deployment, troubleshooting, FAQ, and developer guides
- Community health files: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`.
- GitHub templates: bug report, feature request, pull request.
- CI workflow (Python syntax check + dependency sanity).
- `requirements.txt` dependency manifest and `config.json.example`.
- Proprietary license declaration.

### Fixed
- `start_server.bat` previously hardcoded `cd /d E:\Server`; now resolves to the
  script's own directory (`%~dp0`) so it works from any clone location.
- `.gitignore`: corrected `!data/.geetkeep` → `!data/.gitkeep`.
- `.gitignore`: `Home/server-icons/` (file-type icons) now tracked instead of ignored.
- File uploads no longer depend on the `cgi` module (removed in Python 3.13).
  A streaming multipart parser replaces `cgi.FieldStorage`, so the server now
  runs on Python 3.7 through 3.14+.

---

## Backlog (planned)

- HTTPS support via reverse-proxy guide.
- User accounts & per-user folders.
- Upload resumable / chunked support.
- Docker deployment recipe.
