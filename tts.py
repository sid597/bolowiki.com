from google.cloud import texttospeech
from flask import current_app as app
import os


def GoogleTextToSpeech(textToConvert, nameToSaveWith):
    print(textToConvert)
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=textToConvert)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    saveDirectory = os.getcwd() + "/static/tts/"
    mediaLocation = saveDirectory + nameToSaveWith + ".mp3"
    app.logger.info("mediaLocation is going to be : %s "% mediaLocation)
    # The response's audio_content is binary.
    with open(mediaLocation, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        # print('Audio content written to file "output.mp3"')
    return mediaLocation


# Test this by $ python3 tts.py
# You should see a file helloworld.mp3 in you static directory

if __name__ == '__main__':
    GoogleTextToSpeech("art", 'helloworld')
