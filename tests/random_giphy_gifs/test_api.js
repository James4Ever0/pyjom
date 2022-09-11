// Require with custom API key
const myBetaApiKey = 'IoJVsWoxDPKBr6gOcCgOPWAB25773hqP';
var giphy = require('giphy-api')(myBetaApiKey);
const fs = require("fs");
const jsonFormat = require("json-format");

function writeJsonToFile(json, filename) {
    // let data = JSON.stringify(json);
    let data = jsonFormat(json);
    fs.writeFile(filename, data, function(err) {
        if (err) {
            console.error(err);
        } else {
            console.log(filename + " has been saved with the json data");
        }
    });
}
// // Require with the public beta key
// var giphy = require('giphy-api')(); // banned. cannot use this public api.
// it may timeout!
// giphy.search({
//     q: 'pokemon',
//     rating: 'g'
// }, function(err, res) {
//     // Res contains gif data!
//     console.log('ERROR?', err); //null if normal.
//     // save it to json?
//     writeJsonToFile(res, 'pokemon_test.json');
// });

