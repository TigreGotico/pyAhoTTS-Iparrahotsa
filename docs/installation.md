# Installation

## From PyPI

```bash
pip install pyahotts_iparrahotsa
```

The wheel bundles the native library (`libhtts`) for Linux `x86_64`, plus all voice
and dictionary data, so nothing needs to be compiled. The only runtime dependency is
`numpy`.

```python
from pyahotts_iparrahotsa import AhoTTSIparrahotsa
tts = AhoTTSIparrahotsa()             # loads the bundled libhtts for your arch
tts.get_tts("Kaixo!", lang="eu", wav_path="out.wav")
```

## From source

```bash
git clone https://github.com/TigreGotico/pyAhoTTS-Iparrahotsa
cd pyAhoTTS-Iparrahotsa
pip install .            # or: pip install -e .[test]   to run the test suite
```

## Building the native library

The prebuilt `libhtts_x86_64.so` lives in `pyahotts_iparrahotsa/`. To rebuild it from
the C/C++ sources in `src/`, run:

```bash
mkdir build && cd build
cmake .. -DCMAKE_POLICY_VERSION_MINIMUM=3.5    # needed on CMake >= 4
make -j"$(nproc)"
cp src/libhtts.so ../pyahotts_iparrahotsa/libhtts_<arch>.so
```

For an architecture without a bundled `.so` (for example `aarch64`), build it and
pass the path explicitly:

```python
tts = AhoTTSIparrahotsa(lib_path="/path/to/libhtts.so")
```

See [Building libhtts](building.md) for details on the build and the exported C API.

## Supported platforms

Linux `x86_64` ships prebuilt. `aarch64`, macOS, and Windows are not bundled. Build
`libhtts` for your platform and pass `lib_path`.

---
[Home](README.md) · [Usage →](usage.md)
