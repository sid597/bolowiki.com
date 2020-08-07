# External packages
from flask import request, session, jsonify, Blueprint

# Imports from local packages
from ..dbOperations import setUserRemainingLimit, GoogleTextToSpeech
from ..utils import login_required, remainingCharacterLimitNotZero
from .utils import _translate

translate_bp = Blueprint('translate_bp', __name__, url_prefix='/translate')


@translate_bp.route('/toText/', methods=["POST", "GET"])
@login_required
def translate():
    try:
        data = request.get_json()
        srcLanguage = data['srcLanguage']
        destLanguage = data['destLanguage']
        textToTranlate = data['textToTranslate']
         app.logger.info("Text to translate is : %s " % data)
        translatedText = _translate(
            textToTranlate,
            src=srcLanguage,
            dest=destLanguage)
         app.logger.info("Translated Text is %s " % translatedText)
        returnData = {'translatedTextResponse': translatedText,
                      'textWhichWasToBeTranslated': data['textToTranslate']}
        return jsonify(returnData)
    except:
        return "noob"
        # print(e)
         app.logger.error('Error in translate :%s' % e)


@translate_bp.route('/toSpeech/', methods=["POST", "GET"])
@login_required
@remainingCharacterLimitNotZero
def translateToSpeech():
    data = request.get_json()
     app.logger.info("Request to translate text to speech with data %s" % data)
    textToConvert = data['textToConvert']
    nameToSaveWith = data['nameToSaveWith']
    translateLanguage = data['translateLanguage']
    voiceGender = data['voiceGender']
    setUserRemainingLimit(session['username'], len(textToConvert))
    mediaLocation = GoogleTextToSpeech(textToConvert=textToConvert,
                                       nameToSaveWith=nameToSaveWith,
                                       translateLanguage=translateLanguage,
                                       voiceGender=voiceGender,
                                       convertType='translate'
                                       )
     app.logger.info("Text to speech request audio file location is : %s" % mediaLocation)
    return mediaLocation
