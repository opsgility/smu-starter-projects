package com.skillmeup.taskapi;

import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

// TODO Exercise 2: Add @Valid to the @RequestBody parameter in createTask
// so Spring validates the request against TaskRequest constraints.

@RestController
@RequestMapping("/api/tasks")
public class TaskController {
    private final TaskService taskService;
    public TaskController(TaskService taskService) { this.taskService = taskService; }

    @GetMapping
    public List<TaskResponse> getAllTasks() { return taskService.getAllTasks(); }

    @GetMapping("/{id}")
    public ResponseEntity<TaskResponse> getById(@PathVariable Long id) {
        TaskResponse t = taskService.getById(id);
        return t != null ? ResponseEntity.ok(t) : ResponseEntity.notFound().build();
    }

    @PostMapping
    public ResponseEntity<TaskResponse> create(@RequestBody TaskRequest req) { // TODO: add @Valid
        return ResponseEntity.status(201).body(taskService.createTask(req));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        taskService.deleteTask(id); return ResponseEntity.noContent().build();
    }
}
