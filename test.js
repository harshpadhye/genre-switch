//simple hello world program

var http = require("http");

http.createServer(function(request, response) {
    response.writeHead(200, {"Content-Type": "text/plain"});
    response.write("alexa play the box by roddy rich");
    response.end();
}).listen(8888);