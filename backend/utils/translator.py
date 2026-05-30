from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory


DetectorFactory.seed = 0


class Translator:
    def __init__(self):
        self.supported_languages = {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "ru": "Russian",
            "zh-CN": "Chinese",
            "ja": "Japanese",
            "ko": "Korean",
            "ar": "Arabic",
            "hi": "Hindi",
            "te": "Telugu",
            "ta": "Tamil",
            "kn": "Kannada",
            "ml": "Malayalam",
            "bn": "Bengali",
            "mr": "Marathi",
            "gu": "Gujarati",
            "pa": "Punjabi",
            "ur": "Urdu",
            "tr": "Turkish",
            "nl": "Dutch",
            "pl": "Polish",
            "vi": "Vietnamese",
            "th": "Thai",
            "id": "Indonesian",
            "sv": "Swedish",
            "el": "Greek",
            "he": "Hebrew",
        }

    def detect_language(self, text):
        try:
            if not text or not text.strip():
                return "en"

            return detect(text)
        except Exception:
            return "en"

    def translate(self, text, target_lang="en", source_lang="auto"):
        try:
            if not text or source_lang == target_lang:
                return text

            translated = GoogleTranslator(
                source=source_lang,
                target=target_lang,
            ).translate(text)

            return translated
        except Exception as e:
            print(f"Translation error: {e}")
            return text

    def translate_to_english(self, text):
        source = self.detect_language(text)

        if source == "en":
            return text, "en"

        translated = self.translate(
            text,
            target_lang="en",
            source_lang=source,
        )

        return translated, source

    def translate_from_english(self, text, target_lang):
        if target_lang == "en":
            return text

        return self.translate(
            text,
            target_lang=target_lang,
            source_lang="en",
        )

    def get_language_name(self, code):
        return self.supported_languages.get(code, code.upper())