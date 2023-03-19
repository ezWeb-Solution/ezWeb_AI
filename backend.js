const http = require('http');
const fs = require('fs');
const path = require('path');

const server = http.createServer((req, res) => {
  if (req.method === 'GET' && req.url === '/style') {
    const cssFilePath = path.join(__dirname, 'style.css');

    fs.readFile(cssFilePath, (err, data) => {
      if (err) {
        res.statusCode = 500;
        res.end(`Error getting the file: ${err}.`);
      } else {
        res.setHeader('Content-Type', 'text/css');
        res.end(data);
      }
    });
  } else if (req.method === 'GET' && req.url === '/html') {
    const cssFilePath = path.join(__dirname, 'home.html');

    fs.readFile(cssFilePath, (err, data) => {
      if (err) {
        res.statusCode = 500;
        res.end(`Error getting the file: ${err}.`);
      } else {
        res.setHeader('Content-Type', 'text/css');
        res.end(data);
      }
    });
  } else if (req.method === 'POST' && req.url === '/uploadcss') {
    let body = '';
    req.on('data', (chunk) => {
      body += chunk;
    });
    req.on('end', () => {
      const cssFilePath = path.join(__dirname, 'style.css');
      fs.writeFile(cssFilePath, body, (err) => {
        if (err) {
          res.statusCode = 500;
          res.end(`Error saving the file: ${err}.`);
        } else {
          res.statusCode = 200;
          res.end('File uploaded successfully.');
        }
      });
    });
  } else if (req.method === 'POST' && req.url === '/uploadhtml') {
    let body = '';
    req.on('data', (chunk) => {
      body += chunk;
    });

    req.on('end', () => {
      const cssFilePath = path.join(__dirname, 'home.html');
      fs.writeFile(cssFilePath, body, (err) => {
        if (err) {
          res.statusCode = 500;
          res.end(`Error saving the file: ${err}.`);
        } else {
          res.statusCode = 200;
          res.end('File uploaded successfully.');
        }
      });
    });
  } else {
    res.statusCode = 404;
    res.end('Not found');
  }
});

const PORT = process.env.PORT || 3000;

server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});