const http = require('http');
const url = require('url');

function randomAPIKey() {
    var items = ['Yes', 'No', 'Maybe'];
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