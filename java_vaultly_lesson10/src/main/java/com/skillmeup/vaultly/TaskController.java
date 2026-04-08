package com.skillmeup.vaultly;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

// TODO Exercise 3: Inject TaskService instead of TaskRepository (after creating TaskService in Exercise 4)
// TODO Exercise 3: In create(), set ownerUsername from SecurityContextHolder before saving
@RestController
@RequestMapping("/api/tasks")
public class TaskController {

    private final TaskRepository repo;

    public TaskController(TaskRepository repo) {
        this.repo = repo;
    }

    @GetMapping
    public List<Task> getAllTasks() {
        return repo.findAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Task> getById(@PathVariable Long id) {
        return repo.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<Task> create(@RequestBody Task t) {
        // TODO Exercise 3: Set ownerUsername from SecurityContextHolder.getContext().getAuthentication().getName()
        return ResponseEntity.status(201).body(repo.save(t));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        repo.deleteById(id);
        return ResponseEntity.noContent().build();
    }
}
