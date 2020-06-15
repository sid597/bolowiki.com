document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('form').onsubmit = () => {
        const request = new XMLHttpRequest()
        const wikiLink = document.querySelector('#tts').value
        console.log("Text in text area is : %s" % wikiLink)
        request.open('POST', '/converttospeech/')

        // Append a new audio tag to the div its format will be like:
        // <audio controls>
        //    <source id="audio" src="/path-to-media-location" type="audio/mpeg">
        //     Your browser does not support the audio element.
        // </audio>


        request.onload = () => {
            const data = JSON.parse(request.responseText)
            console.log(data.txt)
            console.log(data.success)


            if (data.success) {
                const loc = data.mediaLocation
                s = `<div><audio controls><source id="audio" src=${loc} type="audio/mpeg"> Your browser does not support the audio element.</audio></div>`

                console.log(loc)
                console.log(s)
                console.log(data.txt)
                document.querySelector('#display').innerHTML = data.txt
                d1 = document.querySelector('#audiop')
                d1.insertAdjacentHTML('afterend', s)
            }
            else {
                s = `<div class="alert alert-danger" role="alert">
                ${data.txt}
              </div>`
                console.log(data)
                document.querySelector('#display').innerHTML = s
            }
        }
        const data = new FormData();

        data.append('textforspeech', wikiLink);

        request.send(data);
        return false;
    };
});
