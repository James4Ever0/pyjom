const http = require('http');
// const url = require('url');
const { GiphyFetch } = require('@giphy/js-fetch-api');
const GiphyApi = require('giphy-api');

function randomAPIKey() {
    webApiKeys = ["L8eXbxrbPETZxlvgXN9kIEzQ55Df04v0", "Gc7131jiJuvI7IdN0HZ1D7nh0ow5BU6g", "MRwXFtxAnaHo3EUMrSefHWmI0eYz5aGe", "3eFQvabDx69SMoOemSPiYfh9FY0nzO9x", "5nt3fDeGakBKzV6lHtRM1zmEBAs6dsIc", "eDs1NYmCVgdHvI1x0nitWd5ClhDWMpRE"]
    publicSdkKeys = ["Gc7131jiJuvI7IdN0HZ1D7nh0ow5BU6g"]
    apiKeys = ['IoJVsWoxDPKBr6gOcCgOPWAB25773hqP', 'lTRWAEGHjB1AkfO0sk2XTdujaPB5aH7X']
    sdkKeys = ['6esYBEm9OG3wAifbBFZ2mA0Ml6Ic0rvy', 'sXpGFDGZs0Dv1mmNFvYaGUvYwKX0PWIh']

    items = webApiKeys.concat(publicSdkKeys).concat(apiKeys).concat(sdkKeys)
        // deleted some unqualified api keys because they look different in length
    item = items[Math.floor(Math.random() * items.length)];
    console.log("using api key: " + item)
    return item
}

function randInt(start, end) {
    if (start > end) {
        medium = end
        end = start
        start = medium
    } else if (start == end) {
        return Math.floor(start)
    }
    return Math.floor(Math.random() * (end - start) + start)
}

function processElemUncatched(elem, typeFilter) {
    if ('type' in elem) {
        dataType = elem['type']
        if (typeFilter.indexOf(dataType) == -1) {
            dataId = elem['id']
            dataUrl = elem['url']
            title = elem['title']
            original = elem['images']['original']
            height = original['height']
            width = original['width']
            url = original['url']
            newElem = {
                id: dataId,
                url: dataUrl,
                title: title,
                media: { height: height, width: width, url: url }

            }
            return newElem
        }
    } else {
        console.log("some weird data/element encountered. please check.")
        console.log(elem)
    }
    return null
}

function processElem(elem, typeFilter) {
    try {
        result = processElemUncatched(elem, typeFilter)
        return result
    } catch (e) {
        console.log(e)
        console.log("______________________ELEMENT______________________")
        console.log(elem)
        console.log("______________________ELEMENT______________________")
        console.log("error while processing element")
        return null;
    }
}

function getResultParsed(result, typeFilter) {
    filteredResult = []
    if ('data' in result) {
        data = result['data']
        if (Array.isArray(data)) {
            for (elem of data) {
                newElem = processElem(elem, typeFilter)
                if (newElem != null) {
                    filteredResult.push(newElem)
                }
            }
        } else {
            newElem = processElem(data, typeFilter)
            if (newElem != null) {
                filteredResult.push(newElem)
            }
        }
    }
    return JSON.stringify(filteredResult)
}

function getGF() {
    return new GiphyFetch(randomAPIKey())
}

function getApi() {
    return GiphyApi(randomAPIKey())
}

