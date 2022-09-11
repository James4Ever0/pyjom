// Require with custom API key
// const myBetaApiKey = 'IoJVsWoxDPKBr6gOcCgOPWAB25773hqP';
const myBetaApiKey = "Gc7131jiJuvI7IdN0HZ1D7nh0ow5BU6g"; // some common web browser based things.
// can we prepare some key server? i don't know. wtf is this shit?

var giphy = require('giphy-api')(myBetaApiKey);
const JsonFormat = require("json-format")

const fs = require("fs");

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
//     // save it to json?
//     writeJsonToFile(res, 'pokemon_test.json');
// });

// giphy.search({
//     q: 'pokemon',
//     rating: 'y'
// }, function(err, res) {
//     // Res contains gif data!
//     console.log('ERROR?', err); //null if normal.
//     // save it to json?
//     writeJsonToFile(res, 'pokemon_test_youth.json');
// });

// question: is that still image?
// check the duration bro. filter out those ridiculusly short ones.
// Input £0, gif, from 'still_gif_image.gif':
// Duration: 00:00:00.84, start: 0.000000, bitrate: 635 kb/s
// Stream £0:0: Video: gif, bgra, 300x200, 19.42 fps, 25 tbr, 100 tbn

// giphy.random({
//     tag: 'dog funny',
//     rating: 'g',
//     fmt: 'json',
// }, function (err, res) {
//     console.log('ERROR?', err); //null if normal.
//     // save it to json?
//     writeJsonToFile(res, 'funny_dog_test.json');
// });

giphy.id('feqkVgjJpYtjy', function (err, res) { // only one reply. there are no other fancy shits.
    console.log('ERROR?', err); //null if normal.
    // save it to json?
    writeJsonToFile(res, 'id_search2.json');
});