# AhoTTS Iparrahotsa Python

[AhoTTS_Iparrahotsa](https://github.com/aholab/AhoTTS_Iparrahotsa) is a text-to-speech
engine for **Northern (continental) Basque** (the *Iparralde* dialect). It is a
dialect fork of the classic AhoTTS V1 engine. It includes linguistic processing and a
voice for Northern Basque. Its acoustic engine is based on `hts_engine`, and it uses
the AhoCoder vocoder. Aholab Signal Processing Laboratory, at the Bilbao School of
Engineering (University of the Basque Country), develops AhoTTS.

This package is the Northern-dialect counterpart of
[pyAhoTTS](https://github.com/TigreGotico/pyAhoTTS). The two engines differ:

- This engine is **Basque-only** (`eu`). It has no Spanish module.
- **/h/ is pronounced** here. It is silent in the Southern engine.
- This engine has **French rounded vowels**: ü (/y/) and ö (/ø/).
- This engine uses a **uvular r** (SAMPA `R` → IPA ʁ).
- Input text uses **WINDOWS-1252 (cp1252)** encoding, not ISO-8859-15.

## Install

```bash
pip install pyahotts_iparrahotsa
```

The package bundles `libhtts_x86_64.so`. For other architectures (for example
`aarch64`), build the library yourself (see below) and pass `lib_path`.

## Compile

```bash
git clone https://github.com/TigreGotico/pyAhoTTS-Iparrahotsa
cd pyAhoTTS-Iparrahotsa
mkdir build && cd build
cmake .. -DCMAKE_POLICY_VERSION_MINIMUM=3.5
make -j"$(nproc)"
cp src/libhtts.so ../pyahotts_iparrahotsa/libhtts_$(uname -m).so
```

> Only `x86_64` is committed. For `aarch64`, run the build above on an `aarch64`
> host, then commit `libhtts_aarch64.so`.

## Usage

```python
from pyahotts_iparrahotsa import AhoTTSIparrahotsa  # also exported as AhoTTS

tts = AhoTTSIparrahotsa()

audio_bytes = tts.get_tts("Kaixo, ongi etorri!", lang="eu", wav_path="output_eu.wav")
if audio_bytes:
    print(f"Generated {len(audio_bytes)} bytes of audio.")
```

## Phonemes (phonetic transcription)

`get_tts` synthesizes audio. `get_phonemes` runs only the linguistic front end:
number, date, and abbreviation normalization, then grapheme-to-phoneme conversion,
then syllabification, then lexical stress. It uses the Northern dialect rules
(`PhTIparralde`) and returns the SAMPA (or IPA) transcription. It exposes the AhoTTS
linguistic analysis directly, without the acoustic stage.

Full documentation: [`docs/`](docs/README.md).

```python
from pyahotts_iparrahotsa import AhoTTSIparrahotsa

tts = AhoTTSIparrahotsa()

# one list of phones per word; lexical stress is a leading "'" on the nucleus.
# note the leading /h/ on "Hau", "hori", "hemen": the Northern feature.
tts.get_phonemes("Hau eta hori hemen daude.", lang="eu", ipa=True)
# [['h', "'a", 'w'], ['e', 't', 'a'], ['h', "'o", 'ɾ', 'i'],
#  ['h', 'e', 'm', "'e", 'n'], ['d', 'a', 'w', 'ð', "'e"]]

tts.get_phonemes("bürü", lang="eu", ipa=True)
# [['b', 'y', 'ʁ', 'y']]   # French ü = /y/, uvular r = ʁ
```

## Related projects

- [pyAhoTTS](https://github.com/TigreGotico/pyAhoTTS): the Southern (standard)
  Basque and Spanish counterpart of this package.
- [AhoTTS_Iparrahotsa](https://github.com/aholab/AhoTTS_Iparrahotsa): the upstream
  C/C++ engine this package binds to.

## LICENSE

Read `COPYRIGHT_and_LICENSE_code.txt` and `COPYRIGHT_and_LICENSE_voices.txt`. The
engine sources use the GPL-3.0+ license. The voice and linguistic data use the
CC BY-SA 3.0 license.

    Basque (voice models & linguistic data):
     	Copyright: Aholab Signal Processing Laboratory, University of the Basque Country (UPV/EHU)
    	License: The files in this package are licensed under a Creative Commons Attribution-ShareAlike 3.0 Unported License.
    	         http://creativecommons.org/licenses/by-sa/3.0/

## Credits

> Based on the [AhoTTS_Iparrahotsa engine](https://github.com/aholab/AhoTTS_Iparrahotsa)
> by Aholab (UPV/EHU). The ctypes binding and transcription patch follow
> [TigreGotico/pyAhoTTS](https://github.com/TigreGotico/pyAhoTTS).