async function getRandomGif(keywords, type, callback) {
    try{
        
    }
    result = await getGF().random({ tag: keywords, type: type })
    callback(result)
}
function getRandomGifs(keywords, rating, callback) {
    getApi().random({ tag: keywords, rating: rating, fmt: 'json' }, function(err, result) {
        console.log('ERROR?', err); //null if normal.
        if (err != null) {
            callback([]);
        } else {
            callback(result)
        }
    })
}
async function getSearchGifs(keywords, sort, limit, offset, type, rating, lang, callback) {
    // sort in 'recent', 'relevant'
    try{
        
    }
    result = await getGF().search(keywords, { sort: sort, limit: limit, offset: offset, type: type, rating: rating, lang: lang })
    callback(result)
}
async function getRelatedGifs(keywords, limit, offset, type, callback) {
    // sort in 'recent', 'relevant'
    try{
        
    }
    result = await getGF().related(keywords, { limit: limit, offset: offset, type: type })
    callback(result)
}
async function getTrendingGifs(limit, offset, type, rating, callback) {
    // sort in 'recent', 'relevant'
    try{
        
    }
    result = await getGF().trending({ limit: limit, offset: offset, type: type, rating: rating })
    callback(result)
}

function getQueryParams(reqUrl) {
    current_url = new URL('http://localhost' + reqUrl)
    params = current_url.searchParams
    console.log('query parameters:', params)
    return params
}

const typeArray = ['gifs', 'text', 'videos', 'stickers']
const ratingArray = ['y', 'g', 'pg', 'pg-13', 'r']
const sortArray = ['recent', 'relevant']
const langArray = ["en", "es", "pt", "id", "fr", "ar", "tr", "th", "vi", "de", "it", "ja", "zh-CN", "zh-TW", "ru", "ko", "pl", "nl", "ro", "hu", "sv", "cs", "hi", "bn", "da", "fa", "tl", "fi", "he", "ms", "no", "uk"]
const limitArray = [...Array(101).keys()].slice(20)
const offsetArray = [...Array(20000).keys()]

function fallbackDefault(params, tag, valid, defaultParam) {
    param = params.get(tag)
    if (typeof(defaultParam) == 'number') {
        param = parseFloat(param)
    }
    if (valid.indexOf(param) == -1) {
        // type = 'gifs'
        console.log(tag + " undefined. falling back to default: " + defaultParam)
        return defaultParam
    }
    return param
}

const validEntries = ['/random', '/related', '/trending', '/search']


const requestListener = function(req, res) {
    // use 'less' to scan this beast?
    console.log("________________________________________________")
    console.log("REQUEST AT:", req.url, req.method)
    if (req.url == "/") {
        res.writeHead(200);
        res.end('nodejs giphy server');
    } else if (validEntries.indexOf(req.url.split("?")[0]) != -1) {
        callback = (result) => {
            res.writeHead(200);
            res.end(getResultParsed(result, ['text', 'sticker']))
        }
        params = getQueryParams(req.url)
        q = params.get('q')
        type = fallbackDefault(params, 'type', typeArray, typeArray[0])
        rating = fallbackDefault(params, 'rating', ratingArray, ratingArray[1])
        limit = fallbackDefault(params, 'limit', limitArray, 100)
        offset = fallbackDefault(params, 'offset', offsetArray, randInt(0, 100))
        sort = fallbackDefault(params, 'sort', sortArray, sortArray[1])
        lang = fallbackDefault(params, 'lang', langArray, 'en')
        console.log('search keywords:', q)
        if (q != null) {
            if (req.url.startsWith('/random')) {
                // getRandomGif(q, type, callback) // this only returns a single random gif. deprecated.
                getRandomGifs(q, rating, callback)
            } else if (req.url.startsWith('/search')) {
                getSearchGifs(q, sort, limit, offset, type, rating, lang, callback)
            } else if (req.url.startsWith('/related')) {
                getRelatedGifs(q, limit, offset, type, callback)
            } else {
                res.end("don't know how you get here")
            }
        } else {
            if (req.url.startsWith('/trending')) {
                getTrendingGifs(limit, offset, type, rating, callback)
            } else { res.end('no search keywords.') }

        }
        // def = params.get('def')
        // console.log(def, def == null)
        // console.log(req.params)
    } else {
        res.end('not being right')
    }
}

const server = http.createServer(requestListener);
port = 8902
server.listen(port);
console.log('server running on http://localhost:' + port);