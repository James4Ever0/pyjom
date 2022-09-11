// Require with custom API key
// const myBetaApiKey = 'IoJVsWoxDPKBr6gOcCgOPWAB25773hqP';
const myBetaApiKey = "Gc7131jiJuvI7IdN0HZ1D7nh0ow5BU6g"; // some common web browser based things.

// sXpGFDGZs0Dv1mmNFvYaGUvYwKX0PWIh
// is this key limited? or is it production ready?

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

// const data = await gf.categories() // category are actually keywords here.
// // data.forEach((category) => {
// //     console.log(category) // ICategory
// // })
// await writeJsonToFile(data,'categories.json')

// var data = await gf.gifs('animals','bulldog') // not freaking found!
var data = await gf.gifs('animals','samoyed') // freaking works! guess it is just keyword based search
await writeJsonToFile(data, 'samoyed_subcategory.json')

}
test()
