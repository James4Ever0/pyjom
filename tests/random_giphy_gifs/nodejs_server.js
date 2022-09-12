const http = require('http');
// const url = require('url');
const { GiphyFetch } = require('@giphy/js-fetch-api');

function randomAPIKey() {
    var items = [
        "L8eXbxrbPETZxlvgXN9kIEzQ55Df04v0", "Gc7131jiJuvI7IdN0HZ1D7nh0ow5BU6g", "MRwXFtxAnaHo3EUMrSefHWmI0eYz5aGe", "3eFQvabDx69SMoOemSPiYfh9FY0nzO9x", "5nt3fDeGakBKzV6lHtRM1zmEBAs6dsIc", "eDs1NYmCVgdHvI1x0nitWd5ClhDWMpRE", "Gc7131jiJuvI7IdN0HZ1D7nh0ow5BU6g", 'IoJVsWoxDPKBr6gOcCgOPWAB25773hqP', 'lTRWAEGHjB1AkfO0sk2XTdujaPB5aH7X', '6esYBEm9OG3wAifbBFZ2mA0Ml6Ic0rvy', 'sXpGFDGZs0Dv1mmNFvYaGUvYwKX0PWIh'
    ];
    // deleted some unqualified api keys because they look different in length
    var item = items[Math.floor(Math.random() * items.length)];
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
    return Math.floor(Math.random() * (end - start) + end)
}

function getResultParsed(result, typeFilter) {
    filteredResult = []
    if ('data' in result) {
        for (elem of result['data']) {
            dataType = elem['type']
            if (typeFilter.indexOf(dataType) == -1) {
                dataId = elem['id']
                dataUrl = elem['url']
                title = elem['title']
                original = result['images']['original']
                height = original['height']
                width = original['width']
                url = original['url']
                newElem = {
                    id: dataId,
                    url: dataUrl,
                    title: title,
                    media: { height: height, width: width, url: url }
                }
                filteredResult.push(newElem)
            }
        }
    }
    return filteredResult
}

function getGF() {
    return new GiphyFetch(randomAPIKey())
}

async function getRandomGifs(keywords, type, callback) {
    result = await getGF().random({ tag: keywords, type: type })
    callback(result)
}
async function getSearchGifs(keywords, sort, limit, offset, type, rating, callback) {
    // sort in 'recent', 'relevant'
    result = await getGF().search(keywords, { sort: sort, limit: limit, offset: offset, type: type, rating: rating })
    callback(result)
}
async function getRelatedGifs(keywords, limit, offset, type, callback) {
    // sort in 'recent', 'relevant'
    result = await getGF().related(keywords, { limit: limit, offset: offset, type: type })
    callback(result)
}
async function getTrendingGifs(limit, offset, type, rating, callback) {
    // sort in 'recent', 'relevant'
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
const limitArray = [...Array(101).keys()].slice(20)
const offsetArray = [...Array(1000).keys()]

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
    console.log("REQUEST AT:", req.url, req.method)
    if (req.url == "/") {
        res.writeHead(200);
        res.end('nodejs giphy server');
    } else if (validEntries.indexOf(req.url.split("?")[0]) != -1) {
        callback = (result) => res.end(getResultParsed(result, ['text', 'sticker']))
        params = getQueryParams(req.url)
        q = params.get('q')
        type = fallbackDefault(params, 'type', typeArray, typeArray[0])
        rating = fallbackDefault(params, 'rating', ratingArray, ratingArray[1])
        limit = fallbackDefault(params, 'limit', limitArray, 100)
        offset = fallbackDefault(params, 'offset', offsetArray, randInt(100, 500))
        sort = fallbackDefault(params, 'sort', sortArray, sortArray[1])
        console.log('search keywords:', q)
        if (q != null) {
            if (req.url.startsWith('/random')) {
                getRandomGifs(q, type, callback)
            } else if (req.url.startsWith('/search')) {
                getSearchGifs(q, sort, limit, offset, type, rating, callback)
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