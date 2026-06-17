# Licensing & credits

pyAhoTTS-Iparrahotsa carries a **split license** — the Python wrapper, the upstream
engine code, and the bundled voice/linguistic data are licensed differently.

| Component | License |
|---|---|
| Python wrapper (`pyahotts_iparrahotsa/__init__.py`, packaging) | MIT |
| AhoTTS_Iparrahotsa engine sources (`src/`, compiled to `libhtts`) | GPL-3.0+ (Aholab / UPV-EHU) |
| Voice models & linguistic data (`data_tts/`, dictionary) | CC BY-SA 3.0 (Aholab / UPV-EHU) |

See `COPYRIGHT_and_LICENSE_code.txt` and `COPYRIGHT_and_LICENSE_voices.txt` in the
repository root for the authoritative terms. The repository's `LICENSE` file is
GPL-3.0. Because the distributed library links the GPL-3.0+ engine, redistribution
of the **binary** package is governed by the GPL-3.0+; the MIT wrapper code may be
reused under MIT.

## Credits

- **AhoTTS / AhoTTS_Iparrahotsa** — Aholab Signal Processing Laboratory, University
  of the Basque Country (UPV/EHU). Linguistic processing for (Northern) Basque, and
  the AhoCoder vocoder. Upstream:
  [aholab/AhoTTS_Iparrahotsa](https://github.com/aholab/AhoTTS_Iparrahotsa).
- The HTS acoustic engine derives from `hts_engine` (Nagoya Institute of Technology
  / Tokyo Institute of Technology), Modified BSD (GPL-compatible).
- The transcription patch and ctypes binding follow the approach used in
  [TigreGotico/pyAhoTTS](https://github.com/TigreGotico/pyAhoTTS), which builds on
  the [ekaitz-zarraga/AhoTTS](https://github.com/ekaitz-zarraga/AhoTTS) fork.
