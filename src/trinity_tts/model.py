"""Tiny neural acoustic model components.

PyTorch is imported only when this module is used so the CLI can still synthesize
basic speech on machines that only have the Python standard library installed.
"""

from __future__ import annotations

from .config import ModelConfig


class TinyAcousticModel:  # pragma: no cover - exercised when torch is installed
    """Factory wrapper that builds a compact depthwise-separable TTS model."""

    @staticmethod
    def build(config: ModelConfig):
        import torch
        from torch import nn

        class DepthwiseBlock(nn.Module):
            def __init__(self, channels: int, dropout: float) -> None:
                super().__init__()
                self.net = nn.Sequential(
                    nn.Conv1d(channels, channels, kernel_size=5, padding=2, groups=channels),
                    nn.GELU(),
                    nn.Conv1d(channels, channels, kernel_size=1),
                    nn.Dropout(dropout),
                )
                self.norm = nn.LayerNorm(channels)

            def forward(self, values: torch.Tensor) -> torch.Tensor:
                residual = values
                values = self.net(values.transpose(1, 2)).transpose(1, 2)
                return self.norm(values + residual)

        class AcousticModel(nn.Module):
            def __init__(self) -> None:
                super().__init__()
                self.embedding = nn.Embedding(config.vocab_size, config.hidden_size)
                self.blocks = nn.ModuleList(
                    DepthwiseBlock(config.hidden_size, config.dropout) for _ in range(config.layers)
                )
                self.mel_head = nn.Linear(config.hidden_size, config.mel_bins)
                self.energy_head = nn.Linear(config.hidden_size, 1)
                self.pitch_head = nn.Linear(config.hidden_size, 1)

            def forward(self, token_ids: torch.Tensor) -> dict[str, torch.Tensor]:
                hidden = self.embedding(token_ids)
                for block in self.blocks:
                    hidden = block(hidden)
                return {
                    "mel": self.mel_head(hidden),
                    "energy": self.energy_head(hidden).squeeze(-1),
                    "pitch": self.pitch_head(hidden).squeeze(-1),
                }

        return AcousticModel()
