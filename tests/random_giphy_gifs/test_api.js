// Require with custom API key
const myBetaApiKey = 'IoJVsWoxDPKBr6gOcCgOPWAB25773hqP';
var giphy = require('giphy-api')(myBetaApiKey);
const fs = require("fs");

function writeJsonToFile(json, filename) {

}
// // Require with the public beta key
// var giphy = require('giphy-api')(); // banned. cannot use this public api.
// it may timeout!
giphy.search({
    q: 'pokemon',
    rating: 'g'
}, function(err, res) {
    // Res contains gif data!
    // console.log(res);
    // save it to json?
    writeJsonToFile(res, 'pokemon_test.json');
});