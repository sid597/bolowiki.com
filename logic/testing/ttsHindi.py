from google.cloud import texttospeech
from wikipediaTesting import *


def GoogleTextToSpeech(textToConvert, nameToSaveWith):
    # print(textToConvert)

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=textToConvert)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="hi-In", ssml_gender=texttospeech.SsmlVoiceGender.MALE
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=0.85
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    saveDirectory = "/home/sid597/Don-tReadListen/" + "/static/tts/"
    mediaLocation = saveDirectory + nameToSaveWith + ".mp3"

    # The response's audio_content is binary.
    with open(mediaLocation, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        # print('Audio content written to file "output.mp3"')
    return "../static/tts/" + nameToSaveWith


# Test this by $ python3 tts.py
# You should see a file helloworld.mp3 in you static directory

if __name__ == '__main__':
    hindiUrl = "https://hi.wikipedia.org/wiki/%E0%A4%B9%E0%A4%B0%E0%A4%BF%E0%A4%AF%E0%A4%BE%E0%A4%A3%E0%A4%BE"
    article = testThisUrl(hindiUrl)
    GoogleTextToSpeech(article, 'hindi')
