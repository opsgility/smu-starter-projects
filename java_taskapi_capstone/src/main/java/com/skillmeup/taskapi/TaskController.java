package com.skillmeup.taskapi;

import jakarta.validation.Valid;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/tasks")
public class TaskController {
    private final TaskService taskService;
    public TaskController(TaskService taskService) { this.taskService = taskService; }

    // TODO Exercise 3: Add @RequestParam(required=false) String status parameter.
    // If status is not null, call taskService.getByStatus(status, pageable).
    // Otherwise call taskService.getAllTasks(pageable).
    @GetMapping
    public Page<TaskResponse> getAllTasks(
            @PageableDefault(size = 20, sort = "id") Pageable pageable) {
        return taskService.getAllTasks(pageable); // TODO: add status filter
    }

    @GetMapping("/{id}")
    public ResponseEntity<TaskResponse> getById(@PathVariable Long id) {
        TaskResponse t = taskService.getById(id);
        return t != null ? ResponseEntity.ok(t) : ResponseEntity.notFound().build();
    }

    @PostMapping
    public ResponseEntity<TaskResponse> create(@Valid @RequestBody TaskRequest req) {
        return ResponseEntity.status(201).body(taskService.createTask(req));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        taskService.deleteTask(id); return ResponseEntity.noContent().build();
    }
}
