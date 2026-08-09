"""Command-line interface for Trinity TTS."""

from __future__ import annotations

import argparse

from .config import PROFILES
from .synthesizer import Synthesizer


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
