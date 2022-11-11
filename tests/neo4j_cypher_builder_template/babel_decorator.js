function decorate(func){
    function innerfunc()
    return innerfunc
}

@decorate
function myfunc(val){
    return val
}