from trinity_tts.frontend import TextFrontend


def test_normalize_collapses_noise():
    frontend = TextFrontend()

    assert frontend.normalize("Hello---WORLD!!!") == "hello world!!!"


def test_encode_returns_ids():
    frontend = TextFrontend()

    encoded = frontend.encode("Hi")

    assert encoded
    assert all(isinstance(token, int) for token in encoded)
