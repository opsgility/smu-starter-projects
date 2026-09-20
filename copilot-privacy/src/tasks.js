// ForgeBoard Task Module
// Note: This file contains intentional security vulnerabilities for training purposes.

const tasks = {};
let nextId = 1;

function createTask(title, description) {
    const id = nextId++;
    tasks[id] = { id, title, description };
    return tasks[id];
}

function getTask(id) {
    return tasks[id] || null;
}

function listTasks() {
    return Object.values(tasks);
}

// VULNERABILITY: XSS — task title inserted without HTML escaping
function renderTaskHtml(task) {
    return `<div class="task" data-id="${task.id}">
        <h3>${task.title}</h3>
        <p>${task.description}</p>
    </div>`;
}

module.exports = { createTask, getTask, listTasks, renderTaskHtml };
