package com.skillmeup.taskapi;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

// TODO Exercise 1: Add @RestController annotation above the class declaration (it's already there).
// Add @GetMapping("/") that returns Map.of("message", "Task API is running", "version", "1.0")

// TODO Exercise 2: Add @GetMapping("/health") that returns
// Map.of("status", "UP", "service", "task-api")

// TODO Exercise 3: Add @GetMapping("/api/tasks") as a placeholder that returns
// Map.of("tasks", new ArrayList<>(), "count", 0)
// Import java.util.ArrayList for this.

@RestController
public class HelloController {

    @GetMapping("/")
    public Map<String, Object> home() {
        return Map.of("message", "Task API is running", "version", "1.0");
    }
}
