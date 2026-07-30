# pyAhoTTS-Iparrahotsa documentation

This is the Python binding for [AhoTTS_Iparrahotsa](https://github.com/aholab/AhoTTS_Iparrahotsa),
the **Northern (continental) Basque dialect** text-to-speech engine from the Aholab
Signal Processing Laboratory at the University of the Basque Country (UPV/EHU). It is
a dialect fork of AhoTTS V1: the engine structure is the same, but the transcription
rules are the *Iparralde* rules. Unlike the Southern engine wrapped by
[pyAhoTTS](https://github.com/TigreGotico/pyAhoTTS), this engine:

- is **Basque-only** (`eu`, with no Spanish module),
- **pronounces /h/** as a real phone,
- has the **French rounded vowels** (ü = /y/, ö = /ø/),
- uses a **uvular r** (SAMPA `R` → IPA ʁ),
- expects input text in **WINDOWS-1252 (cp1252)**.

`pyahotts_iparrahotsa` wraps the compiled engine (`libhtts`) through `ctypes`. It
ships the native library and all voice and dictionary data inside the wheel, so you
can synthesize speech, and get phonetic transcriptions, without compiling anything.

```python
from pyahotts_iparrahotsa import AhoTTSIparrahotsa  # or: AhoTTS (alias)

tts = AhoTTSIparrahotsa()
tts.get_tts("Kaixo, ongi etorri!", lang="eu", wav_path="out.wav")   # text -> audio
tts.get_phonemes("Hau eta hori hemen daude.", lang="eu", ipa=True)  # text -> phonemes
# [['h', "'a", 'w'], ['e', 't', 'a'], ['h', "'o", 'ɾ', 'i'], ['h', 'e', 'm', "'e", 'n'], ['d', 'a', 'w', 'ð', "'e"]]
```

Note the leading `h` on *Hau / hori / hemen*. It is the Northern dialect feature
absent from the Southern V1 engine.

## Contents

- [Installation](installation.md): pip install, and building `libhtts` from source.
- [Usage](usage.md): the `AhoTTSIparrahotsa` API for synthesis and phonemization.
- [Phonemes](phonemes.md): phonetic transcription, SAMPA/IPA, stress, the Northern phones.
- [Architecture](architecture.md): how the binding and the C engine fit together.
- [Building libhtts](building.md): the CMake build, the C API, per-architecture `.so` notes.
- [Versions & source of truth](versions.md): the AhoTTS lineage and what this bundles.
- [Testing](testing.md): unit and end-to-end golden tests, regenerating fixtures, CI.
- [Licensing](licensing.md): the split license and credits.

## At a glance

| | |
|---|---|
| Dialect | Northern / continental Basque (Iparralde) |
| Languages | Basque (`eu`) only |
| Synthesis output | 16-bit mono PCM WAV @ 16 kHz |
| Phoneme output | per-word phone lists, SAMPA or IPA, lexical stress as a leading `'` |
| Native lib | `libhtts` (bundled `.so` for `x86_64`, build `aarch64` yourself) |
| Runtime deps | `numpy` only |
| Internal text encoding | WINDOWS-1252 (cp1252) |
