# warning! potential code injection.
# better use some json5 formatter instead.
curl "https://codeshare.frida.re/@Gand3lf/xamarin-antiroot/" 2>/dev/null | grep "projectSource: " | sed 's/projectSource:/"projectSource":/;s/^/{/;s/,$//;s/$/}/'  
# curl "https://codeshare.frida.re/@Gand3lf/xamarin-antiroot/" 2>/dev/null | grep "projectSource: " | sed 's/^/var a={/;s/$/}\; console.log(a.projectSource);/' | node