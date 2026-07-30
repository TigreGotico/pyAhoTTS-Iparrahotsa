# Licensing & credits

pyAhoTTS-Iparrahotsa carries a **split license**. The Python wrapper, the upstream
engine code, and the bundled voice and linguistic data each use a different license.

| Component | License |
|---|---|
| Python wrapper (`pyahotts_iparrahotsa/__init__.py`, packaging) | MIT |
| AhoTTS_Iparrahotsa engine sources (`src/`, compiled to `libhtts`) | GPL-3.0+ (Aholab / UPV-EHU) |
| Voice models & linguistic data (`data_tts/`, dictionary) | CC BY-SA 3.0 (Aholab / UPV-EHU) |

See `COPYRIGHT_and_LICENSE_code.txt` and `COPYRIGHT_and_LICENSE_voices.txt` in the
repository root for the authoritative terms. The repository's `LICENSE` file states
GPL-3.0. Because the distributed library links the GPL-3.0+ engine, the GPL-3.0+
governs redistribution of the **binary** package. You may reuse the MIT wrapper
code under MIT.

## Credits

- **AhoTTS / AhoTTS_Iparrahotsa**: Aholab Signal Processing Laboratory, University
  of the Basque Country (UPV/EHU). It provides the linguistic processing for
  (Northern) Basque, and the AhoCoder vocoder. Upstream:
  [aholab/AhoTTS_Iparrahotsa](https://github.com/aholab/AhoTTS_Iparrahotsa).
- The HTS acoustic engine derives from `hts_engine` (Nagoya Institute of Technology
  / Tokyo Institute of Technology), under the Modified BSD license (GPL-compatible).
- The transcription patch and ctypes binding follow the approach used in
  [TigreGotico/pyAhoTTS](https://github.com/TigreGotico/pyAhoTTS), which builds on
  the [ekaitz-zarraga/AhoTTS](https://github.com/ekaitz-zarraga/AhoTTS) fork.

---
[← Testing](testing.md) · [Home](README.md)
