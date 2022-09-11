// Require with custom API key
const myBetaApiKey = 'IoJVsWoxDPKBr6gOcCgOPWAB25773hqP';
var giphy = require('giphy-api')(myBetaApiKey);
const fs = require("fs");

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