 
function hook_spdy(){
    var SwitchConfig = Java.use('mtopsdk.mtop.global.SwitchConfig');
    SwitchConfig.isGlobalSpdySwitchOpen.overload().implementation = function(){
        var ret = this.isGlobalSpdySwitchOpen.apply(this, arguments);
        console.log("\nSwitchConfig.isGlobalSpdySwitchOpen()="+ret);
        return false;
    }
}