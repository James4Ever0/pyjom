const http = require('http');

const requestListener = function(req, res) {
    console.log(req)
    res.writeHead(200);
    res.end('Hello, World!');
}

const server = http.createServer(requestListener);
server.listen(89 port);
console.log('server running on http://localhost:' + port);