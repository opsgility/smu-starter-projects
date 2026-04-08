package com.skillmeup.taskapi;

// TODO Exercise 3: Implement TaskNotFoundException as a custom RuntimeException.
// - Add a private final Long taskId field
// - Constructor takes Long id, calls super("Task not found with id: " + id), stores id in taskId
// - Add a getter: public Long getTaskId() { return taskId; }
public class TaskNotFoundException extends RuntimeException {
    // TODO: implement
    public TaskNotFoundException(Long id) {
        super("Task not found with id: " + id);
    }
}
