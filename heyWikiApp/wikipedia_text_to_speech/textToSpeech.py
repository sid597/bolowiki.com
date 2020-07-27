import os
from flask import current_app as app
from google.cloud import texttospeech


def GoogleTextToSpeech(textToConvert, nameToSaveWith, translateLanguage, voiceGender, convertType):
    ssmlVoiceGender = {
        'MALE': texttospeech.SsmlVoiceGender.MALE,
        'FEMALE': texttospeech.SsmlVoiceGender.FEMALE
    }

    languageSettings = {'hi':
                        {
                            'language_code': 'hi-IN',
                            'ssml_gender': ssmlVoiceGender[voiceGender],
                            'speaking_rate': 0.85
                        },

                        'en': {
                            'language_code': 'en-US',
                            'ssml_gender': ssmlVoiceGender[voiceGender],
                            'speaking_rate': 1
                        },
                        'en-IN': {
                            'language_code': 'en-IN',
                            'ssml_gender': ssmlVoiceGender[voiceGender],
                            'speaking_rate': 1
                        },
                        'en-GB': {
                            'language_code': 'en-GB',
                            'name' : "en-GB-Wavenet-D",
                            'ssml_gender': ssmlVoiceGender[voiceGender],
                            'speaking_rate': 1
                        },
                        }
    app.logger.info("Inside GoogleTextToSpeech")
    # print(textToConvert)
    app.logger.info(
        'Text which is to be converted to speech is %s' % textToConvert)

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=textToConvert)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code=languageSettings[translateLanguage]['language_code'],
        ssml_gender=languageSettings[translateLanguage]['ssml_gender']
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=languageSettings[translateLanguage]['speaking_rate']
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    if convertType == 'wiki':
        saveDirectory = os.getcwd() + "/static/textToSpeech/"
    else:
        # TODO: change the location
        saveDirectory = os.getcwd() + "/static/translate/"
    mediaLocation = saveDirectory + nameToSaveWith + ".mp3"
    app.logger.info("mediaLocation is going to be : %s " % mediaLocation)
    # The response's audio_content is binary.
    with open(mediaLocation, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        # print('Audio content written to file "output.mp3"')
    return "../static/textToSpeech/" + nameToSaveWith

