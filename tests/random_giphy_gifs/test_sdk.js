// Require with custom API key
const myBetaApiKey = 'IoJVsWoxDPKBr6gOcCgOPWAB25773hqP';
const fs = require("fs");

const { GiphyFetch } = require('@giphy/js-fetch-api')

const gf = new GiphyFetch('your api key')

// fetch 10 gifs
let data = await gf.trending({ limit: 10 })

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