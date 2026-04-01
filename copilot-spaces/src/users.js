const express = require('express');
const router = express.Router();
let users = [
  { id: 1, name: "Alex Chen", email: "alex@pixelforge.dev", role: "developer" },
  { id: 2, name: "Sam Rivera", email: "sam@pixelforge.dev", role: "lead" },
];
router.get('/', (req, res) => res.json(users));
module.exports = router;
