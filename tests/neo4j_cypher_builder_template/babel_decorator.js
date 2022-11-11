function decorate(func){
    function innerfunc(...args){
        
    }
    return innerfunc
}

@decorate
function myfunc(val){
    return val
}