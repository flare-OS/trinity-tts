"""Lightweight text-to-speech components for Trinity TTS."""

from .config import HardwareProfile, ModelConfig
from .frontend import TextFrontend
from .synthesizer import Synthesizer

__all__ = ["HardwareProfile", "ModelConfig", "Synthesizer", "TextFrontend"]
