// Require with custom API key
const myBetaApiKey = 'IoJVsWoxDPKBr6gOcCgOPWAB25773hqP';

// sXpGFDGZs0Dv1mmNFvYaGUvYwKX0PWIh

const fetch = require('node-fetch');
const fs = require("fs");

const { GiphyFetch } = require('@giphy/js-fetch-api')

const gf = new GiphyFetch(myBetaApiKey)

// fetch 10 gifs

function writeJsonToFile(json, filename) {
    let data = JSON.stringify(json);
    fs.writeFile(filename, data, function(err) {
        if (err) {
            console.error(err);
        } else {
            console.log(filename + " has been saved with the json data");
        }
    });
}

let data = await gf.trending({ limit: 10 }) // a promise
// console.log(data)
// https://bobbyhadz.com/blog/javascript-error-err-require-esm-of-es-module-node-fetch
// fucking hell?
// data.then((result) =>{console.log('TRENDING OUTPUT');
// writeJsonToFile(result, 'trending.json')
// })
writeJsonToFIle(data,'trending.json')
