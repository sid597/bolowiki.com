document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('form').onsubmit = () => {
    const request = new XMLHttpRequest();
    const wikiLink = document.querySelector('#tts').value;
    console.debug('Text in text area is : %s' % wikiLink);
    request.open('POST', '/converttospeech/');

    // Append a new audio tag to the div its format will be like:
    // <audio controls>
    //    <source id="audio" src="/path-to-media-location" type="audio/mpeg">
    //     Your browser does not support the audio element.
    // </audio>

    request.onload = () => {
      const data = JSON.parse(request.responseText);
      console.debug(data.txt);
      console.debug(data.success);

      if (data.success) {
        const loc = data.mediaLocation;
        const s = `<div><audio controls><source id="audio" src=${loc} type="audio/mpeg"> Your browser does not support the audio element.</audio></div>`;

        console.debug(loc);
        console.debug(s);
        console.debug(data.txt);
        document.querySelector('#display').innerHTML = data.txt;
        const d1 = document.querySelector('#audiop');
        d1.insertAdjacentHTML('afterend', s);
      } else {
        const s = `<div class="alert alert-danger" role="alert">
                ${data.txt}
              </div>`;
        console.debug(data);
        document.querySelector('#display').innerHTML = s;
      }
    };
    const data = new FormData();

    data.append('wikipediaLink', wikiLink);

    request.send(data);
    return false;
  };
});
