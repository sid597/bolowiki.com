// Wikipedia API for getting search suggestions is :

// https://en.wikipedia.org/w/api.php?action=opensearch&format=json&formatversion=2&search=hit&namespace=0&limit=10
// https://en.wikipedia.org/w/api.php?action=opensearch&format=json&formatversion=2&search=hitf&namespace=0&limit=10
// https://en.wikipedia.org/w/api.php?action=opensearch&format=json&formatversion=2&search=hitfg&namespace=0&limit=10

// So will use this API for my case also on a keyup event in the search box

// ;

document.addEventListener('DOMContentLoaded', () => {
  // document.querySelector('form').onsubmit() = () => {};
  const searchBox = document.querySelector('#searchBox');

  searchBox.addEventListener('keyup', (e) => {
    // console.debug(e.target.value);

    const wikiLink = `https://en.wikipedia.org/w/api.php?action=opensearch&format=json&origin=*&formatversion=2&search=${e.target.value}&namespace=0&limit=10`;
    // console.debug(wikiLink);
    const request = new XMLHttpRequest();
    request.open('GET', wikiLink);
    // console.debug(request)
    request.onload = () => {
      const data = JSON.parse(request.responseText);
      console.debug(data);
      const l = ['<ul class="list-group list-group-flush">'];
      console.debug(l);

      for (let i = 0; i < 10; i += 1) {
        l.push(`<a href=${data[3][i]}> <li class="listitem">${data[1][i]}</li></a>`);
        // document.querySelector('.suggestions').append(ii)
      }
      l.push('</ul>');
      console.debug(l);
      // document.querySelector('.suggestions').insertAdjacentHTML('beforeend',l.join(''))
      document.querySelector('.suggestions').innerHTML = l.join('');
    };

    request.send(null);
    // console.debug(request.responseText)
    return false;
  });
});
