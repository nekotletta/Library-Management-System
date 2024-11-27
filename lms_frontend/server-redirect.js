const http = require('http');

const hostname = '100.127.68.1';
const port = 5678;
const redirectTo = 'http://100.127.68.1:5678/';

const server = http.createServer((req, res) => {
  res.writeHead(301, { Location: redirectTo });
  res.end();
});

server.listen(port, hostname, () => {
  console.log(`Redirect server running at http://${hostname}:${port}`);
});