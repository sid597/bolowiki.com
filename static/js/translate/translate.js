const LANGUAGES = {
  af: 'afrikaans',
  sq: 'albanian',
  am: 'amharic',
  ar: 'arabic',
  hy: 'armenian',
  az: 'azerbaijani',
  eu: 'basque',
  be: 'belarusian',
  bn: 'bengali',
  bs: 'bosnian',
  bg: 'bulgarian',
  ca: 'catalan',
  ceb: 'cebuano',
  ny: 'chichewa',
  'zh-cn': 'chinese (simplified)',
  'zh-tw': 'chinese (traditional)',
  co: 'corsican',
  hr: 'croatian',
  cs: 'czech',
  da: 'danish',
  nl: 'dutch',
  en: 'english',
  eo: 'esperanto',
  et: 'estonian',
  tl: 'filipino',
  fi: 'finnish',
  fr: 'french',
  fy: 'frisian',
  gl: 'galician',
  ka: 'georgian',
  de: 'german',
  el: 'greek',
  gu: 'gujarati',
  ht: 'haitian creole',
  ha: 'hausa',
  haw: 'hawaiian',
  iw: 'hebrew',
  he: 'hebrew',
  hi: 'hindi',
  hmn: 'hmong',
  hu: 'hungarian',
  is: 'icelandic',
  ig: 'igbo',
  id: 'indonesian',
  ga: 'irish',
  it: 'italian',
  ja: 'japanese',
  jw: 'javanese',
  kn: 'kannada',
  kk: 'kazakh',
  km: 'khmer',
  ko: 'korean',
  ku: 'kurdish (kurmanji)',
  ky: 'kyrgyz',
  lo: 'lao',
  la: 'latin',
  lv: 'latvian',
  lt: 'lithuanian',
  lb: 'luxembourgish',
  mk: 'macedonian',
  mg: 'malagasy',
  ms: 'malay',
  ml: 'malayalam',
  mt: 'maltese',
  mi: 'maori',
  mr: 'marathi',
  mn: 'mongolian',
  my: 'myanmar (burmese)',
  ne: 'nepali',
  no: 'norwegian',
  or: 'odia',
  ps: 'pashto',
  fa: 'persian',
  pl: 'polish',
  pt: 'portuguese',
  pa: 'punjabi',
  ro: 'romanian',
  ru: 'russian',
  sm: 'samoan',
  gd: 'scots gaelic',
  sr: 'serbian',
  st: 'sesotho',
  sn: 'shona',
  sd: 'sindhi',
  si: 'sinhala',
  sk: 'slovak',
  sl: 'slovenian',
  so: 'somali',
  es: 'spanish',
  su: 'sundanese',
  sw: 'swahili',
  sv: 'swedish',
  tg: 'tajik',
  ta: 'tamil',
  te: 'telugu',
  th: 'thai',
  tr: 'turkish',
  uk: 'ukrainian',
  ur: 'urdu',
  ug: 'uyghur',
  uz: 'uzbek',
  vi: 'vietnamese',
  cy: 'welsh',
  xh: 'xhosa',
  yi: 'yiddish',
  yo: 'yoruba',
  zu: 'zulu',
};
document.addEventListener('DOMContentLoaded', () => {
  const textareaElement = document.querySelector('.textareaElement');
  const textToTranslate = document.querySelector('#textToTranslate');
  const translateTextToSpeech = document.querySelector('#translateTextToSpeech');
  const translatedCardBody = document.querySelector('#translatedCardBody');
  const micIconModal = new bootstrap.Modal(document.querySelector('#micIconModal'));
  const micIcon = document.querySelector('#micIcon');
  const micIconCurrentStatus = document.querySelector('#micIconCurrentStatus');
  const micIconResult = document.querySelector('#micIconCurrentStatus');
  const voiceSelectDropdownButton = document.querySelector('#voiceSelectDropdownButton');
  const nameToSaveWith = document.querySelector('#nameToSaveWith');
  textareaElement.focus();

  // Voice select Dropdown button
  voiceSelectDropdownButton.textContent = 'Male  ';
  document.querySelector('#demolist').addEventListener('click', (e) => {
    console.log(e.target.textContent);
    voiceSelectDropdownButton.textContent = `${e.target.textContent}  `;
  });

  // Paste text as plain text in content editable
  document.querySelector('[contenteditable]').addEventListener('paste', (event) => {
    event.preventDefault();
    document.execCommand('inserttext', false, event.clipboardData.getData('text/plain'));
  });

  // Translte the text which is added

  textToTranslate.addEventListener('input', () => {
    const textToTranslateData = textToTranslate.innerHTML;
    // console.log(e);
    const request = new XMLHttpRequest();
    request.open('POST', '/translate/');
    request.onload = () => {
      const responseData = JSON.parse(request.responseText);
      // console.log(` RESPONSE DATA IS : ${responseData.translatedTextResponse}`);
      translatedCardBody.innerHTML = responseData.translatedTextResponse;
    };
    const postData = JSON.stringify({
      textToTranslate: textToTranslateData,
      srcLanguage: 'en',
      destLanguage: 'en',
    });
    // console.log(`Data to send for speech translation is ${postData}`)

    // console.log(data);
    request.setRequestHeader('Content-type', 'application/json');
    request.send(postData);
    // setTimeout(() => {
    //   request.send(data);
    // }, 200);
  });

  translateTextToSpeech.addEventListener('click', () => {
    const textToTranslateData = translatedCardBody.innerHTML;
    const request = new XMLHttpRequest();
    console.log('translateTextToSpeech clicked');
    request.open('POST', '/translateToSpeech/');
    request.onload = () => { };
    const postData = JSON.stringify({
      textToConvert: textToTranslateData,
      translateLanguage: 'en-GB',
      nameToSaveWith: nameToSaveWith.value.length !== 0 ? nameToSaveWith.value : 'sid_translate',
      voiceGender: voiceSelectDropdownButton.textContent,
    });
    request.setRequestHeader('Content-type', 'application/json');
    console.log(`Data to send for speech translation is ${postData}`);
    request.send(postData);
  });

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
      recognition.lang = 'en-US';

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
        micIconResult.innerHTML = trans;
        micIconQuery = trans;
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
