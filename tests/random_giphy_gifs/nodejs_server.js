const http = require('http');
// const url = require('url');
const { GiphyFetch } = require('@giphy/js-fetch-api')



function randomAPIKey() {
    var items = [
        "L8eXbxrbPETZxlvgXN9kIEzQ55Df04v0", "Gc7131jiJuvI7IdN0HZ1D7nh0ow5BU6g", "MRwXFtxAnaHo3EUMrSefHWmI0eYz5aGe", "3eFQvabDx69SMoOemSPiYfh9FY0nzO9x", "5nt3fDeGakBKzV6lHtRM1zmEBAs6dsIc", "eDs1NYmCVgdHvI1x0nitWd5ClhDWMpRE", "Gc7131jiJuvI7IdN0HZ1D7nh0ow5BU6g", 'IoJVsWoxDPKBr6gOcCgOPWAB25773hqP', 'lTRWAEGHjB1AkfO0sk2XTdujaPB5aH7X', '6esYBEm9OG3wAifbBFZ2mA0Ml6Ic0rvy', 'sXpGFDGZs0Dv1mmNFvYaGUvYwKX0PWIh'
    ];
    // deleted some unqualified api keys because they look different in length
    var item = items[Math.floor(Math.random() * items.length)];
    return item
}

async function getRandomGifs(keywords, type, rating, callback){
    gf = new GiphyFetch(randomAPIKey())
    result = await gf.random({tag: keywords, type: type, rating: rating})
    callback(result)
}

function getQueryParams(reqUrl) {
    current_url = new URL('http://localhost' + reqUrl)
    params = current_url.searchParams
    console.log('query parameters:', params)
    return params
}

const typeArray = ['gifs', 'text', 'videos', 'stickers']

function fallbackDefault(param, tag, valid, default) {
    
}

const requestListener = function(req, res) {
    // use 'less' to scan this beast?
    console.log("REQUEST AT:", req.url, req.method)
    if (req.url == "/") {
        res.writeHead(200);
        res.end('nodejs giphy server');
    } else if (req.url.startsWith('/random')) {
        params = getQueryParams(req.url)
        q = params.get('q')
        type = params.get('type')
        rating = params.get('rating')
        if (q == null) {
            console.log('search keywords:', q)
            if (typeArray.indexOf(type) == -1) {
                type = 'gifs'
                console.log("type undefined. falling back to default: gifs")
            }
            
        }

        // def = params.get('def')
        // console.log(def, def == null)
        // console.log(req.params)
        res.end('random gifs:')
    } else {
        res.end('not being right')
    }
}

const server = http.createServer(requestListener);
port = 8902
server.listen(port);
console.log('server running on http://localhost:' + port);
console.log('server running on http://localhost:' + port);
console.log('server running on http://localhost:' + port);
console.log('server running on http://localhost:' + port);
console.log('server running on http://localhost:' + port);
console.log('server running on http://localhost:' + port);