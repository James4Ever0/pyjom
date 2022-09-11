// Require with custom API key
const myBetaApiKey = 'IoJVsWoxDPKBr6gOcCgOPWAB25773hqP';

Introduction
A web application often needs to communicate with web servers to get various resources. You might need to fetch data from or post data to an external web server or API.

Using client-side JavaScript, this can be achieved using the fetch API and the window.fetch() function. In NodeJS, several packages/libraries can achieve the same result. One of them is the node-fetch package.

node-fetch is a lightweight module that enables us to use the fetch() function in NodeJS, with very similar functionality as window.fetch() in native JavaScript, but with a few differences.

Getting Started With node-fetch
To use node-fetch in your project, cd into your project directory, and run:

$ npm install node-fetch

As of version 3.0, node-fetch is an ESM-only module - you are not able to import it with require(). If you don't use ESM yourself, it's advised to stay on version 2.0 instead of the latest one, in which case you can use the standard require() syntax.

To use the module in code (for versions prior to version 3.0), use:

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