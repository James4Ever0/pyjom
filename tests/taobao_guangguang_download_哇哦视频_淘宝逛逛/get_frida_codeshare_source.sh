# warning! potential code injection.
# better use some json5 formatter instead.
# this is strict! fuck.
PARAM=$1
echo "// script name: $PARAM"
echo
# exit
curl "https://codeshare.frida.re/@$PARAM/" 2>/dev/null | grep "projectSource: " | sed 's/projectSource:/"projectSource":/;s/^/{/;s/,$//;s/$/}/' | python3 -c "d=input();import json;p=json.loads(d);print(p['projectSource'])"
# curl "https://codeshare.frida.re/@Gand3lf/xamarin-antiroot/" 2>/dev/null | grep "projectSource: " | sed 's/^/var a={/;s/$/}\; console.log(a.projectSource);/' | node