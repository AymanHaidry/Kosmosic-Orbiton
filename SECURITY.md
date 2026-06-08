# Security Policy

## Supported Versions

Kosmosic Orbiton is pre-1.0 (0.x.y). There are no formal stability or long-term-support guarantees. Security fixes ship as part of regular minor or patch releases on whatever the current development branch is.

| Version | Supported |
|---------|-----------|
| 0.x (current dev) | ✅ via the next minor release |
| anything older | ❌ |

---

## Reporting a Vulnerability

**Do not open a public issue for security vulnerabilities.**

Instead, report privately via one of these channels:

| Method | Contact |
|--------|---------|
| Email | aymanhaidry2022@outlook.com *(preferred)* |
| GitHub Private Vulnerability Reporting | [Report via GitHub](https://github.com/AymanHaidry/Kosmosic-Orbiton/security/advisories/new) |

### What to include

- Description of the vulnerability
- Steps to reproduce (minimal proof of concept)
- Affected version(s)
- Impact assessment (what can an attacker do?)
- Suggested fix (if you have one)

### Response timeline

| Phase | Target |
|-------|--------|
| Initial acknowledgment | Within 48 hours |
| Severity assessment | Within 5 days |
| Fix released | Next minor or patch release on current dev branch |
| Public disclosure | After fix ships, coordinated with reporter |

### Disclosure policy

- We follow coordinated disclosure. We do not publish details until a fix is available.
- Credit is given to reporters who wish to be named.
- If no response is received from the reporter within 30 days, we proceed with the fix and disclosure independently.

---

## Security-related design decisions

### Pre-1.0 stance

- Breaking changes between 0.x releases are expected.
- Security patches ride along with regular feature releases.
- No backports to older 0.x lines.

### Known limitations (by design)

| Area | Status | Note |
|------|--------|------|
| Code execution via `eval()` in `calculate` | Mitigated | `MathNormalizer.safe_eval()` whitelists only `0-9 + - * / % . ( )` |
| Clipboard access | Platform-native | Uses PowerShell (`Get-Clipboard`), `pbpaste`, or `xclip` — no custom crypto |
| Network requests | Standard library only | `urllib.request` for Wikipedia API, no external HTTP clients |
| File system access | User-scoped | Restricted to `Path.home()` and subdirectories in `handle_open_file` |
| Speech recognition | Cloud (Google) | Audio is processed by Google Speech API; no local model yet |

### Supply chain

- Dependencies are pinned in `requirements.txt`.
- CI runs `pip-audit` or equivalent on every PR (if configured).
- No compiled extensions or binary wheels in the dependency tree.

---

## Acknowledgments

| Date | Reporter | Issue | CVE |
|------|----------|-------|-----|
| — | — | — | — |

*(No security issues reported yet.)*

---

Last updated: 2026-06-07
