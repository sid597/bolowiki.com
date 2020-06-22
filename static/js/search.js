document.addEventListener('DOMContentLoaded', () => {
  const queryTopResultLink = null;
  const queryTopResultText = null;
  const searchMainDiv = document.querySelector('#searchMainDiv');
  const searchBox = document.querySelector('#searchInputBox');
  const searchSuggestion = document.querySelector('#searchSuggestion');
  const searchSuggestionList = document.querySelector('#searchSuggestionList');
  const mainDiv = document.querySelector('#mainDiv');
  const audioModalContentChildren = document.querySelector('#audioModalContent').children;
  const audioModalHeader = document.querySelector('#audioModalHeader');
  const wikipediaAccordian = document.querySelector('#wikipediaAccordian');

  function createWikipediaContentLinks(wikiContentText) {
    const wikiContentTextJoined = wikiContentText.split(' ').join('_');
    const fullWikiLink = `${queryTopResultLink}#${wikiContentTextJoined}`;
    // console.debug(fullWikiLink)

    return fullWikiLink;
  }

  function makeArticlesList(articleText) {
    const l = ['Article Contents :', '<ul>'];
    l.push(`<li class="accordianCardLinks" 
        id='${createWikipediaContentLinks('')}'
        >Introduction
        </li>`);
    for (let i = 1; i < articleText.length; i += 1) {
      l.push(`<li class="accordianCardLinks" 
            id='${createWikipediaContentLinks(articleText[i])}'
            >${articleText[i]}
            </li>`);
    }
    l.push('</ul>');
    return l.join('');
  }

  function showAudioModal(mediaLocation, articleText, articleWikiLink) {
    // console.debug(`media location is : ${mediaLocation} and articleText is ${articleText}`)
    const audioModalBody = audioModalContentChildren[1];
    const audioModalFooter = audioModalContentChildren[2];
    // console.debug(audioModalHeader, audioModalBody, audioModalFooter)
    audioModalHeader.innerHTML = `<audio controls style="width: 100%;"><source src="${mediaLocation}" type="audio/mpeg" />Your browser does not support the audio element.</audio>`;
    audioModalBody.innerHTML = articleText;
    audioModalFooter.innerHTML = `<a href="${articleWikiLink}">${articleWikiLink}</a>`;
    const myModal = new bootstrap.Modal(document.getElementById('audioModal'));
    myModal.toggle();
  }

  function createNewAccordianCard(articleTitle, articleContents) {
    const articleContentsList = makeArticlesList(articleContents);
    const articleTitleForIds = articleTitle.split(' ').join('');
    const newCard = `<div class="card">
        <div class="card-header" id="${articleTitleForIds}Wiki">
          <h2 class="mb-0">
            <button class="btn btn-link btn-block text-left" type="button" data-toggle="collapse" data-target="#${articleTitleForIds}collapse" aria-expanded="true" aria-controls="collapseOne">
            ${articleTitle}
            </button>
          </h2>
        </div>
    
        <div id="${articleTitleForIds}collapse" class="collapse show" aria-labelledby="${articleTitleForIds}Wiki" data-parent="#wikipediaAccordian">
          <div class="card-body">
            ${articleContentsList}
          </div>
        </div>
      </div>`;
    wikipediaAccordian.insertAdjacentHTML('afterbegin', newCard);
    //   console.debug(newCard)
  }

  function getAudioFileData(functionToHandleTheResponse, articleWikiLink) {
    console.debug('inside getAudioFileData');
    console.debug(`function to handle response is ${functionToHandleTheResponse}`);
    const request = new XMLHttpRequest();
    request.open('POST', '/converttospeech/');
    request.onload = () => {
      console.debug(`request response text is ${request.responseText}`);
      const data = JSON.parse(request.responseText);
      console.debug(`response data is ${data}`);
      if (functionToHandleTheResponse === 'showAudioModal') {
        showAudioModal(data.mediaLocation, data.txt, articleWikiLink);
      } else if (functionToHandleTheResponse === 'createNewAccordian') {
        createNewAccordianCard(queryTopResultText, data.articleContents);
      } else if (functionToHandleTheResponse === 'both') {
        showAudioModal(data.mediaLocation, data.txt, articleWikiLink);
        createNewAccordianCard(queryTopResultText, data.articleContents);
      }
    };
    const data = new FormData();
    data.append('wikipediaLink', articleWikiLink);
    console.debug(`data is ${data}`);
    // request.setRequestHeader("Content-type", "application/json")
    request.send(data);
  }

  function defaultStyle() {
    // console.debug(`searchBox.value is ${searchBox.value}`)
    if (!searchBox.value) {
      searchMainDiv.style.borderRadius = '24px';
      searchMainDiv.style.boxShadow = 'none';
      searchMainDiv.style.borderColor = 'rgb(223, 225, 229)';
      searchSuggestion.style.display = 'none';
    } else {
      searchMainDiv.style.borderRadius = '24px';
      searchMainDiv.style.boxShadow = '0 1px 6px 0 rgba(32,33,36,0.28)';
      searchMainDiv.style.borderColor = 'rgba(223,225,229,0)';
      searchSuggestion.style.display = 'none';
    }
  }

  function focusedStyle() {
    if (searchBox.value) {
      searchMainDiv.style.borderBottomRightRadius = 0;
      searchMainDiv.style.borderBottomLeftRadius = 0;
      searchMainDiv.style.boxShadow = '0 1px 6px 0 rgba(32,33,36,0.28)';
      searchMainDiv.style.borderColor = 'rgba(223,225,229,0)';
      searchSuggestion.style.display = 'flex';
    } else {
      searchMainDiv.style.borderRadius = '24px';
      searchMainDiv.style.boxShadow = '0 1px 6px 0 rgba(32,33,36,0.28)';
      searchMainDiv.style.borderColor = 'rgba(223,225,229,0)';
      searchSuggestion.style.display = 'none';
    }
  }

  function getMatchString(s1, s2) {
    const l1 = s1.toLowerCase();
    const l2 = s2.toLowerCase();
    // console.debug(s1,'---', s2)
    if (l1 === l2) { return s2; }

    let res = '';
    for (let x = 0; x <= s1.length; x += 1) {
      if (l1[x] === l2[x]) {
        res += s2[x];
      } else {
        break;
      }
    }
    return res;
  }

  function getWikipediaresponse(searchText) {
    const wikiLink = `https://en.wikipedia.org/w/api.php?action=opensearch&format=json&origin=*&formatversion=2&search=${searchText}&namespace=0&limit=10`;

    const request = new XMLHttpRequest();
    request.open('GET', wikiLink);

    request.onload = () => {
      const data = JSON.parse(request.responseText);
      // console.debug(data)
      const l = ['<ul class="list-group list-group-flush">'];
      // console.debug(l)

      for (let i = 0; i < 10; i += 1) {
        const textLink = data[3][i];
        const text = data[1][i];
        if (text) {
          const matchText = getMatchString(searchText, text);
          const unmatchedText = text.slice(matchText.length, text.length);
          // console.debug(`${searchText}-->`, matchText, '||', unmatchedText)
          if (matchText) {
            if (unmatchedText) {
              l.push(`<a class="resultLink" href=${textLink}> <li class="listitem"><span style="font-weight:600">${matchText}</span><span>${unmatchedText}</span></li></a>`);
            } else {
              l.push(`<a class="resultLink" href=${textLink}> <li class="listitem"><b>${matchText}</b></li></a>`);
            }
          }
          // document.querySelector('.suggestions').append(ii)
        }
      }
      l.push('</ul>');
      // console.debug(l.join(''))
      searchSuggestionList.innerHTML = l.join('');
      // document.querySelector('.suggestions').innerHTML = l.join('')
      queryTopResultLink = data[3][0];
      // console.debug(queryTopResultLink)
      queryTopResultText = data[1][0];
      return l.join('');
    };
    request.send(null);
    // console.debug(request.responseText)
  }

  function mouseoverMainDiv() {
    searchMainDiv.style.boxShadow = '0 1px 6px 0 rgba(32,33,36,0.28)';
    searchMainDiv.style.borderColor = 'rgba(223,225,229,0)';
  }

  mainDiv.addEventListener('mouseover', () => {
    mouseoverMainDiv();
  });

  searchBox.addEventListener('keyup', (e) => {
    if (e.key === 'Enter') {
      console.debug('keyup event with enter key');
      defaultStyle();
      getAudioFileData('both', queryTopResultLink);
    } else {
      focusedStyle();
      const searchQuery = (e.target.value).trim();
      if (searchQuery) {
        getWikipediaresponse(searchQuery);
      }
    }
  });

  document.addEventListener('click', (e) => {
    const { target } = e;
    const clickVal = mainDiv.contains(target);
    if (target.className === 'accordianCardLinks') {
      const wikipediaArticleLink = target.id;
      console.debug(wikipediaArticleLink);
      getAudioFileData('showAudioModal', wikipediaArticleLink);
    } else if (clickVal) {
      focusedStyle();
    } else {
      defaultStyle();
    }
  });
});
