// Require with custom API key
const myBetaApiKey = 'IoJVsWoxDPKBr6gOcCgOPWAB25773hqP';

// sXpGFDGZs0Dv1mmNFvYaGUvYwKX0PWIh

const fetch = require('node-fetch');
const fs = require("fs");
const JsonFormat = require("json-format")

const { GiphyFetch } = require('@giphy/js-fetch-api')

const gf = new GiphyFetch(myBetaApiKey)

// fetch 10 gifs

function writeJsonToFile(json, filename) {
    // let data = JSON.stringify(json);
    let data = JsonFormat(json)
    fs.writeFile(filename, data, function(err) {
        if (err) {
            console.error(err);
        } else {
            console.log(filename + " has been saved with the json data");
        }
    });
}

// console.log(data)
// https://bobbyhadz.com/blog/javascript-error-err-require-esm-of-es-module-node-fetch
// fucking hell?
// data.then((result) =>{console.log('TRENDING OUTPUT');
// writeJsonToFile(result, 'trending.json')
// })
async function test(){
// var data = await gf.trending({ limit: 10 }) // a promise
// search for related things dog related things.
// await writeJsonToFile(data,'trending.json')

// var data = await gf.search('dog cute', { sort: 'relevant', rating: 'g'});
// await writeJsonToFile(data,'cute_dog.json')

// var relatedId = "QvBoMEcQ7DQXK"
// var data = await gf.related(relatedId, { limit: 50 })
// await writeJsonToFile(data,'related.json')

const { category } = await gf.categories()
categories.forEach((category) => {
    console.log(category) // ICategory
})
}
test()
