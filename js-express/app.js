import express from 'express';

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get('/', (req, res) => {
  res.json({ service: 'ByteForge API', status: 'running' });
});

app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

// TODO: Add task routes

app.listen(PORT, () => {
  console.log(`ByteForge API running on http://localhost:${PORT}`);
});

export default app;
