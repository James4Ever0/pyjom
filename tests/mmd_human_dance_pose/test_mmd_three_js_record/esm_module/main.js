// ESM syntax is supported.
export {}

import * as THREE from 'three';
import * as gl from 'gl';
// init
const width = 1000;
const height = 1000;

// var width = 64
// var height = 64
var gl2 = gl(width, height, {
    preserveDrawingBuffer: true
})


const camera = new THREE.PerspectiveCamera(70, width / height, 0.01, 10);
camera.position.z = 1;

const scene = new THREE.Scene();

const geometry = new THREE.BoxGeometry(0.2, 0.2, 0.2);
const material = new THREE.MeshNormalMaterial();

const mesh = new THREE.Mesh(geometry, material);
scene.add(mesh);


const renderer = new THREE.WebGLRenderer({
    antialias: true,
    context: gl2
});
renderer.setSize(width, height);
renderer.setAnimationLoop(animation);