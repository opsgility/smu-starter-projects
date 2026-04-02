import express from 'express';

const app = express();
app.use(express.json());

app.get('/', (req, res) => {
  res.json({ service: 'ByteForge API', status: 'running' });
});

// TODO: Students will add routes and tests

export default app;
