"""End-to-end tests for pyAhoTTS-Iparrahotsa.

This binding bundles a build of the AhoTTS_Iparrahotsa engine, the Northern
(continental) Basque dialect fork of AhoTTS V1 (aholab/AhoTTS_Iparrahotsa). The
bundled binary is the source of truth; these golden fixtures capture its
behavior, and these tests assert the binding keeps reproducing it across
rebuilds / platforms.

Fixtures: test/fixtures/iparrahotsa_golden_eu.json  (regenerate from a verified
build if the engine is ever updated).
"""
import json
import os

import pytest
from pyahotts_iparrahotsa import AhoTTSIparrahotsa

FIX = os.path.join(os.path.dirname(__file__), "fixtures", "iparrahotsa_golden_eu.json")


@pytest.fixture(scope="module")
def golden():
    with open(FIX, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def tts():
    return AhoTTSIparrahotsa()


def test_phonemes_match_golden(tts, golden):
    """get_phonemes must reproduce the bundled engine's transcription verbatim."""
    mism = []
    for text, expected in golden["phonemes"].items():
        got = tts.get_phonemes(text, lang="eu", ipa=True)
        if got != expected:
            mism.append((text, got, expected))
    assert not mism, "phoneme drift vs golden:\n" + "\n".join(
        f"  {t}\n    got={g}\n    exp={e}" for t, g, e in mism
    )


def test_synthesis_produces_audio(tts, golden):
    """get_tts must produce a non-trivial waveform for each sentence."""
    for text, min_bytes in golden["audio_min_bytes"].items():
        audio = tts.get_tts(text, lang="eu")
        assert isinstance(audio, bytes)
        assert len(audio) >= min_bytes, f"{text!r}: {len(audio)} < {min_bytes}"


def test_northern_h_pronounced(tts):
    """Regression: the Northern dialect pronounces word-initial /h/ as a phone."""
    out = tts.get_phonemes("Hau eta hori hemen daude.", lang="eu", ipa=True)
    # first phone of "Hau", "hori", "hemen" is /h/
    assert out[0][0] == "h"
    assert out[2][0] == "h"
    assert out[3][0] == "h"
