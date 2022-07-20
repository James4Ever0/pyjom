var THREE = require("three");

// Create a DOM
var MockBrowser = require('mock-browser').mocks.MockBrowser;
var mock = new MockBrowser();
var document = MockBrowser.createDocument();
var window = MockBrowser.createWindow();

//REST API
//wtf is going on out here?
var mywidth = 1000;
var myheight = 1000;

var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var router = express.Router();

var gl = require('gl')(1000, 1000); //headless-gl

var pngStream = require('three-png-stream');
var port = process.env.PORT || 8080;


// whatever let's just roll.
router.get('/render', function(req, res) {
    console.log("has render")
    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(75, mywidth / myheight, 0.1, 1000);
    var renderer = new THREE.WebGLRenderer({
        context: gl
    });

    scene.add(camera);

    renderer.setSize(mywidth, myheight);
    renderer.setClearColor(0xFFFFFF, 1);

    /*...
        Add your objects & light to the scene 
    ...*/

    var target = new THREE.WebGLRenderTarget(mywidth, myheight);
    renderer.render(scene, camera, target);


    res.setHeader('Content-Type', 'image/png');
    pngStream(renderer, target).pipe(res);
});

app.use('/api', router);

app.listen(port);
console.log('Server active on port: ' + port);