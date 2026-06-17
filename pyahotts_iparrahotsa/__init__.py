import ctypes
import platform
import wave
from os.path import dirname, isfile
from typing import Optional

import numpy as np


# AhoTTS SAMPA -> IPA. Matches the mapping shipped with the Aholab phonemizer
# (https://huggingface.co/spaces/arrandi/phonemizer-eus-esp). Used by
# AhoTTSIparrahotsa.get_phonemes(ipa=True).
#
# AhoTTS_Iparrahotsa is the Northern (continental) Basque dialect engine, so the
# Northern features show up here: /h/ ("h") is pronounced, the French rounded
# vowels /y/ ("y" -> y) and /ø/ ("2" -> ø) appear, and the rhotic is uvular
# ("rr" -> ʁ in Northern Basque, kept as "r" for parity with the southern map).
SAMPA_TO_IPA = {
    "p": "p", "b": "b", "t": "t", "c": "c", "d": "d", "k": "k", "g": "ɡ",
    "tS": "tʃ", "ts": "ts", "ts`": "tʂ", "gj": "ɟ", "jj": "ʝ", "f": "f",
    "B": "β", "T": "θ", "D": "ð", "s": "s", "s`": "ʂ", "S": "ʃ", "x": "x",
    "G": "ɣ", "m": "m", "n": "n", "J": "ɲ", "l": "l", "L": "ʎ", "r": "ɾ",
    "rr": "r", "j": "j", "w": "w", "i": "i", "e": "e", "a": "a", "o": "o",
    "u": "u", "y": "y", "Z": "ʒ", "h": "h", "ph": "pʰ", "kh": "kʰ", "th": "tʰ",
    # Northern (Iparralde) dialect phones, as emitted by phone_tosampa:
    "R": "ʁ",    # uvular r (Northern Basque), distinct from "r"/"rr"
    "Y": "ø",    # PH_2: French rounded vowel /ø/ ("eu"/ö)
    "v": "v", "z": "z", "N": "ŋ",
    "a~": "ã", "e~": "ẽ", "o~": "õ",  # nasal vowels
}


# AhoTTS_Iparrahotsa is Basque-only; lang is always "eu" internally.
DEFAULT_LANG = "eu"


