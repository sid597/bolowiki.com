document.addEventListener('DOMContentLoaded', () => {

    var queryTopResultLink = null;
    var queryTopResultText = null;
    searchMainDiv = document.querySelector('#searchMainDiv')
    searchBox = document.querySelector('#searchInputBox')
    searchSuggestion = document.querySelector('#searchSuggestion')
    searchSuggestionList = document.querySelector('#searchSuggestionList')
    mainDiv = document.querySelector('#mainDiv')
    audioModalContentChildren = document.querySelector('#audioModalContent').children
    audioModalHeader = document.querySelector('#audioModalHeader')
    wikipediaAccordian = document.querySelector('#wikipediaAccordian')

    function showAudioModal(mediaLocation, articleText) {
        console.log(`media location is : ${mediaLocation} and articleText is ${articleText}`)
        audioModalBody = audioModalContentChildren[1]
        audioModalFooter = audioModalContentChildren[2]
        console.log(audioModalHeader, audioModalBody, audioModalFooter)
        audioModalHeader.innerHTML = `<audio controls style="width: 100%;"><source src="${mediaLocation}" type="audio/mpeg" />Your browser does not support the audio element.</audio>`
        audioModalBody.innerHTML = articleText
        audioModalFooter.innerHTML = `<a href="${queryTopResultLink}">${queryTopResultLink}</a>`
        var myModal = new bootstrap.Modal(document.getElementById('audioModal'))
        myModal.toggle()


    }
    function createNewAccordianCard(articleTitle, articleContents){
        let newCard = `<div class="card">
        <div class="card-header" id="${articleTitle}Wiki">
          <h2 class="mb-0">
            <button class="btn btn-link btn-block text-left" type="button" data-toggle="collapse" data-target="#${articleTitle}collapse" aria-expanded="true" aria-controls="collapseOne">
            ${articleTitle}
            </button>
          </h2>
        </div>
    
        <div id="${articleTitle}collapse" class="collapse show" aria-labelledby="${articleTitle}Wiki" data-parent="#wikipediaAccordian">
          <div class="card-body">
            ${articleContents}
          </div>
        </div>
      </div>`
      wikipediaAccordian.insertAdjacentHTML('afterbegin', newCard)
      console.log(newCard)
      
    }


    function getAudioFileData(functionToHandleTheResponse) {
        console.log('inside getAudioFileData')
        console.log(`function to handle response is ${functionToHandleTheResponse}`)
        request = new XMLHttpRequest();
        request.open('POST', '/converttospeech/')
        request.onload = () => {
            console.log(`request response text is ${request.responseText}`)
            const data = JSON.parse(request.responseText)
            console.log(`response data is ${data}`)
            if (functionToHandleTheResponse === "showAudioModal") {
                
                showAudioModal(data.mediaLocation, data.txt)
            }
            else if (functionToHandleTheResponse === 'createNewAccordian') {
                createNewAccordianCard(queryTopResultText, data.articleContents)
            }
            else if (functionToHandleTheResponse === 'both') {
                showAudioModal(data.mediaLocation, data.txt)
                createNewAccordianCard(queryTopResultText, data.articleContents)
            }
        }
        const data = new FormData();
        data.append('wikipediaLink', queryTopResultLink)
        console.log(`data is ${data}`)
        // request.setRequestHeader("Content-type", "application/json")
        request.send(data)

    }

    function defaultStyle() {
        console.log(`searchBox.value is ${searchBox.value}`)
        if (!searchBox.value) {
            searchMainDiv.style.borderRadius = "24px"
            searchMainDiv.style.boxShadow = 'none'
            searchMainDiv.style.borderColor = "rgb(223, 225, 229)"
            searchSuggestion.style.display = 'none'
        }
        else {
            searchMainDiv.style.borderRadius = "24px"
            searchMainDiv.style.boxShadow = "0 1px 6px 0 rgba(32,33,36,0.28)";
            searchMainDiv.style.borderColor = "rgba(223,225,229,0)";
            searchSuggestion.style.display = 'none'
        }
    }

    function focusedStyle() {
        if (searchBox.value) {
            searchMainDiv.style.borderBottomRightRadius = 0
            searchMainDiv.style.borderBottomLeftRadius = 0
            searchMainDiv.style.boxShadow = "0 1px 6px 0 rgba(32,33,36,0.28)"
            searchMainDiv.style.borderColor = "rgba(223,225,229,0)"
            searchSuggestion.style.display = 'flex'
        }
        else {
            searchMainDiv.style.borderRadius = "24px"
            searchMainDiv.style.boxShadow = "0 1px 6px 0 rgba(32,33,36,0.28)";
            searchMainDiv.style.borderColor = "rgba(223,225,229,0)";
            searchSuggestion.style.display = 'none'
        }
    }

    function getMatchString(s1, s2) {
        l1 = s1.toLowerCase()
        l2 = s2.toLowerCase()
        // console.log(s1,'---', s2)
        if (l1 === l2) { return s2; }

        res = ""
        for (x = 0; x <= s1.length; x++) {
            if (l1[x] == l2[x]) {
                res += s2[x];
            }
            else {
                break;
            }
        }
        return res;
    }

    function getWikipediaresponse(searchText) {

        const wikiLink = `https://en.wikipedia.org/w/api.php?action=opensearch&format=json&origin=*&formatversion=2&search=${searchText}&namespace=0&limit=10`

        const request = new XMLHttpRequest()
        request.open('GET', wikiLink);

        request.onload = () => {
            const data = JSON.parse(request.responseText);
            // console.log(data)
            var l = ['<ul class="list-group list-group-flush">'];
            // console.log(l)

            for (var i = 0; i < 10; i++) {
                textLink = data[3][i]
                text = data[1][i]
                if (text) {
                    matchText = getMatchString(searchText, text)
                    unmatchedText = text.slice(matchText.length, text.length)
                    // console.log(`${searchText}-->`, matchText, '||', unmatchedText)
                    if (matchText) {
                        if (unmatchedText) {
                            l.push(`<a class="resultLink" href=${textLink}> <li class="listitem"><span style="font-weight:600">${matchText}</span><span>${unmatchedText}</span></li></a>`)
                        }
                        else {
                            l.push(`<a class="resultLink" href=${textLink}> <li class="listitem"><b>${matchText}</b></li></a>`)
                        }
                    }
                    // document.querySelector('.suggestions').append(ii)
                }
            };
            l.push('</ul>')
            // console.log(l.join(''))
            searchSuggestionList.innerHTML = l.join('')
            // document.querySelector('.suggestions').innerHTML = l.join('')
            queryTopResultLink = data[3][0]
            // console.log(queryTopResultLink)
            queryTopResultText = data[1][0]
            return l.join('');


        };
        request.send(null)
        // console.log(request.responseText)
    }

    function mouseoverMainDiv() {
        searchMainDiv.style.boxShadow = "0 1px 6px 0 rgba(32,33,36,0.28)";
        searchMainDiv.style.borderColor = "rgba(223,225,229,0)";
    }

    mainDiv.addEventListener('mouseover', e => {
        mouseoverMainDiv()
    });

    searchBox.addEventListener('keyup', e => {
       
        if (e.key === 'Enter') {
            console.log("keyup event with enter key")
            defaultStyle()
            getAudioFileData("both",)
        }
        else {
            focusedStyle()
            searchQuery = (e.target.value).trim()
            if (searchQuery) {
                getWikipediaresponse(searchQuery)
            }
        }
    });

    

    document.addEventListener('click', e => {
        clickVal = mainDiv.contains(e.target)
        if (clickVal) {
            focusedStyle()
        }
        else {
            defaultStyle()
        }
    });
});