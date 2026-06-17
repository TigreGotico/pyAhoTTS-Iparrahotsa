# Building libhtts

The native library is built from the C/C++ sources in `src/` with CMake. A prebuilt
`libhtts_x86_64.so` is committed under `pyahotts_iparrahotsa/` and shipped in the
wheel; you only need to build when porting to a new architecture (e.g. `aarch64`) or
changing the engine.

## Build

```bash
mkdir build && cd build
cmake .. -DCMAKE_POLICY_VERSION_MINIMUM=3.5    # the flag is needed on CMake >= 4
make -j"$(nproc)"
# result: build/src/libhtts.so
```

Install it into the package for your architecture:

```bash
cp src/libhtts.so ../pyahotts_iparrahotsa/libhtts_$(uname -m).so
```

The top-level `CMakeLists.txt` builds `libhtts` from `src/CMakeLists.txt` and
installs the `data_tts` tree.

## Per-architecture notes

- `uname -m` selects the bundled library at runtime (`libhtts_<machine>.so`).
- **Only `x86_64` is committed.** `aarch64` (and others) must be built locally — run
  the build above on the target and commit `libhtts_aarch64.so`, or pass
  `AhoTTSIparrahotsa(lib_path=...)` at runtime.
- **When you change the C sources, rebuild *every* shipped architecture**, not just
  the host one — otherwise the other arch's bundled `.so` goes stale.

## Exported symbols

The build exposes the C API consumed by the Python binding — see
[Architecture](architecture.md): `create_tts`, `synthesize_text`,
`transcribe_text`, `free_samples`, `free_string`, `destroy_tts`.

## Regenerating phoneme golden fixtures

If an engine change legitimately alters transcriptions, regenerate the e2e golden
fixtures from a **verified** build and review the diff — see [Testing](testing.md).
