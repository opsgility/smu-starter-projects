// ForgeBoard Task Module - INTENTIONALLY VULNERABLE FOR TRAINING
function renderTaskTitle(task) {
  // VULNERABILITY: XSS - using innerHTML with unsanitized user input
  return `<div class="task-title">${task.title}</div>`;
}

function executeCommand(userInput) {
  const { execSync } = require('child_process');
  // VULNERABILITY: Command injection - unsanitized input to shell
  return execSync(`grep -r "${userInput}" ./tasks/`).toString();
}

function generateSecureId() {
  // VULNERABILITY: Math.random() is not cryptographically secure
  return Math.random().toString(36).substring(2);
}

module.exports = { renderTaskTitle, executeCommand, generateSecureId };
