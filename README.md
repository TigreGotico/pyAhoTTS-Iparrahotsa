# AhoTTS Iparrahotsa Python

[AhoTTS_Iparrahotsa](https://github.com/aholab/AhoTTS_Iparrahotsa) is a Text-to-Speech
conversor for **Northern (continental) Basque** — the *Iparralde* dialect. It is a
dialect fork of the classic AhoTTS V1 engine and includes linguistic processing and a
built voice for Northern Basque. Its acoustic engine is based on `hts_engine` and it
uses the high-quality AhoCoder vocoder. Developed by Aholab Signal Processing
Laboratory, at the Bilbao School of Engineering (University of the Basque Country).

This is the Northern-dialect counterpart of
[pyAhoTTS](https://github.com/TigreGotico/pyAhoTTS). Differences from the Southern
engine:

- **Basque-only** (`eu`); there is no Spanish module.
- **/h/ is pronounced** as a real phone (silent in the South).
- **French rounded vowels** ü (/y/) and ö (/ø/).
- **Uvular r** (SAMPA `R` → IPA ʁ).
- Input text encoding is **WINDOWS-1252 (cp1252)**, not ISO-8859-15.

## Install

```bash
pip install pyahotts_iparrahotsa
```

`libhtts_x86_64.so` is bundled with the package. For other architectures (e.g.
`aarch64`) build the library yourself (see below) and pass `lib_path`.

## Compile

```bash
git clone https://github.com/TigreGotico/pyAhoTTS-Iparrahotsa
cd pyAhoTTS-Iparrahotsa
mkdir build && cd build
cmake .. -DCMAKE_POLICY_VERSION_MINIMUM=3.5
make -j"$(nproc)"
cp src/libhtts.so ../pyahotts_iparrahotsa/libhtts_$(uname -m).so
```

> Only `x86_64` is committed. `aarch64` needs a native build (run the above on an
> aarch64 host and commit `libhtts_aarch64.so`).

## Usage

```python
from pyahotts_iparrahotsa import AhoTTSIparrahotsa  # also exported as AhoTTS

tts = AhoTTSIparrahotsa()

audio_bytes = tts.get_tts("Kaixo, ongi etorri!", lang="eu", wav_path="output_eu.wav")
if audio_bytes:
    print(f"Generated {len(audio_bytes)} bytes of audio.")
```

## Phonemes (phonetic transcription)

`get_tts` synthesizes audio; `get_phonemes` runs only the linguistic front end
(number/date/abbreviation normalization, grapheme-to-phoneme, syllabification and
lexical stress) with the Northern dialect rules (`PhTIparralde`) enabled, and returns
the SAMPA (or IPA) transcription — the AhoTTS linguistic analysis exposed directly,
without the acoustic stage.

Full documentation: [`docs/`](docs/README.md).

```python
from pyahotts_iparrahotsa import AhoTTSIparrahotsa

tts = AhoTTSIparrahotsa()

# one list of phones per word; lexical stress is a leading "'" on the nucleus.
# note the leading /h/ on "Hau", "hori", "hemen" — the Northern feature.
tts.get_phonemes("Hau eta hori hemen daude.", lang="eu", ipa=True)
# [['h', "'a", 'w'], ['e', 't', 'a'], ['h', "'o", 'ɾ', 'i'],
#  ['h', 'e', 'm', "'e", 'n'], ['d', 'a', 'w', 'ð', "'e"]]

tts.get_phonemes("bürü", lang="eu", ipa=True)
# [['b', 'y', 'ʁ', 'y']]   # French ü = /y/, uvular r = ʁ
```

## LICENSE

Read `COPYRIGHT_and_LICENSE_code.txt` and `COPYRIGHT_and_LICENSE_voices.txt`. The
engine sources are GPL-3.0+; the voice/linguistic data is CC BY-SA 3.0.

    Basque (voice models & linguistic data):
     	Copyright: Aholab Signal Processing Laboratory, University of the Basque Country (UPV/EHU)
    	License: The files in this package are licensed under a Creative Commons Attribution-ShareAlike 3.0 Unported License.
    	         http://creativecommons.org/licenses/by-sa/3.0/

## Credits

> Based on the [AhoTTS_Iparrahotsa engine](https://github.com/aholab/AhoTTS_Iparrahotsa)
> by Aholab (UPV/EHU). The ctypes binding and transcription patch follow
> [TigreGotico/pyAhoTTS](https://github.com/TigreGotico/pyAhoTTS).
