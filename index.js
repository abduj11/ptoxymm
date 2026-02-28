const http = require('http');
const httpProxy = require('http-proxy');

const proxy = httpProxy.createProxyServer({});
const PORT = process.env.PORT || 10000;

const server = http.createServer((req, res) => {
  // يمكنك هنا تخصيص الوجهة target مثلاً لمواقع عامة أو بناء منطق لتوفير خدمة بروكسي عامة
  // هنا مثل: إعادة توجيه كل الطلبات إلى google.com كأمثلة فقط
  proxy.web(req, res, { target: 'http://example.com', changeOrigin: true }, err => {
    res.writeHead(502);
    res.end('Proxy Error');
  });
});

server.listen(PORT, () => {
  console.log(`Proxy running on port ${PORT}`);
});
