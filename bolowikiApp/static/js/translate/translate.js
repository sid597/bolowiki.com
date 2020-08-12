const speechToText = {
  'en-GB': 'en',
  'en-IN': 'en',
  'en-US': 'en',
  'hi-IN': 'hi',
  'bn-IN': 'bn',
  'gu-IN': 'gu',
  'kn-IN': 'kn',
  'ml-IN': 'ml',
  'ta-IN': 'ta',
  'te-IN': 'te',
};

document.addEventListener('DOMContentLoaded', () => {
  const textareaElement = document.querySelector('.textareaElement');
  const textToTranslate = document.querySelector('#textToTranslate');
  const translateTextToSpeech = document.querySelector('#translateTextToSpeech');
  const translatedTextResultBody = document.querySelector('#translatedCardBody');
  const micIconModal = new bootstrap.Modal(document.querySelector('#micIconModal'));
  const micIcon = document.querySelector('#micIcon');
  const micIconCurrentStatus = document.querySelector('#micIconCurrentStatus');
  const micIconResult = document.querySelector('#micIconCurrentStatus');
  const voiceSelectDropdownButton = document.querySelector('#voiceSelectDropdownButton');
  const translateLanguageFromDropdownButton = document.querySelector('#translateLanguageFromDropdownButton');
  const translateLanguageToDropdownButton = document.querySelector('#translateLanguageToDropdownButton');
  let translatedVoiceFiles = document.querySelector('#translatedVoiceFiles');

  let fromLanguage = 'en-US';
  let toLanguage = 'hi-IN';

  const nameToSaveWith = document.querySelector('#nameToSaveWith');
  const characterCount = document.querySelector('#characterCount');
  textareaElement.focus();

  // #############################################################################
  // ## Xhhr Requests                                                           ##
  // #############################################################################

  function requestToTextTranslate() {
    const textToTranslateData = textToTranslate.textContent.trim();
    if (textToTranslateData.length !== 0) {
      characterCount.innerHTML = textToTranslateData.length;
      const request = new XMLHttpRequest();
      request.open('POST', '/translate/toText/');
      request.onload = () => {
        const responseData = JSON.parse(request.responseText);
        translatedTextResultBody.innerHTML = responseData.translatedTextResponse;
      };
      const postData = JSON.stringify({
        textToTranslate: textToTranslateData,
        srcLanguage: speechToText[fromLanguage],
        destLanguage: speechToText[toLanguage],
      });
      console.log(`Data to send for speech translation is ${postData}`);
      request.setRequestHeader('Content-type', 'application/json');
      request.send(postData);
    } else {
      translatedTextResultBody.innerHTML = '';
    }
  }

  function requestToSpeechTranslate() {
    const textToTranslateData = translatedTextResultBody.innerHTML;
    const request = new XMLHttpRequest();
    console.log('translateTextToSpeech clicked');
    request.open('POST', '/translate/toSpeech/');
    request.onload = () => {
      const responseData = request.responseText;
      console.log(responseData);
      translatedVoiceFiles.innerHTML = `<audio id="audioControl" controls style="width: 100%;"><source src="${responseData}" type="audio/mpeg" />Your browser does not support the audio element.</audio>`;
    };
    const postData = JSON.stringify({
      textToConvert: textToTranslateData,
      translateLanguage: toLanguage,
      nameToSaveWith: nameToSaveWith.value.length !== 0 ? nameToSaveWith.value : 'sid_translate',
      voiceGender: voiceSelectDropdownButton.textContent,
    });
    request.setRequestHeader('Content-type', 'application/json');
    console.log(`Data to send for speech translation is ${postData}`);
    request.send(postData);
  }

  // #############################################################################
  // ## Dropdown buttons update text                                      ##
  // #############################################################################

  // Language translate from dropdown
  translateLanguageFromDropdownButton.textContent = 'English  ';
  document.querySelector('#translateLanguageFromList').addEventListener('click', (e) => {
    console.log(e.target.id);
    translateLanguageFromDropdownButton.textContent = `${e.target.textContent}  `;
    fromLanguage = e.target.id;
    requestToTextTranslate();
  });
  // Language translate to dropdown
  translateLanguageToDropdownButton.textContent = 'Hindi  ';
  document.querySelector('#translateLanguageToList').addEventListener('click', (e) => {
    console.log(e.target.id);
    translateLanguageToDropdownButton.textContent = `${e.target.textContent}  `;
    toLanguage = e.target.id;
    requestToTextTranslate();
  });
  // Voice gender dropdown
  voiceSelectDropdownButton.textContent = 'Male  ';
  document.querySelector('#demolist').addEventListener('click', (e) => {
    console.log(e.target.textContent);
    voiceSelectDropdownButton.textContent = `${e.target.textContent}  `;
    requestToSpeechTranslate();
  });

  // Paste text as plain text in content editable
  document.querySelector('[contenteditable]').addEventListener('paste', (event) => {
    event.preventDefault();
    document.execCommand('inserttext', false, event.clipboardData.getData('text/plain'));
  });

  // #############################################################################
  // ## Translate Text                                                          ##
  // #############################################################################

  // Translte the text which is added

  textToTranslate.addEventListener('input', requestToTextTranslate);

  // Translate text to speech

  translateTextToSpeech.addEventListener('click', requestToSpeechTranslate);

  // #############################################################################
  // ## Voice Input related Functions                                          ##
  // #############################################################################

  function showmicIconError(msg) {
    micIconCurrentStatus.className = 'alert alert-danger';
    micIconCurrentStatus.innerHTML = msg;
  }

  function showmicIconNormalMsg(msg) {
    micIconCurrentStatus.className = 'alert alert-light';
    micIconCurrentStatus.innerHTML = msg;
  }

  micIcon.addEventListener('click', () => {
    console.debug('micIcon clicked');
    // eslint-disable-next-line no-use-before-define
    listenToVoiceQuery();
  });

  async function listenToVoiceQuery() {
    const listening = false;
    console.debug('inside listen to voice query');
    if (!('webkitSpeechRecognition' in window)) {
      // TODO : Show a update to chrome message or completly hide this svg
    } else {
      const recognition = await new webkitSpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      // TODO : Change the language detection
      // recognition.lang = getmicIconLanguage();
      // recognition.lang = 'en-US';
      recognition.lang = speechToText[fromLanguage];

      console.debug(`recognition data is ${recognition}`);

      recognition.onstart = (e) => {
        showmicIconNormalMsg('Listening ...');
        console.debug(`recognition started ${e}`);
      };

      recognition.onresult = (e) => {
        console.debug(`recognition complete here is your result ${e.results[0][0].transcript}`);
        console.debug(`here is your event ${e}`);
        const trans = e.results[0][0].transcript;

        console.debug(`recognition complete here is your result ${trans}`);
        showmicIconNormalMsg(trans);
        console.log(`textToTranslate.innerHTML is : ${textToTranslate.innerHTML}`);
        textToTranslate.innerHTML = trans;
        requestToTextTranslate();
        return trans;
      };

      recognition.onerror = (e) => {
        if (e.error === 'no-speech') {
          showmicIconError('No speech was detected. You may need to adjust your  microphone');
        }
        if (e.error === 'audio-capture') {
          showmicIconError('No microphone was found. Ensure that a microphone is installed and that microphone settings</a> are configured correctly.');
        }
        if (e.error === 'not-allowed') {
          showmicIconError('Permission to use microphone was denied/blocked. To change,go to chrome://settings/contentExceptions#media-stream');
        }

        console.debug(` error occured : ${e.error}`);
      };

      recognition.onend = async () => {
        console.debug('ended');
        setTimeout(() => {
          showmicIconNormalMsg('Closing voice search');
          micIconModal.hide();
        }, 3000);
      };

      recognition.start();
    }
  }
});
