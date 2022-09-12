const http = require('http');

const requestListener = function(req, res) {
        // use 'less' to scan this beast?
        console.log("REQUEST AT:", req.url, req.method)
        if (req.url == "/") {
            res.writeHead(200);
            res.end('nodejs );

            }
        }

        const server = http.createServer(requestListener);
        port = 8902
        server.listen(port);
        console.log('server running on http://localhost:' + port);