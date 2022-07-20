var fs = require("fs")

var self = {};

var ratio = 16 / 9.0;

var canvasWidth = 500;
var canvasHeight = 500;

var window = {
    innerWidth: canvasWidth,
    innerHeight: canvasHeight

};
var document = {
    createElement: function(name) {
        if (name == "canvas") {
            //return new Canvas(canvasWidth, canvasHeight);
        }
        var Canvas = require('canvas')
        return new Canvas(500, 500)
    },
    createElementNS: function(name) {

        var Canvas = require('canvas')
        return new Canvas(500, 500)
    }
};

var THREE = require("./threejs/three.js")
eval(fs.readFileSync("threejs/additionalRenderers.js").toString())
eval(fs.readFileSync("threejs/SceneUtils.js").toString())
// what is this shit?
const EventEmitter = require('events');

//var OS = new ShereOS()

class ThreeClient extends EventEmitter {
    constructor() {
        super()
        var self = this
        this.appId = 667


        self.loaded = false

        this.bgColor = '#282c34'
        this.textColor = '#fff'
        this.tildeColor = '#0000ff'
        this.selectColor = '#ffffff'

        this.width = 500
        this.height = 500



        this.renderer = new THREE.CanvasRenderer();
        this.renderer.setSize(this.width, this.height);

        this.camera = new THREE.PerspectiveCamera(75, this.width / this.height, 0.001, 3000);
        this.camera.position.z = 2;




        this.scene = new THREE.Scene();

        this.scene.background = new THREE.Color(0xECF8FF);
        this.scene.add(new THREE.HemisphereLight(0x606060, 0x404040));
        this.light = new THREE.DirectionalLight(0xffffff);
        this.light.position.set(1, 1, 1).normalize();
        this.scene.add(this.light);
        //console.log(this.scene.children)


        this.updated = false
        /*
        var geometry = new THREE.SphereGeometry( 0.1, 32, 32 );
        var material = new THREE.MeshBasicMaterial( {color: 0xFF0000} );
        this.sphere = new THREE.Mesh( geometry, material );
        this.scene.add( this.sphere );
        */
    }




    getTexture() {
        this.renderer.render(this.scene, this.camera);
        var data = this.renderer.domElement.toDataURL().substr("data:image/png;base64,".length)
        var buf = new Buffer(data, 'base64');
        fs.writeFile('image.png', buf);
        //return this.renderer.domElement.toDataURL().substr("data:image/png;base64,".length);

    }
}

var THREEClient = new ThreeClient();