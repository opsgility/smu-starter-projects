// Meridian Devworks internal API skeleton.
// Two un-implemented endpoints — perfect for running two parallel agent
// conversations against the same codebase, each in its own worktree.

const express = require('express');
const users = require('./data/users.json');
const products = require('./data/products.json');

const app = express();

// TODO: Add pagination. Accept ?page=N&limit=M query parameters.
// Return a response like { page, limit, total, items } where items is the
// paginated subset. Default page=1, default limit=10. Reject negative or
// zero values for either parameter with a 400.
app.get('/users', (req, res) => {
  res.json(users);
});

// TODO: Add filtering. Accept ?category=X query parameter.
// When category is provided, return only products whose category field
// matches (case-insensitive). When category is omitted, return the full
// list. Include the applied filter in the response like { filter, items }.
app.get('/products', (req, res) => {
  res.json(products);
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`[meridian-api] listening on http://127.0.0.1:${PORT}`);
});
