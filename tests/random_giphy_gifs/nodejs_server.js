const http = require('http');

const requestListener = function(req, res) {
    console.log(req.url, req.method)
    res.writeHead(200);
    res.end('Hello, World!');
}

const server = http.createServer(requestListener);
port = 8902
server.listen(port);
console.log('server running on http://localhost:' + port);