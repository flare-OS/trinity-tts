"""Command-line interface for Trinity TTS."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from trinity_tts.config import PROFILES
    from trinity_tts.synthesizer import Synthesizer
else:
    from .config import PROFILES
    from .synthesizer import Synthesizer

# Compatibility for the common-but-invalid `python -m cli.py` invocation from
# inside this directory: runpy imports `cli` first and then searches for a
# `py` submodule, so exposing this file as a package lets `py.py` handle it.
if __name__ == "cli":
    __path__ = [str(Path(__file__).resolve().parent)]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate lightweight TTS WAV audio.")
    parser.add_argument("text", help="Text to speak")
    parser.add_argument("--output", "-o", default="trinity.wav", help="Output WAV path")
    parser.add_argument("--profile", choices=sorted(PROFILES), default="edge", help="Hardware profile")
    parser.add_argument("--speaking-rate", type=float, default=1.0, help="Speech speed multiplier")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    Synthesizer(profile=PROFILES[args.profile]).save_wav(
        args.text,
        args.output,
        speaking_rate=args.speaking_rate,
    )
    print(f"Saved speech to {args.output}")


if __name__ == "__main__":
    main()
