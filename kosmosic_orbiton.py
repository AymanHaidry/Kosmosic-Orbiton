#!/usr/bin/env python3
"""Compatibility launcher for older scripts and imports.

New installations should use ``python -m stag``. The module alias keeps
legacy imports and monkeypatch-based integrations pointed at the real app.
"""
import sys
from stag import app as _app

if __name__ == "__main__":
    _app.main()
else:
    sys.modules[__name__] = _app
