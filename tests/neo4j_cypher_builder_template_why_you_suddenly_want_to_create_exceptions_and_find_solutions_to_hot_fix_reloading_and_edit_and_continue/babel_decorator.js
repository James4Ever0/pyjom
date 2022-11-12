
// require("@babel/core").transformSync("code", {
//     plugins: ["@babel/plugin-syntax-decorators"]
//   });
function dec(func){
    function innerfunc(...args){
        console.log('calling func with args:', args)
        func(...args)
    }
    return innerfunc
}

@dec
function myfunc(val){
    return val
}

val = myfunc('myval')
console.log('val:', val)