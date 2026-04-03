const express = require('express');
const router = express.Router();

const VALID_ROLES = ['admin', 'developer', 'designer', 'qa'];

let users = [
  { id: 1, name: "Alex Chen", username: "alexchen", email: "alex@pixelforge.dev", role: "developer" },
  { id: 2, name: "Sam Rivera", username: "samrivera", email: "sam@pixelforge.dev", role: "admin" },
  { id: 3, name: "Jordan Kim", username: "jordankim", email: "jordan@pixelforge.dev", role: "designer" },
  { id: 4, name: "Taylor Moss", username: "taylormoss", email: "taylor@pixelforge.dev", role: "qa" },
  { id: 5, name: "Morgan Lee", username: "morganlee", email: "morgan@pixelforge.dev", role: "developer" },
];

// Get all users
router.get('/', (req, res) => res.json(users));

// Get user by ID
router.get('/:id', (req, res) => {
  const user = users.find(u => u.id === parseInt(req.params.id));
  user ? res.json(user) : res.status(404).json({ error: "User not found" });
});

module.exports = router;
module.exports.VALID_ROLES = VALID_ROLES;
