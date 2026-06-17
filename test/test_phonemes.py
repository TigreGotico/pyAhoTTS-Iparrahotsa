"""Tests for AhoTTSIparrahotsa.get_phonemes (phonetic transcription, no synthesis).

AhoTTS_Iparrahotsa is the Northern (continental) Basque dialect engine: it
pronounces /h/, has the French rounded vowels (ü/ö), and a uvular r.
"""
import pytest
from pyahotts_iparrahotsa import AhoTTSIparrahotsa, AhoTTS, SAMPA_TO_IPA


@pytest.fixture(scope="module")
def tts():
    return AhoTTSIparrahotsa()


def test_class_alias():
    # API parity: AhoTTS is an alias of AhoTTSIparrahotsa
    assert AhoTTS is AhoTTSIparrahotsa


def test_basic_sampa(tts):
    # "Bai" -> b 'a j  (stress on the nucleus a)
    out = tts.get_phonemes("Bai.", lang="eu")
    assert out == [["b", "'a", "j"]]


def test_multiword_structure(tts):
    out = tts.get_phonemes("Bai eta ez.", lang="eu")
    assert len(out) == 3                      # one list of phones per word
    assert all(isinstance(w, list) for w in out)
    assert out[0] == ["b", "'a", "j"]


def test_h_is_pronounced(tts):
    # Northern dialect: word-initial <h> surfaces as the phone /h/, unlike the
    # southern V1 engine where it is silent.
    out = tts.get_phonemes("hau eta hori", lang="eu")
    assert out[0][0] == "h"     # hau -> h ...
    assert out[2][0] == "h"     # hori -> h ...


def test_french_vowel(tts):
    # Northern dialect has the French rounded vowel /y/ (written ü).
    out = tts.get_phonemes("bürü", lang="eu")
    assert "y" in out[0]


def test_uvular_r_ipa(tts):
    # SAMPA "R" (uvular r) maps to IPA "ʁ".
    out = tts.get_phonemes("bürü", lang="eu", ipa=True)
    assert "ʁ" in out[0]


def test_ipa_mapping(tts):
    sampa = tts.get_phonemes("Kaixo mundua!", lang="eu")
    ipa = tts.get_phonemes("Kaixo mundua!", lang="eu", ipa=True)
    assert len(sampa) == len(ipa) == 2
    # SAMPA "S" (kaixo's x) -> IPA "ʃ"
    assert "S" in sampa[0] and "ʃ" in ipa[0]
    # stress mark is preserved through the IPA conversion
    assert any(p.startswith("'") for w in ipa for p in w)


def test_empty_input(tts):
    assert tts.get_phonemes("", lang="eu") == []


def test_transcribe_then_synthesize_no_crash(tts):
    # regression: transcribing without ever synthesizing must not corrupt the
    # engine state (the HTS engine is only initialized in the synthesis path).
    tts.get_phonemes("Kaixo.", lang="eu")
    audio = tts.get_tts("Kaixo.", lang="eu")
    assert isinstance(audio, bytes) and len(audio) > 0


def test_sampa_to_ipa_table():
    assert SAMPA_TO_IPA["s`"] == "ʂ"
    assert SAMPA_TO_IPA["tS"] == "tʃ"
    assert SAMPA_TO_IPA["R"] == "ʁ"   # Northern uvular r
    assert SAMPA_TO_IPA["h"] == "h"
