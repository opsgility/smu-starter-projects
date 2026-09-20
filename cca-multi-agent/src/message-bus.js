// TODO: Step 2 — Implement the MessageBus class
// The bus should support:
//   - publish(stage, data): store a message and notify listeners
//   - subscribe(stage, callback): register a listener for a stage
//   - getLastMessage(stage): return the most recent message for a stage
// Each published message should have: id, stage, timestamp, data

class MessageBus {
  constructor() {
    this.messages = [];
    this.listeners = new Map();
    // TODO: initialize any additional state
  }

  publish(stage, data) {
    // TODO: implement
    // Create a message object with id, stage, timestamp, data
    // Store it and notify listeners
  }

  subscribe(stage, callback) {
    // TODO: implement
  }

  getLastMessage(stage) {
    // TODO: implement
  }
}

module.exports = { MessageBus };
