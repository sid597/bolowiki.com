`
Wikipedia API for getting search suggestions is :

https://en.wikipedia.org/w/api.php?action=opensearch&format=json&formatversion=2&search=hit&namespace=0&limit=10
https://en.wikipedia.org/w/api.php?action=opensearch&format=json&formatversion=2&search=hitf&namespace=0&limit=10
https://en.wikipedia.org/w/api.php?action=opensearch&format=json&formatversion=2&search=hitfg&namespace=0&limit=10

So will use this API for my case also on a keyup event in the search box

`

document.addEventListener('DOMContentLoaded',() =>{

    // document.querySelector('form').onsubmit() = () => {};
    searchBox = document.querySelector('#searchBox');
     
    searchBox.addEventListener('keyup' ,e => {
        // console.log(e.target.value);
        
        const wikiLink = `https://en.wikipedia.org/w/api.php?action=opensearch&format=json&origin=*&formatversion=2&search=${e.target.value}&namespace=0&limit=10`
        // console.log(wikiLink);
        const request = new XMLHttpRequest()
        request.open('GET', wikiLink);
        // console.log(request)
        request.onload = () => {
            const data = JSON.parse(request.responseText);
            console.log(data)
            var l = ['<ul class="list-group list-group-flush">'];
            console.log(l)
            

            for (var i = 0; i < 10; i++) {
                 
                l.push(`<a href=${data[3][i]}> <li class="list-group-item">${data[1][i]}</li></a>`)
                // document.querySelector('.suggestions').append(ii)
            };
            l.push('</ul>')
            console.log(l)
            // document.querySelector('.suggestions').insertAdjacentHTML('beforeend',l.join(''))
            document.querySelector('.suggestions').innerHTML =l.join('')

        };
         
        request.send(null)
        // console.log(request.responseText)
        return false;
    });


//     wi = new XMLHttpRequest;
// wi.open('GET','https://en.wikipedia.org/w/api.php?action=opensearch&format=json&formatversion=2&search=z&namespace=0&limit=10')
// wi.send()
// wi.responseText




}); 