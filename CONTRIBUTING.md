# Contributing to SajiloCloud

First off - thank you for your interest! Because SajiloCloud is **proprietary software**, the standard open-source contribution flow works a little differently here. Please read this page before doing anything.

## License Notice - Read First

SajiloCloud is **not free for use** and requires **explicit written permission** from the copyright holder for *every* use - including copying, modifying, and contributing code.

Before you fork, clone, or submit anything:

1. Contact **Arun Neupane** - [arunneupane0000@gmail.com](mailto:arunneupane0000@gmail.com)
2. Explain what you'd like to do (use, modify, contribute).
3. Wait for written approval.

Submitting a contribution does **not** grant you any rights to the project. All contributions become the property of the copyright holder. If you were invited to contribute, you'll receive explicit permission along with the invitation.

## Ways to Contribute

### 1. Report Bugs
If the project owner has granted you access, and you find a bug:

- Search the issue tracker first to avoid duplicates.
- Open a bug report using the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.md).
- Include: OS + Python version, exact steps to reproduce, expected vs. actual behavior, and any terminal output.

### 2. Suggest Features
- Open a [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md).
- Describe the problem you're solving and a concrete proposal.

### 3. Write Documentation
Documentation fixes are always welcome (with permission). Keep the tone practical and beginner-friendly.

### 4. Submit Code
Once you have written permission and a task is agreed with the maintainer:

1. Create a feature branch: `git checkout -b feat/your-feature`
2. Follow the [Developer Guide](docs/DEVELOPMENT.md).
3. Keep changes small and focused.
4. Test that both servers start cleanly:
 ```bash
 python server.py
 python websocket_server.py
 ```
5. Commit with a clear message and open a PR against `main`.

## Code Style

- **Python:** 4-space indentation, standard library first, keep dependencies minimal.
- **JavaScript:** 2-space indentation, vanilla ES6+, no build step.
- **HTML/CSS:** follow existing class conventions in `styles.css`.
- **No comments** unless they explain *why* (not *what*).
- Never commit `config.json`, `data/*`, or anything generated at runtime.

## Commit Convention

Use conventional prefixes so history stays readable:

```
feat: add new feature
fix: fix a bug
docs: documentation only
chore: tooling / housekeeping
build: dependency or build changes
refactor: code change with no behavior change
test: add/update tests
ci: CI configuration
```

## Before You Open a PR

- Run `python server.py` and `python websocket_server.py` - both must start without errors.
- Run `git status` and make sure **no** runtime files (`config.json`, `server_debug.log`, `Home/**`, `data/*`) are staged.
- Reference the issue your PR closes: `Closes #12`.

## Questions?

Open a discussion or email the maintainer. Please be patient - responses are typically fastest between 1 AM and 3 AM Nepal time (UTC+5:45). 

---

*SajiloCloud is maintained by [Arun Neupane](https://github.com/arundada9000).*
