// Minimal GraphQL passthrough backend for the multi-import lab.
// Run: node graphql-server.js
import http from 'node:http';

const schema = `type Order { id: String!, total: Float! } type Query { orders: [Order] }`;
const data = { orders: [{ id: 'ord-001', total: 249.5 }, { id: 'ord-002', total: 59.0 }] };

const server = http.createServer(async (req, res) => {
  if (req.method === 'POST' && req.url === '/graphql') {
    let body = ''; req.on('data', c => body += c);
    req.on('end', () => {
      const { query } = JSON.parse(body || '{}');
      res.setHeader('content-type','application/json');
      if (query && query.includes('orders')) res.end(JSON.stringify({ data }));
      else res.end(JSON.stringify({ errors: [{ message: 'unknown query' }] }));
    });
    return;
  }
  if (req.method === 'GET' && req.url === '/schema') { res.setHeader('content-type','text/plain'); res.end(schema); return; }
  res.statusCode = 404; res.end('not found');
});

server.listen(4000, () => console.log('graphql at :4000/graphql'));
