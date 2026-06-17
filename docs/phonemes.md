# Phonemes (phonetic transcription)

`get_phonemes()` exposes the AhoTTS_Iparrahotsa linguistic front end as phonemes
without synthesizing audio, so it can be used as a grapheme-to-phoneme (G2P)
component on its own.

```python
from pyahotts_iparrahotsa import AhoTTSIparrahotsa, SAMPA_TO_IPA
tts = AhoTTSIparrahotsa()
tts.get_phonemes("Hau eta hori.", lang="eu", ipa=True)
# [['h', "'a", 'w'], ['e', 't', 'a'], ['h', "'o", 'ɾ', 'i']]
```

## Output format

- A **list of words**; each word is a **list of phone tokens** in order.
- **Lexical stress** is a leading `'` on the stressed nucleus (e.g. `"'o"`).
- Phones are **SAMPA** by default, or **IPA** when `ipa=True`.

## How it is produced

Internally the engine runs the full linguistic pipeline with the Northern dialect
(`PhTIparralde`) rules, and the transcription is read off the resolved utterance:

```
text
 → normalization (numbers, dates, abbreviations)
 → grapheme-to-phoneme (Iparralde rules: /h/ pronounced, ü→/y/, ö→/ø/, uvular r)
 → syllabification
 → lexical stress assignment
 → SAMPA phone names (canonical, from the engine's phone table)
```

The native side walks the utterance one word at a time, emitting the canonical
SAMPA for each phone (via the engine's `phone_tosampa` table), with `'` prefixed on
stressed nuclei. Pause/silence phones are dropped; word boundaries separate the
lists.

## Northern dialect phones

The Iparralde rules surface phones absent from (or different in) the Southern V1
engine:

| SAMPA | IPA | feature |
|---|---|---|
| `h` | h | /h/ is **pronounced** (word-initial `h` is silent in the South) |
| `y` | y | French rounded vowel, written **ü** |
| `Y` | ø | French rounded vowel, written **ö** (engine phone `PH_2`) |
| `R` | ʁ | **uvular** r (distinct from the tap `r` and trill `rr`) |
| `a~` `e~` `o~` | ã ẽ õ | nasal vowels |

## SAMPA → IPA

`ipa=True` maps each phone through `SAMPA_TO_IPA` (importable from
`pyahotts_iparrahotsa`). The base mapping matches the one shipped with the Aholab
phonemizer, extended with the Northern phones above:

| SAMPA | IPA | | SAMPA | IPA | | SAMPA | IPA |
|---|---|---|---|---|---|---|---|
| `g` | ɡ | | `tS` | tʃ | | `ts\`` | tʂ |
| `B` | β | | `D` | ð | | `G` | ɣ |
| `T` | θ | | `s\`` | ʂ | | `S` | ʃ |
| `J` | ɲ | | `L` | ʎ | | `r` | ɾ |
| `rr` | r | | `R` | ʁ | | `h` | h |
| `y` | y | | `Y` | ø | | `jj` | ʝ |

(Full table in `pyahotts_iparrahotsa.SAMPA_TO_IPA`.) Stress marks are preserved
across the conversion.

## Notes & limitations

- The transcription reflects the **bundled engine version**; behavior is pinned by
  the [golden tests](testing.md).
- AhoTTS is the *engine*; if you need a pure-Python, dependency-free G2P that
  matches a specific AhoTTS version, see the companion port project.
