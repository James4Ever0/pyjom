const {
    Vmd
} = require('vmd.js');
const fs = require('fs');
let arrayBuffer = fs.readFileSync('./miku_dance_recorder/models/mmd/vmds/wavefile_v2.vmd', null).buffer;

let myVMD = new Vmd(arrayBuffer);
// console.log(myVMD)
let timeline = myVMD.timeline
// let myarray = [];
let maxTime = 0
for (let elem of timeline) {
    frameTime = elem.frameTime
    if (frameTime > maxTime) {
        maxTime = frameTime
    }
}
console.log(maxTime)
// 2808 frametime. what is the fps?
// fps is 30
// we assume this shit and now we head on the call.
// time is 93.6
// "Timestep is just the frame number / 30 since MMD is 30 FPS."
// cited from https://github.com/CraftyMoment/mmd_vam_import