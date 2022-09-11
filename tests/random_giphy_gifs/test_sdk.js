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

let data = gf.trending({ limit: 10 })
console.log(data)