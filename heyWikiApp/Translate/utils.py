# Local packages
from googletrans import Translator


def _translate(text, dest='en', src='auto'):
    try:
        print(text, dest, src)
        translator = Translator()
        translatorResponse = translator.translate(text.strip(), dest, src)
        return translatorResponse.text
    except Exception as e:
        return e
