const express = require('express');
const app = express();
app.use(express.json());
app.get('/api/health', (req, res) => res.json({ status: 'ok', timestamp: new Date() }));
app.get('/api/tasks', (req, res) => res.json([
  { id: 1, title: "Deploy to staging", status: "todo" },
  { id: 2, title: "Run load tests", status: "in-progress" }
]));
app.listen(3000, () => console.log('ForgeBoard on port 3000'));
