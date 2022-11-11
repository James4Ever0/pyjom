function decorate(func){
    function innerfunc(...args){
        console.log('calling func with args:', args)
        func(...args)
    }
    return innerfunc
}

@decorate
function myfunc(val){
    return val
}

val = myfunc('myval')
console.log('val:', val)