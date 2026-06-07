# CI/CD Workflows

> How Orbiton's GitHub Actions are configured, and how to modify them.

---

## Current Workflows

| Workflow | File | What it tests | Runs on | Trigger |
|----------|------|--------------|---------|---------|
| Core Logic | `.github/workflows/core-logic.yml` | Intent parsing, command patterns, NLP | Ubuntu | push, PR |
| URL Engine | `.github/workflows/url-engine.yml` | URL generation for all web commands | Ubuntu | push, PR |
| Compute | `.github/workflows/compute.yml` | Math expressions, security, constants | Ubuntu | push, PR |
| Launch | `.github/workflows/launch.yml` | File operations, projects, scripts | Windows | push, PR |
| System | `.github/workflows/system.yml` | Status, time, motivation, hardware | Ubuntu | push, PR |
| Integration | `.github/workflows/integration.yml` | End-to-end command flows | Ubuntu | push, PR |
| Pylint | `.github/workflows/pylint.yml` | Code quality for main files | Ubuntu | push, PR |

---

## Why Windows for Launch?

Launch tests use `subprocess.Popen(["explorer.exe", ...])` on Windows, which is different from Linux/macOS (`subprocess.run(["open"/"xdg-open", ...])`). Running on Windows ensures the actual Windows file-opening path is tested.

---

## Workflow Template

```yaml
name: <Category>

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: <ubuntu-latest | windows-latest | macos-latest>
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - run: pip install pytest speechrecognition rich
      - run: pytest tests/<category>/ -v --tb=short
```

---

## Adding a New Workflow

1. Create `.github/workflows/<name>.yml`
2. Copy the template above
3. Set `name`, `runs-on`, and `pytest` path
4. Add the badge to README.md and TEST_STATUS.md

Example for a new `plugins` category:

```yaml
name: Plugins

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - run: pip install pytest speechrecognition rich
      - run: pytest tests/plugins/ -v --tb=short
```

Badge to add:

```markdown
![Plugins](https://github.com/AymanHaidry/Kosmosic-Orbiton/actions/workflows/plugins.yml/badge.svg)
```

---

## Pylint Workflow

The pylint workflow is special — it doesn't run tests, it checks code quality:

```yaml
name: Pylint

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - run: pip install pylint
      - run: pylint kosmosic_orbiton.py neuro_link_intel.py
```

---

## Troubleshooting CI Failures

| Problem | Cause | Fix |
|---------|-------|-----|
| `ModuleNotFoundError: speech_recognition` | Missing dependency | Add `pip install speechrecognition` to workflow |
| `subprocess` patch fails on Windows | Wrong patch target | See `tests/launch/` for `_patch_open_explorer()` pattern |
| `Path.exists()` returns False | CI doesn't have real folders | Mock `Path.exists` and `Path.is_dir` in tests |
| Tests pass locally but fail in CI | OS difference | Ensure tests work on both Windows and Ubuntu |
| Pylint fails | Code style issues | Run `pylint kosmosic_orbiton.py neuro_link_intel.py` locally |

---

## Matrix Strategy (Advanced)

If you want to test on multiple OSes simultaneously:

```yaml
strategy:
  fail-fast: false
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    python-version: ['3.11', '3.12', '3.13']
runs-on: ${{ matrix.os }}
steps:
  - uses: actions/setup-python@v5
    with:
      python-version: ${{ matrix.python-version }}
```

---

## Secrets and Environment Variables

If you need API keys or secrets (not currently used):

```yaml
env:
  SOME_API_KEY: ${{ secrets.SOME_API_KEY }}
```

Add secrets in GitHub repo settings → Secrets and variables → Actions.

---

## See Also

- [TEST_STATUS.md](TEST_STATUS.md) — Current CI status for all categories
- [TESTS.md](TESTS.md) — Test architecture and how to write new tests
