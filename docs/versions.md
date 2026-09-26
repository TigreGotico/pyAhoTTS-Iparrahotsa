# Versions & source of truth

Aholab (UPV/EHU) develops AhoTTS upstream. `AhoTTS_Iparrahotsa` is a **dialect fork**
of the classic AhoTTS V1 engine that targets **Northern (continental) Basque**
(Iparralde) instead of the Southern standard.

**The upstream AhoTTS source repositories are the source of truth.**
`pyahotts_iparrahotsa` is *our* binding: it wraps a build of the Iparrahotsa engine
and is validated against it (see [Testing](testing.md)). It is not itself the
reference.

## The lineage

| | Release | Upstream source | Notes |
|---|---|---|---|
| **V1 (South)** | Original AhoTTS | [ekaitz-zarraga/AhoTTS](https://github.com/ekaitz-zarraga/AhoTTS) (= [aholab/AhoTTS](https://github.com/aholab/AhoTTS) before its Dec-2025 rewrite) | Classic linguistic front end; Basque + Spanish; /h/ silent. Wrapped by [pyAhoTTS](https://github.com/TigreGotico/pyAhoTTS). |
| **V1 (North)** | AhoTTS_Iparrahotsa | [aholab/AhoTTS_Iparrahotsa](https://github.com/aholab/AhoTTS_Iparrahotsa) | Same V1 engine structure, Northern dialect: Basque-only, /h/ pronounced, French vowels (ü/ö), uvular r. **This is what this package bundles.** |

The two share the same engine architecture and the same transcription patch
(`pho2sampa`, `transcribe_*`). They differ in the linguistic rules
(`PhTIparralde=yes`), the dictionary (`eu_dicc`), and the input encoding
(WINDOWS-1252).

## What this package provides

`pyahotts_iparrahotsa` bundles and exposes the **Northern dialect** engine. Its
`get_phonemes` and `get_tts` reproduce that engine's behavior, locked down by golden
[end-to-end tests](testing.md), so the bundled binding cannot silently drift from the
upstream source.

## Picking a version

- To synthesize or phonemize **Northern Basque**, use this package.
- For Southern / standard Basque (or Spanish), use
  [pyAhoTTS](https://github.com/TigreGotico/pyAhoTTS) instead.
- To produce phonemes for a **specific pretrained model**, use the release that
  model was trained with. Matching the wrong dialect or release yields
  out-of-distribution input.

---
[← Building libhtts](building.md) · [Home](README.md) · [Testing →](testing.md)
