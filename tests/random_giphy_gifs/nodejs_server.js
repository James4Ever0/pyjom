const http = require('http');

const requestListener = function(req, res) {
    // use 'less' to scan this beast?
    console.log("REQUEST AT:", req.url, req.method)
    res.writeHead(200);
    res.end('Hello, World!');
}

const server = http.createServer(requestListener);
port = 8902
server.listen(port);
console.log('server running on http://localhost:' + port);