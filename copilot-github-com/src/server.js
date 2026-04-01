const express = require('express');
const app = express();
app.use(express.json());
const tasks = require('./tasks');
const users = require('./users');
app.use('/api/tasks', tasks);
app.use('/api/users', users);
app.listen(3000, () => console.log('ForgeBoard on port 3000'));
