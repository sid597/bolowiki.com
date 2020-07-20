from googletrans import Translator
from flask import current_app as app


def _translate(text, dest='en', src='auto'):
    try:
        print(text, dest, src)
        translator = Translator()
        translatorResponse = translator.translate(text.strip(), dest, src)
        return translatorResponse.text
    except Exception as e:
        return e
        app.logger.error("Got an exception in _translate %s" % e)
 