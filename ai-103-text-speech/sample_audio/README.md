# Sample audio

The Speech SDK expects WAV files at **16 kHz / 16-bit mono PCM**. Binary WAVs
aren't checked into this repo — the exercises have you generate `hello.wav`
end-to-end via `POST /speak`, so you rarely need a hand-rolled test file.

If you want to verify `/transcribe` before `/speak` works (or if you want to
experiment with another utterance), generate a compatible WAV with `ffmpeg`.

## Recipe 1 — Synthesize 5 seconds of a spoken phrase via `espeak`

```bash
# espeak writes a proprietary sample rate; pipe it through ffmpeg to normalize.
espeak "Hello from Summitline Outfitters." --stdout \
  | ffmpeg -y -i - -ar 16000 -ac 1 -sample_fmt s16 -t 5 hello.wav
```

## Recipe 2 — Generate a 5-second 440 Hz sine tone (silent STT test)

Useful only for confirming file format; STT will return `NoMatch` on a tone.

```bash
ffmpeg -y -f lavfi -i "sine=frequency=440:duration=5" \
  -ar 16000 -ac 1 -sample_fmt s16 tone.wav
```

## Recipe 3 — Re-encode an existing WAV to the right format

```bash
ffmpeg -y -i input.wav -ar 16000 -ac 1 -sample_fmt s16 fixed.wav
```

## Confirm the format

```bash
ffprobe -v error -show_streams fixed.wav | grep -E "sample_rate|channels|codec_name"
```

You should see `sample_rate=16000`, `channels=1`, `codec_name=pcm_s16le`.
