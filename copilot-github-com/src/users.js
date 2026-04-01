const express = require('express');
const router = express.Router();
let users = [
  { id: 1, name: "Alex Chen", role: "developer" },
  { id: 2, name: "Sam Rivera", role: "lead" },
];
router.get('/', (req, res) => res.json(users));
module.exports = router;
