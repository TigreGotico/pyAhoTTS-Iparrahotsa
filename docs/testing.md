# Testing

The suite lives in `test/` and runs with `pytest`:

```bash
pip install -e .[test]
pytest test/ -q
```

## What is tested

- **Unit** (`test/test_phonemes.py`) — `get_phonemes` output shape, SAMPA/IPA
  mapping, stress marks, empty input, the Northern features (/h/ pronounced, French
  ü, uvular r), and that transcribing then synthesizing does not corrupt engine
  state.
- **End-to-end** (`test/test_e2e.py`) — golden tests that pin the engine's behavior:
  - `test_phonemes_match_golden` — `get_phonemes` must reproduce the committed
    transcriptions verbatim.
  - `test_synthesis_produces_audio` — `get_tts` yields a non-trivial waveform.
  - `test_northern_h_pronounced` — word-initial /h/ surfaces as a phone.

## Golden fixtures

`test/fixtures/iparrahotsa_golden_eu.json` holds the expected text→phoneme pairs
(and audio size floors). Because this is a binding, these goldens are the contract
that the bundled native library keeps matching the engine across rebuilds and
architectures.

### Regenerating

Only regenerate when the engine legitimately changes, and **review the diff**:

```python
import json
from pyahotts_iparrahotsa import AhoTTSIparrahotsa
t = AhoTTSIparrahotsa()
corpus = [...]   # the sentences in the fixture
golden = {"phonemes": {s: t.get_phonemes(s, lang="eu", ipa=True) for s in corpus},
          "audio_min_bytes": {...}}
json.dump(golden, open("test/fixtures/iparrahotsa_golden_eu.json", "w"),
          ensure_ascii=False, indent=1)
```

## CI

Pull requests run the shared `OpenVoiceOS/gh-automations` reusable workflows:
build-tests (matrix Python versions), coverage, lint, license-check, pip-audit,
repo-health, and release-preview. The golden e2e tests run as part of build-tests,
so any drift of the bundled binding fails CI without needing to rebuild the engine
sources. CI runs on `x86_64`; the bundled `libhtts_x86_64.so` is exercised directly.
