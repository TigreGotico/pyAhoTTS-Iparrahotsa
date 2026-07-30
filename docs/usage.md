# Usage

A single class, `AhoTTSIparrahotsa`, exposes everything. It is also exported as
`AhoTTS`, for API parity with pyAhoTTS.

```python
from pyahotts_iparrahotsa import AhoTTSIparrahotsa

tts = AhoTTSIparrahotsa()
```

## `AhoTTSIparrahotsa(lib_path=None, data_path=...)`

| arg | default | meaning |
|---|---|---|
| `lib_path` | bundled `libhtts_<machine>.so` | path to the native library; override for unbundled architectures |
| `data_path` | `<package>/data_tts` | directory holding `dicts/` and `voices/` |

The underlying engine instance is created lazily. This engine supports only Basque
(`eu`).

## Synthesis — `get_tts(text, lang="eu", wav_path=None) -> bytes`

Generates speech and returns raw **16-bit mono PCM @ 16 kHz** bytes. If you pass
`wav_path`, the method also writes a WAV file.

```python
audio = tts.get_tts("Kaixo, ongi etorri!", lang="eu", wav_path="eu.wav")
print(len(audio), "bytes")          # empty bytes on failure
```

- `lang`: `"eu"` (Northern Basque) is the only supported language.
- The method returns `b""` if synthesis fails. It never raises for empty output.

### Numpy / custom playback

The bytes are little-endian `int16`:

```python
import numpy as np
samples = np.frombuffer(tts.get_tts("Kaixo!"), dtype=np.int16)
```

## Phonemization — `get_phonemes(text, lang="eu", ipa=False) -> list[list[str]]`

Runs **only the linguistic front end** (normalization, then grapheme-to-phoneme
conversion, then syllabification, then lexical stress) with the Northern dialect
rules (`PhTIparralde`) enabled. It returns the phonetic transcription, with no audio
synthesis.

```python
tts.get_phonemes("Hau eta hori.", lang="eu")
# [['h', "'a", 'w'], ['e', 't', 'a'], ['h', "'o", 'r', 'i']]

tts.get_phonemes("bürü", lang="eu", ipa=True)
# [['b', 'y', 'ʁ', 'y']]   # French ü = /y/, uvular r = ʁ
```

- The method returns **one list of phones per word**, in order.
- **Lexical stress** appears as a leading `'` on the stressed phone.
- `ipa=False` returns SAMPA phones; `ipa=True` returns IPA through the
  [`SAMPA_TO_IPA`](phonemes.md) table.
- The method returns `[]` if transcription fails.

Number, date, and abbreviation **normalization happens inside the engine**, so
digits and abbreviations expand before phonemization.

See [Phonemes](phonemes.md) for the phone inventory and the SAMPA-to-IPA mapping.

## Languages & voices

| lang | dictionary | bundled voice |
|---|---|---|
| `eu` | `data_tts/dicts/eu_dicc` | `aholab_eu_female` |

## Text encoding

The binding encodes input text to **WINDOWS-1252 (cp1252)** before it reaches the
engine. The Northern dialect README specifies this encoding, not ISO-8859-15 as in
the Southern engine. This matters for French accented characters (ü, ö, û, ñ).
Characters outside cp1252 get replaced.

---
[← Installation](installation.md) · [Home](README.md) · [Phonemes →](phonemes.md)
