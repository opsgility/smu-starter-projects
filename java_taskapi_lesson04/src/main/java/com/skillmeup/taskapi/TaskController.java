package com.skillmeup.taskapi;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

// TODO Exercise 3: Complete the controller methods:
// - GET /api/tasks returns a list of tasks (return empty list for now)
// - POST /api/tasks accepts a TaskRequest body and returns 201 Created with the created TaskResponse
// Hint: use @RequestBody TaskRequest request and ResponseEntity.status(201).body(response)

@RestController
@RequestMapping("/api/tasks")
public class TaskController {

    // TODO: Implement GET — return empty list
    @GetMapping
    public List<TaskResponse> getAllTasks() {
        return List.of(); // placeholder
    }

    // TODO: Implement POST — create a task and return 201
    @PostMapping
    public ResponseEntity<TaskResponse> createTask(@RequestBody TaskRequest request) {
        return ResponseEntity.status(201).body(null); // placeholder
    }
}
