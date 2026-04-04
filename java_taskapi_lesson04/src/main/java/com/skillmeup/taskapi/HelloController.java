package com.skillmeup.taskapi;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.ArrayList;
import java.util.Map;

@RestController
public class HelloController {
    @GetMapping("/")
    public Map<String, Object> home() { return Map.of("message", "Task API is running", "version", "1.0"); }

    @GetMapping("/health")
    public Map<String, Object> health() { return Map.of("status", "UP", "service", "task-api"); }

    @GetMapping("/api/tasks")
    public Map<String, Object> tasks() { return Map.of("tasks", new ArrayList<>(), "count", 0); }
}
