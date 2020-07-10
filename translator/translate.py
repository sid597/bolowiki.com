from googletrans import Translator


def translate(text, dest='en', src='auto'):
    translator = Translator()
    translatorResponse = translator.translate(text, dest, src)
    return translatorResponse.text