# Architecture

pyAhoTTS-Iparrahotsa is a thin `ctypes` binding over the native **`libhtts`**
library compiled from the AhoTTS_Iparrahotsa C/C++ sources in `src/`.

```
your code
   │  AhoTTSIparrahotsa.get_tts / get_phonemes   (pyahotts_iparrahotsa/__init__.py)
   ▼
ctypes  ──►  libhtts.so                          (src/, built via CMake)
                 │
                 ├─ linguistic front end (eu_* : normalization, G2P,
                 │     syllabification, stress, Iparralde rules)  →  utterance of phones
                 ├─ HTS acoustic engine          →  parameter streams
                 └─ AhoCoder vocoder             →  waveform
```

This engine is **Basque-only** — there are no `es_*` (Spanish) sources, unlike
pyAhoTTS.

## Python surface (`pyahotts_iparrahotsa/__init__.py`)

`AhoTTSIparrahotsa` loads `libhtts` with `ctypes.cdll`, declares the C prototypes,
and exposes `get_tts`, `get_phonemes`, plus the `SAMPA_TO_IPA` table. It encodes
text as **cp1252** (the Northern dialect input encoding), converts the returned
`c_short` sample buffer into NumPy `int16`, and writes WAV when asked. The class is
also exported as `AhoTTS` for API parity.

## Exported C API (`src/htts_wrapper.cpp`)

| symbol | purpose |
|---|---|
| `create_tts(data_path, lang)` | build an engine for Basque (loads `eu_dicc`, `aholab_eu_female`, sets `PhTIparralde=yes`) |
| `synthesize_text(tts, text, data_path, lang, &samples, &len)` | text → `int16` samples |
| `transcribe_text(tts, text, data_path, lang) -> char*` | text → SAMPA, one word per line, stress as `'` |
| `free_samples(short*)` / `free_string(char*)` | free engine-allocated buffers |
| `destroy_tts(tts)` | free the engine |

`create_tts` additionally calls `tts->set("PhTIparralde", "yes")` to enable the
Northern transcription rules — this is the key difference from pyAhoTTS's wrapper.

## The transcription path

`transcribe_text` reuses the engine's linguistic stage and stops before acoustic
synthesis. It runs `input_multilingual` then walks the resolved utterance with
`HTS_U2W::pho2sampa`, emitting canonical SAMPA per phone (`phone_tosampa`), one word
per line, stress as a leading `'`. Because no voice models are loaded on this path,
the destructor guards `HTS_Engine_clear` with an "engine initialized" flag —
otherwise transcribing (or merely creating an engine) and then destroying it would
free uninitialized pointers.

These transcription additions (`pho2sampa`, `transcribe_do_next_sentence`,
`transcribe_next`, the destructor guard, and the `htts_wrapper.cpp` C API) are the
same patch applied to pyAhoTTS, ported onto the Iparrahotsa engine sources.

## Data layout (`data_tts/`)

```
data_tts/
  dicts/   eu_dicc.dic                  # Northern Basque dictionary
  voices/  aholab_eu_female/            # HTS voice model
```

`data_path` defaults to the packaged `data_tts`; override it to point at custom
dictionaries/voices.
