// Task Manager App
// A simple task manager to practice Git branching and merging

const tasks = [];

function addTask(title) {
    tasks.push({ title, completed: false });
    console.log(`Added: ${title}`);
}

function listTasks() {
    if (tasks.length === 0) {
        console.log('No tasks found.');
        return;
    }
    tasks.forEach((task, i) => {
        console.log(`${i + 1}. [${task.completed ? 'x' : ' '}] ${task.title}`);
    });
}

// TODO: Add a completeTask(index) function on a feature branch
// TODO: Add a deleteTask(index) function on a separate feature branch

addTask('Learn Git basics');
addTask('Practice branching');
listTasks();
