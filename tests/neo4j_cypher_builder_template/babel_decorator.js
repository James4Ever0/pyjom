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