class AhoTTSIparrahotsa:
    """
    Python bindings for the AhoTTS_Iparrahotsa engine: the Northern (continental)
    Basque dialect text-to-speech system from Aholab (UPV/EHU).

    Unlike the Southern V1 engine wrapped by pyAhoTTS, this one is Basque-only,
    pronounces /h/, has the French vowels (ü/ö) and uvular r of Northern Basque,
    and expects its input text in WINDOWS-1252 (cp1252).

    Attributes:
        data_path (bytes): Path to the directory containing TTS data.
        tts (ctypes.c_void_p): The TTS instance created by the shared library.
        current_lang (Optional[str]): The current language used by the TTS instance.
    """

    # Text encoding expected by the engine. The Northern dialect README states the
    # input encoding is WINDOWS-1252 (not ISO-8859-15 as in the southern engine).
    ENCODING = "cp1252"

    def __init__(self, lib_path: Optional[str] = None,
                 data_path: str = f"{dirname(__file__)}/data_tts"):
        """
        Initializes the engine, loading the shared library and setting the data path.

        Args:
            lib_path (Optional[str]): Path to the shared library (.so). If None, the
                library is determined based on the platform (libhtts_<machine>.so).
            data_path (str): Path to the directory containing TTS data
                (default is `./data_tts`).
        """
        if lib_path is None:
            lib_path = f"{dirname(__file__)}/libhtts_{platform.machine()}.so"
            if not isfile(lib_path):
                raise FileNotFoundError(
                    "Please compile and pass the shared library via 'lib_path' argument")

        self.data_path = data_path.encode("utf-8")
        self._load_library(lib_path)
        self.tts = None
        self.current_lang = None

    def _load_library(self, lib_path: str):
        """
        Loads the shared library and sets up the function prototypes.
        """
        self.lib = ctypes.cdll.LoadLibrary(lib_path)

        # Setup argument types and return types for library functions
        self.lib.create_tts.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self.lib.create_tts.restype = ctypes.c_void_p

        self.lib.synthesize_text.argtypes = [
            ctypes.c_void_p,
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.POINTER(ctypes.POINTER(ctypes.c_short)),
            ctypes.POINTER(ctypes.c_int),
        ]
        self.lib.synthesize_text.restype = ctypes.c_int

        self.lib.free_samples.argtypes = [ctypes.POINTER(ctypes.c_short)]
        self.lib.destroy_tts.argtypes = [ctypes.c_void_p]

        # Phonetic transcription: char* transcribe_text(tts, text, data_path, lang)
        self.lib.transcribe_text.argtypes = [
            ctypes.c_void_p,
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_char_p,
        ]
        self.lib.transcribe_text.restype = ctypes.c_void_p
        self.lib.free_string.argtypes = [ctypes.c_void_p]

    def _recreate_tts(self, lang: str):
        """
        Recreates the TTS instance for a given language.

        Raises:
            RuntimeError: If the TTS instance could not be created.
        """
        if self.tts is not None:
            self.lib.destroy_tts(self.tts)
        self.tts = self.lib.create_tts(self.data_path, lang.encode("utf-8"))
        if not self.tts:
            raise RuntimeError(f"Failed to create TTS instance for language: {lang}")
        self.current_lang = lang

    def get_tts(self, text: str, lang: str = DEFAULT_LANG,
                wav_path: Optional[str] = None) -> bytes:
        """
        Generates speech from text and returns it as raw 16-bit PCM bytes,
        optionally saving it to a WAV file.

        Args:
            text (str): The text to be converted to speech.
            lang (str): Language code (only 'eu', Northern Basque, is supported).
            wav_path (Optional[str]): If provided, saves the generated audio as a
                WAV file at this path.

        Returns:
            bytes: The generated audio (16-bit mono @ 16kHz), or b"" on failure.
        """
        # Northern engine expects WINDOWS-1252 input.
        text_bytes = text.encode(self.ENCODING, "replace")
        lang_bytes = lang.encode("utf-8")

        if self.tts is None or self.current_lang != lang:
            self._recreate_tts(lang)

        samples_ptr = ctypes.POINTER(ctypes.c_short)()
        length = ctypes.c_int()

        success = self.lib.synthesize_text(
            self.tts, text_bytes, self.data_path, lang_bytes,
            ctypes.byref(samples_ptr), ctypes.byref(length)
        )

        if not success or length.value <= 0:
            return b""

        samples_np = np.ctypeslib.as_array(samples_ptr, shape=(length.value,))
        samples_bytes = samples_np.astype(np.int16).tobytes()

        if wav_path:
            with wave.open(wav_path, "wb") as wf:
                wf.setnchannels(1)  # Mono
                wf.setsampwidth(2)  # 2 bytes per sample (16-bit)
                wf.setframerate(16000)  # 16kHz
                wf.writeframes(samples_bytes)

        self.lib.free_samples(samples_ptr)
        return samples_bytes

    def get_phonemes(self, text: str, lang: str = DEFAULT_LANG, ipa: bool = False):
        """
        Phonetically transcribe text to SAMPA (or IPA) without synthesizing audio.

        Runs the full AhoTTS linguistic pipeline (number/date/abbreviation
        normalization, grapheme-to-phoneme, syllabification, lexical stress) with
        the Northern dialect rules (PhTIparralde) enabled, so /h/ surfaces as a
        phone and the French vowels appear.

        Args:
            text (str): Input text.
            lang (str): Language code (only 'eu' is supported).
            ipa (bool): If True, map SAMPA phones to IPA via SAMPA_TO_IPA.

        Returns:
            list[list[str]]: One list of phones per word, in order. Lexical stress
            is carried as a leading "'" on the stressed phone. Empty list on failure.
        """
        # Northern engine expects WINDOWS-1252 input.
        text_bytes = text.encode(self.ENCODING, "replace")
        lang_bytes = lang.encode("utf-8")

        if self.tts is None or self.current_lang != lang:
            self._recreate_tts(lang)

        ptr = self.lib.transcribe_text(self.tts, text_bytes, self.data_path, lang_bytes)
        if not ptr:
            return []
        raw = ctypes.cast(ptr, ctypes.c_char_p).value.decode(self.ENCODING)
        self.lib.free_string(ptr)

        words = []
        for line in raw.split("\n"):
            line = line.strip()
            if not line:
                continue
            phones = line.split(" ")
            if ipa:
                phones = [self._sampa_to_ipa(p) for p in phones]
            words.append(phones)
        return words

    @staticmethod
    def _sampa_to_ipa(phone: str) -> str:
        """Map a single (optionally stress-marked) SAMPA phone to IPA."""
        stress = ""
        if phone.startswith("'"):
            stress, phone = "'", phone[1:]
        return stress + SAMPA_TO_IPA.get(phone, phone)

    def __del__(self):
        """Destroy the TTS instance when the object is garbage-collected."""
        if hasattr(self, 'tts') and self.tts:
            self.lib.destroy_tts(self.tts)
            self.tts = None


# API parity with pyAhoTTS: the class is also exported as `AhoTTS`.
AhoTTS = AhoTTSIparrahotsa


if __name__ == "__main__":
    tts = AhoTTSIparrahotsa()

    audio_bytes = tts.get_tts("Kaixo, ongi etorri!", lang="eu",
                              wav_path="../output_eu.wav")
    if audio_bytes:
        print(f"Generated {len(audio_bytes)} bytes of audio.")

    print(tts.get_phonemes("Kaixo, ongi etorri!", lang="eu", ipa=True))
