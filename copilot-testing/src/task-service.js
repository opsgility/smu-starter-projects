class TaskService {
  constructor() { this.tasks = []; this.nextId = 1; }

  create(title, description, priority = 'medium') {
    if (!title || title.trim() === '') throw new Error('Title is required');
    if (!['low', 'medium', 'high', 'critical'].includes(priority)) throw new Error('Invalid priority');
    const task = { id: this.nextId++, title: title.trim(), description: description || '', status: 'todo', priority, createdAt: new Date(), updatedAt: new Date() };
    this.tasks.push(task);
    return task;
  }

  getById(id) { return this.tasks.find(t => t.id === id) || null; }

  getAll(filters = {}) {
    let result = [...this.tasks];
    if (filters.status) result = result.filter(t => t.status === filters.status);
    if (filters.priority) result = result.filter(t => t.priority === filters.priority);
    if (filters.search) { const s = filters.search.toLowerCase(); result = result.filter(t => t.title.toLowerCase().includes(s) || t.description.toLowerCase().includes(s)); }
    return result;
  }

  update(id, data) {
    const task = this.getById(id);
    if (!task) throw new Error('Task not found');
    if (data.title !== undefined) { if (!data.title || data.title.trim() === '') throw new Error('Title cannot be empty'); task.title = data.title.trim(); }
    if (data.description !== undefined) task.description = data.description;
    if (data.status) { if (!['todo', 'in-progress', 'done'].includes(data.status)) throw new Error('Invalid status'); task.status = data.status; }
    if (data.priority) { if (!['low', 'medium', 'high', 'critical'].includes(data.priority)) throw new Error('Invalid priority'); task.priority = data.priority; }
    task.updatedAt = new Date();
    return task;
  }

  delete(id) { const idx = this.tasks.findIndex(t => t.id === id); if (idx === -1) throw new Error('Task not found'); this.tasks.splice(idx, 1); return true; }

  getStats() {
    const total = this.tasks.length;
    const byStatus = {}; const byPriority = {};
    this.tasks.forEach(t => { byStatus[t.status] = (byStatus[t.status] || 0) + 1; byPriority[t.priority] = (byPriority[t.priority] || 0) + 1; });
    return { total, byStatus, byPriority };
  }
}

module.exports = TaskService;
