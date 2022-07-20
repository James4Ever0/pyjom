// Create a DOM
var MockBrowser = require('mock-browser').mocks.MockBrowser;
var mock = new MockBrowser();
global.document = MockBrowser.createDocument();
global.window = MockBrowser.createWindow();
// global.object = {}
// global.object.uuid = "whatever";

global.navigator = {
    userAgent: "whatever"
}
var THREE = require("three");
// var THREE = require("three.js");

//REST API
//wtf is going on out here?
// var mywidth = 1000;
// var myheight = 1000;

var mywidth = 64;

var myheight = 64;


var gl = require('gl')(mywidth, myheight, {
    preserveDrawingBuffer: true
}); //headless-gl


// whatever let's just roll.

console.log("has render")
var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(75, mywidth / myheight, 0.1, 1000);
mycanvas = document.createElement('canvas');
var renderer = new THREE.WebGLRenderer({
    context: gl,
    antialias: true,
    preserveDrawingBuffer: true
});

scene.add(camera);

renderer.setSize(mywidth, myheight);
renderer.setClearColor(0xFFEEFF, 1); // the freaking color has changed.
// 255 238 255
var myDOMElement = renderer.domElement;
// document.body.appendChild(myDOMElement);

/*...
    Add your objects & light to the scene 
...*/

// var target = new THREE.CanvasRenderer(mywidth, myheight);
// THREE.CanvasRenderer has been removed # there is nothing here.
var target = new THREE.WebGLRenderTarget(mywidth, myheight);

renderer.render(scene, camera, target);

var pixels = new Uint8Array(mywidth * myheight * 4)
gl.readPixels(0, 0, mywidth, myheight, gl.RGBA, gl.UNSIGNED_BYTE, pixels)
process.stdout.write(['P3\n# gl.ppm\n', mywidth, " ", myheight, '\n255\n'].join(''))

for (var i = 0; i < pixels.length; i += 4) {
    for (var j = 0; j < 3; ++j) {
        process.stdout.write(pixels[i + j] + ' ')
    }
} // it seems to be all white.

// how do you take shots?
// well we still can use electron.