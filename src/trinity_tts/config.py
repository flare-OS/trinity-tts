"""Configuration primitives for hardware-aware TTS models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HardwareProfile:
    """Inference constraints used to size the model for a target device."""

    name: str
    max_parameters: int
    quantized: bool
    sample_rate: int = 22_050


PROFILES: dict[str, HardwareProfile] = {
    "micro": HardwareProfile("micro", max_parameters=750_000, quantized=True, sample_rate=16_000),
    "edge": HardwareProfile("edge", max_parameters=2_500_000, quantized=True),
    "desktop": HardwareProfile("desktop", max_parameters=8_000_000, quantized=False),
}


@dataclass(frozen=True)
class ModelConfig:
    """Compact acoustic model settings."""

    vocab_size: int
    hidden_size: int = 128
    layers: int = 6
    mel_bins: int = 80
    speaker_embedding_size: int = 32
    dropout: float = 0.05

    @classmethod
    def for_profile(cls, vocab_size: int, profile: HardwareProfile) -> "ModelConfig":
        """Create a small but expressive model configuration for a hardware profile."""

        if profile.name == "micro":
            return cls(vocab_size=vocab_size, hidden_size=64, layers=4, mel_bins=64, speaker_embedding_size=16)
        if profile.name == "edge":
            return cls(vocab_size=vocab_size, hidden_size=96, layers=6, mel_bins=80, speaker_embedding_size=24)
        return cls(vocab_size=vocab_size, hidden_size=160, layers=8, mel_bins=100, speaker_embedding_size=40)
