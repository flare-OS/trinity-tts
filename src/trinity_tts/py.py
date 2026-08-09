"""Compatibility shim for `python -m cli.py` from this directory."""

from __future__ import annotations

from cli import main


if __name__ == "__main__":
    main()
