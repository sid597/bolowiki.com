const voiceSearchCurrentStatus = document.querySelector('#voiceSearchCurrentStatus');
const voiceSearchResult = document.querySelector('#voiceSearchCurrentStatus');

function showVoiceSearchError(msg) {
  voiceSearchCurrentStatus.className = 'alert alert-danger';
  voiceSearchCurrentStatus.innerHTML = msg;
}

function showVoiceSearchNormalMsg(msg) {
  voiceSearchCurrentStatus.className = 'alert alert-light';
  voiceSearchCurrentStatus.innerHTML = msg;
}

export default async function listenToVoiceQuery(voiceSearchLanguage) {
  const listening = false;
  console.debug('inside listen to voice query');
  if (!('webkitSpeechRecognition' in window)) {
    // TODO : Show a update to chrome message or completly hide this svg
  } else {
    const recognition = await new webkitSpeechRecognition();
    // recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = voiceSearchLanguage;
    console.debug(recognition);

    recognition.onstart = (e) => {
      showVoiceSearchNormalMsg('Listening ...');
      console.debug(`recognition started here is the event ${e}`);
    };

    recognition.onresult = (e) => {
      console.debug(`recognition complete here is your result ${e.results[0][0].transcript}`);
      console.debug(`here is your event ${e}`);
      const trans = e.results[0][0].transcript;

      console.debug(`recognition complete here is your result ${trans}`);
      voiceSearchResult.innerHTML = trans;
      const voiceSearchQuery = trans;
      return voiceSearchQuery;
    };

    recognition.onerror = (e) => {
      if (e.error === 'no-speech') {
        showVoiceSearchError('No speech was detected. You may need to adjust your  microphone');
      }
      if (e.error === 'audio-capture') {
        showVoiceSearchError('No microphone was found. Ensure that a microphone is installed and that microphone settings</a> are configured correctly.');
      }
      if (e.error === 'not-allowed') {
        showVoiceSearchError('Permission to use microphone was denied/blocked. To change,go to chrome://settings/contentExceptions#media-stream');
      }

      console.debug(` error occured : ${e.error}`);
      return e
    };
    recognition.onend = async () => {
      console.debug('ended');
      showVoiceSearchNormalMsg('Closing voice search');
    };

    recognition.start();
  }
}
