let nextId = 4;
let tasks = [
  { id: 1, title: "Set up CI/CD", status: "done", priority: "high" },
  { id: 2, title: "Database schema", status: "in-progress", priority: "high" },
  { id: 3, title: "User auth", status: "todo", priority: "critical" },
];
module.exports = {
  getAll: () => tasks,
  create: (data) => { const task = { id: nextId++, ...data, createdAt: new Date() }; tasks.push(task); return task; }
};
