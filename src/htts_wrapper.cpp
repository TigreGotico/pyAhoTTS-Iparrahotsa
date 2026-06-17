#include "htts.hpp"
#include <cstring>
#include <cstdlib>
#include <string>

extern "C" {

// AhoTTS_Iparrahotsa is the Northern (continental) Basque dialect engine.
// It is Basque-only (lang "eu"); there is no Spanish module here. Unlike the
// Southern V1 engine, it applies the Iparralde transcription rules (PhTIparralde),
// which pronounce /h/ and use the French vowels and uvular r of Northern Basque.
HTTS* create_tts(const char* data_path, const char* lang) {
    HTTS* tts = new HTTS;
    tts->set("PthModel", "Pth1");
    tts->set("Method", "HTS");
    tts->set("Lang", lang);  // always "eu" for this engine

    char dic_path[1024];
    sprintf(dic_path, "%s/dicts/%s_dicc", data_path, lang);
    tts->set("HDicDBName", dic_path);

    if (!tts->create()) {
        delete tts;
        return nullptr;
    }

    char voice_path[1024];
    sprintf(voice_path, "%s/voices/aholab_%s_female/", data_path, lang);
    tts->set("voice_path", voice_path);
    tts->set("vp", "yes");
    // Northern dialect transcription rules (pronounce /h/, French vowels, uvular r)
    tts->set("PhTIparralde", "yes");

    return tts;
}

int synthesize_text(HTTS* tts, const char* text, const char* data_path, const char* lang, short** out_samples, int* out_len) {
    if (!tts) return 0;

    if (tts->input_multilingual(text, lang, data_path, false)) {
        int len = tts->output_multilingual(lang, out_samples);
        if (out_len) *out_len = len;
        return len > 0;
    }
    return 0;
}

// Phonetic (SAMPA) transcription of `text`. Runs the full linguistic pipeline
// (normalization, G2P, syllabification, stress) but no acoustic synthesis, and
// returns a newly-allocated string: one word per line, phones space-separated,
// lexical stress as a leading "'". Caller frees with free_string().
// Returns NULL on failure / empty result.
char* transcribe_text(HTTS* tts, const char* text, const char* data_path, const char* lang) {
    if (!tts) return nullptr;
    if (!tts->input_multilingual(text, lang, data_path, false)) return nullptr;

    std::string acc;
    char* seg;
    while ((seg = tts->transcribe_next(lang)) != nullptr) {
        if (seg[0]) {                       // skip flush/empty sentinels
            if (!acc.empty()) acc += "\n";
            acc += seg;
        }
        free(seg);
    }
    if (acc.empty()) return nullptr;
    return strdup(acc.c_str());
}

void free_string(char* s) {
    if (s) {
        free(s);
    }
}

void free_samples(short* samples) {
    if (samples) {
        free(samples);
    }
}

void destroy_tts(HTTS* tts) {
    delete tts;
}

}
