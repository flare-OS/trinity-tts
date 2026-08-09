"""Dependency-light speech synthesis utilities."""

from __future__ import annotations

import math
import random
import wave
from array import array
from dataclasses import dataclass
from pathlib import Path

from .config import PROFILES, HardwareProfile
from .frontend import TextFrontend


@dataclass
class Synthesizer:
    """CPU-first TTS synthesizer with a deterministic fallback vocoder."""

    profile: HardwareProfile = PROFILES["edge"]
    frontend: TextFrontend = TextFrontend()

    def synthesize(self, text: str, speaking_rate: float = 1.0) -> array:
        """Return mono PCM samples as an array of float32 values in [-1, 1]."""

        token_ids = self.frontend.encode(text)
        if not token_ids:
            return array("f", [0.0] * (self.profile.sample_rate // 10))

        duration_per_token = max(0.035, 0.075 / max(speaking_rate, 0.25))
        samples_per_token = int(self.profile.sample_rate * duration_per_token)
        waveform = array("f")

        for token in token_ids:
            waveform.extend(self._render_token(token, samples_per_token))

        fade = min(len(waveform) // 8, max(1, self.profile.sample_rate // 200))
        last_index = len(waveform) - 1
        for index, sample in enumerate(waveform):
            if index < fade:
                sample *= index / fade
            elif index > last_index - fade:
                sample *= (last_index - index) / fade
            waveform[index] = max(-1.0, min(1.0, sample))
        return waveform

    def save_wav(self, text: str, output_path: str | Path, speaking_rate: float = 1.0) -> Path:
        """Synthesize text and save it as a 16-bit PCM WAV file."""

        waveform = self.synthesize(text, speaking_rate=speaking_rate)
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        pcm = array("h", (int(sample * 32767) for sample in waveform))
        with wave.open(str(output), "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(self.profile.sample_rate)
            wav_file.writeframes(pcm.tobytes())
        return output

    def _render_token(self, token: int, length: int) -> array:
        rng = random.Random(token)
        samples = array("f")
        base_frequency = 120.0 + (token % 24) * 7.5
        for frame in range(length):
            time = frame / self.profile.sample_rate
            vibrato = 1.0 + 0.015 * math.sin(2 * math.pi * 5.5 * time)
            voiced = math.sin(2 * math.pi * base_frequency * vibrato * time)
            formant = 0.35 * math.sin(2 * math.pi * (base_frequency * 2.1) * time)
            breath = 0.025 * rng.uniform(-1.0, 1.0)
            samples.append(0.55 * voiced + formant + breath)
        return samples
