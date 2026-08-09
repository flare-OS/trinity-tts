# Trinity TTS

Trinity TTS is a lightweight text-to-speech research toolkit designed around a compact,
human-like speech stack that can scale down to CPU-only and edge hardware.

The initial implementation includes:

- A deterministic text frontend for normalization and phoneme-like tokenization.
- A tiny acoustic model architecture based on depthwise-separable residual blocks.
- A hardware profile system for selecting model size and quantization-friendly settings.
- A dependency-light synthesizer that can produce WAV output without GPU-only features.

## Quick start

```bash
python -m trinity_tts.cli "Hello from Trinity TTS" --output hello.wav
```

If you are already inside `src/trinity_tts`, these local development forms also work:

```bash
python -m cli "Hello from Trinity TTS" --output hello.wav
python -m cli.py "Hello from Trinity TTS" --output hello.wav
python cli.py "Hello from Trinity TTS" --output hello.wav
```

For training experiments, install the optional PyTorch dependency:

```bash
pip install -e '.[train,dev]'
```

## Design goals

1. **Runs anywhere:** CPU-first inference, small memory footprint, and simple WAV output.
2. **Sounds human:** expressive prosody controls and a neural acoustic-model path.
3. **Easy to shrink:** hardware profiles tune hidden dimensions, layer count, and quantization.
4. **Hackable:** modular frontend, model, and synthesis components.
