const http = require('http');
const url = require('url');

function randomAPIKey() {
    var items = [ "L8eXbxrbPETZxlvgXN9kIEzQ55Df04v0", "Gc7131jiJuvI7IdN0HZ1D7nh0ow5BU6g", "MRwXFtxAnaHo3EUMrSefHWmI0eYz5aGe", "3eFQvabDx69SMoOemSPiYfh9FY0nzO9x", "5nt3fDeGakBKzV6lHtRM1zmEBAs6dsIc", "e0771ed7b244ec9c942bea646ad08e6bf514f51a", "i3dev0tcpgvcuaocfmdslony2q9er7tvfndxcszm", "eDs1NYmCVgdHvI1x0nitWd5ClhDWMpRE"];
    var item = items[Math.floor(Math.random() * items.length)];
    return item
}

const requestListener = function(req, res) {
    // use 'less' to scan this beast?
    console.log("REQUEST AT:", req.url, req.method)
    if (req.url == "/") {
        res.writeHead(200);
        res.end('nodejs giphy server');
    } else if (req.url.startsWith('/random')) {
        current_url = new URL('http://localhost' + req.url)
        params = current_url.searchParams
        console.log(params, typeof(params))
        q = params.get('q')
            // def = params.get('def')
            // console.log(q, q == null)
            // console.log(def, def == null)

        // console.log(req.params)
        res.end('random gifs:')
    } else {
        res.end('not being right')
    }
}

const server = http.createServer(requestListener);
port = 8902
server.listen(port);
console.log('server running on http://localhost:' + port);
console.log('server running on http://localhost:' + port);