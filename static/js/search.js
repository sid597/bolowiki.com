document.addEventListener('DOMContentLoaded', () => {

    searchMainDiv = document.querySelector('#searchMainDiv')
    searchBox = document.querySelector('#searchInputBox')
    searchSuggestion = document.querySelector('#searchSuggestion')
    searchSuggestionList =document.querySelector('#searchSuggestionList')
    mainDiv = document.querySelector('#mainDiv')


    function defaultStyle() {
        console.log(searchBox.value)
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
        focusedStyle()
        searchQuery = (e.target.value).trim()
        if (searchQuery) { 
            getWikipediaresponse(searchQuery) 
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

