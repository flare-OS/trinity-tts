import wave

from trinity_tts.config import PROFILES
from trinity_tts.synthesizer import Synthesizer


def test_synthesize_returns_audio():
    audio = Synthesizer(profile=PROFILES["micro"]).synthesize("hello")

    assert len(audio) > 0
    assert max(audio) <= 1.0
    assert min(audio) >= -1.0


def test_save_wav(tmp_path):
    output = tmp_path / "voice.wav"

    Synthesizer(profile=PROFILES["micro"]).save_wav("hello", output)

    with wave.open(str(output), "rb") as wav_file:
        assert wav_file.getnchannels() == 1
        assert wav_file.getframerate() == PROFILES["micro"].sample_rate
