
////////////////////////////////////////////////////////////////////////
// try to disable security? disable ssl-spdy and spdy
////////////////////////////////////////////////////////////////////////

// try this first anyway.
setTimeout(function () {
    console.log('start——*-*-*-*-*-');
   Java.perform(function () {
       var SwitchConfig = Java.use('mtopsdk.mtop.global.SwitchConfig');
       SwitchConfig.isGlobalSpdySwitchOpen.overload().implementation = function () {
           var ret = this.isGlobalSpdySwitchOpen.apply(this, arguments);
           console.log("开启抓包" + ret);
           return false;
       }
       SwitchConfig.isGlobalSpdySslSwitchOpen.overload().implementation = function () {
        var ret = this.isGlobalSpdySslSwitchOpen.apply(this, arguments);
        console.log("开启抓包" + ret);
        return false;
       }
   });
});
// ————————————————
// 版权声明：本文为CSDN博主「哈里哈气」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
// 原文链接：https://blog.csdn.net/qq_34067821/article/details/103203549

////////////////////////////////////////////////////////////////////////
// print class names
////////////////////////////////////////////////////////////////////////

// var callback = {
// 	'onMatch': function(cname){
// 		//lets just print out the class name.
// 		console.log(cname);
// 	},
// 	'onComplete': function() {
// 		console.log("done");
// 	},
// 	'onError': function(){
// 		console.log("There is error");
// 	}
// };

// Java.perform(function(){
// 	Java.enumerateLoadedClasses(callback);	//onMatch: function (className)
// });

////////////////////////////////////////////////////////////////////////// failed to hook request/response methods as expected
////////////////////////////////////////////////////////////////////////


// // Java.perform(function () {
// //     // Function to hook is defined here
// //     //所有响应
// in this apk we do not find 'Response' shit.
// //     var Response = Java.use('mtopsdk.network.domain.Response');
// //     Response.$init.overload('mtopsdk.network.domain.Response$Builder').implementation = function() {
// //         //PrintStack()
// //         console.log("Response " + arguments[0].body)
// //         var ret = this.$init.apply(this, arguments);
// //         //all request
// //         console.log("Response " + this.toString())
// //         return ret;
// //     };
    
// //     //所有请求
// //     var RequestBuilder = Java.use('mtopsdk.network.domain.Request$Builder');
// //     RequestBuilder.build.overload().implementation = function() {
// //         //PrintStack()
// //         var ret = this.build.apply(this, arguments);
// //         //all request
// //         console.log("RequestBuilder " + ret.toString())
// //         return ret;
// //     };
    
// //     //所有请求
// //     var ANetworkCallImpl = Java.use('mtopsdk.network.impl.ANetworkCallImpl');
// //     ANetworkCallImpl.$init.overload('mtopsdk.network.domain.Request', 'android.content.Context').implementation = function() {
// //         //PrintStack()
// //         console.log('ANetworkCallImpl ' + arguments[0])
// //         var ret = this.$init.apply(this, arguments);
    
// //         return ret;
// //     };
    
// //     //所有请求url
// //     var AbstractNetworkConverter = Java.use(
// //         'mtopsdk.mtop.protocol.converter.impl.AbstractNetworkConverter'
// //     );
// //     AbstractNetworkConverter.buildBaseUrl.overload(
// //         'mtopsdk.framework.domain.MtopContext',
// //         'java.lang.String',
// //         'java.lang.String'
// //     ).implementation = function() {
// //         console.log("buildBaseUrl "+arguments[1]+' '+arguments[2])
    
// //         var ret = this.buildBaseUrl.apply(this, arguments);
// //         //url
// //         console.log("buildBaseUrl "+ret)
// //         return ret;
// //     };
    
// //     // 禁用spdy协议
// //     var SwitchConfig = Java.use('mtopsdk.mtop.global.SwitchConfig');
// //     SwitchConfig.setGlobalSpdySslSwitchOpen.overload().implementation = function() {
// //         var ret = this.isGlobalSpdySwitchOpen.apply(this, arguments);
// //         console.log('isGlobalSpdySwitchOpenl ' + ret)
    
// //         return false;
// //     };
    
// // });