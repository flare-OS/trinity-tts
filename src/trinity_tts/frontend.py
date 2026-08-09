"""Text normalization and tokenization for compact TTS inference."""

from __future__ import annotations

import re
import string

_ALPHABET = " _'.,!?" + string.ascii_lowercase
_TOKEN_TO_ID = {token: index for index, token in enumerate(_ALPHABET)}


class TextFrontend:
    """Normalize text and convert it to stable character-level IDs."""

    vocab_size = len(_TOKEN_TO_ID)

    def normalize(self, text: str) -> str:
        """Lowercase text, remove unsupported symbols, and collapse whitespace."""

        lowered = text.lower().strip()
        cleaned = re.sub(r"[^a-z0-9 _'.,!?-]", " ", lowered)
        cleaned = re.sub(r"\d", lambda match: f" {match.group(0)} ", cleaned)
        cleaned = cleaned.replace("-", " ")
        return re.sub(r"\s+", " ", cleaned).strip()

    def encode(self, text: str) -> list[int]:
        """Encode normalized text into token IDs, mapping unknowns to spaces."""

        normalized = self.normalize(text)
        return [_TOKEN_TO_ID.get(character, _TOKEN_TO_ID[" "]) for character in normalized]
