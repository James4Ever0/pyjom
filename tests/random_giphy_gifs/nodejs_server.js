const http=require('http');
// const url = require('url');
const {GiphyFetch}=require('@giphy/js-fetch-api')

function randomAPIKey() {
    var items=[
        "L8eXbxrbPETZxlvgXN9kIEzQ55Df04v0","Gc7131jiJuvI7IdN0HZ1D7nh0ow5BU6g","MRwXFtxAnaHo3EUMrSefHWmI0eYz5aGe","3eFQvabDx69SMoOemSPiYfh9FY0nzO9x","5nt3fDeGakBKzV6lHtRM1zmEBAs6dsIc","eDs1NYmCVgdHvI1x0nitWd5ClhDWMpRE","Gc7131jiJuvI7IdN0HZ1D7nh0ow5BU6g",'IoJVsWoxDPKBr6gOcCgOPWAB25773hqP','lTRWAEGHjB1AkfO0sk2XTdujaPB5aH7X','6esYBEm9OG3wAifbBFZ2mA0Ml6Ic0rvy','sXpGFDGZs0Dv1mmNFvYaGUvYwKX0PWIh'
    ];
    // deleted some unqualified api keys because they look different in length
    var item=items[Math.floor(Math.random()*items.length)];
    return item
}

function getResultParsed(result, typeFilter){
    filteredResult = []
    if ('data' in result){
        for (elem of result['data']){
            dataType = elem['type']
            if (typeFilter.indexOf(dataType) == -1)
{            dataId = elem['id']
            dataUrl = elem['url']
            title = elem['title']
            original = result['images']['original']
            height = original['height']
            width = original['width']
            url = original['url']
            newElem = {
                id:dataId, url: dataUrl, title:title, media:{height:height, width:width, url:url}
            }
            filteredResult.push(newElem)
        }
        }
    }
    return filteredResult
}

function getGF(){
    return new GiphyFetch(randomAPIKey())
}

async function getRandomGifs(keywords,type,callback) {
    result=await getGF().random({tag: keywords,type: type})
    callback(result)
}
async function getSearchGifs(keywords, sort, limit,type, callback){
    // sort in 'recent', 'relevant'
    result = await getGF().search(keywords, {sort:sort, limit:limit,type:type })
    callback(result)
}

function getQueryParams(reqUrl) {
    current_url=new URL('http://localhost'+reqUrl)
    params=current_url.searchParams
    console.log('query parameters:',params)
    return params
}

const typeArray=['gifs','text','videos','stickers']
const ratingArray=['y','g','pg','pg-13','r']
const sortArray = ['recent', 'relevant']
const limitArray = [...Array(101).keys()].slice(20)

function fallbackDefault(params,tag,valid,defaultParam) {
    if (typeof(defaultParam) == 'int'){
        param = parseInt(param)
    }
    if(valid.indexOf(param)==-1) {
        // type = 'gifs'
        console.log(tag+" undefined. falling back to default: "+defaultParam)
        return defaultParam
    }
    return param
}

const validEntries=['/random','/related','/trending','/search']


const requestListener=function(req,res) {
    // use 'less' to scan this beast?
    console.log("REQUEST AT:",req.url,req.method)
    if(req.url=="/") {
        res.writeHead(200);
        res.end('nodejs giphy server');
    } else if(validEntries.indexOf(req.url.split("?")[0])!=-1) {
        params=getQueryParams(req.url)
        q=params.get('q')
        type=fallbackDefault(params,'type',typeArray,typeArray[0])
        rating = fallbackDefault(params, 'rating',ratingArray, ratingArray[1])
        limit = fallbackDefault(params, 'limit',limitArray, 100)
        offset = fallbackDefault(params, 'offset', offsetArray, )
        console.log('search keywords:',q)
        callback = (result) => res.end(getResultParsed(result, ['text', 'sticker'])
        if(q!=null) {
            if(req.url.startsWith('/random')){
                getRandomGifs(q, type, callback)
            }
            elif (req.url.startsWith('/search')){
                getSearchGifs(q, sort, limit, type, callback)
            }
        }
        else {
            res.end('no search keywords.')
        }
        // def = params.get('def')
        // console.log(def, def == null)
        // console.log(req.params)
    } else {
        res.end('not being right')
    }
}

const server=http.createServer(requestListener);
port=8902
server.listen(port);
console.log('server running on http://localhost:'+port);
console.log('server running on http://localhost:'+port);
console.log('server running on http://localhost:'+port);
console.log('server running on http://localhost:'+port);
console.log('server running on http://localhost:'+port);
console.log('server running on http://localhost:'+port);