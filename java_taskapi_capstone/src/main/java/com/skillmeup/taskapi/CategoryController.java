package com.skillmeup.taskapi;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

// TODO Capstone Exercise 3: Implement all endpoints:
// GET /api/categories — list all categories
// POST /api/categories — create a category
// GET /api/categories/{id}/tasks — get tasks for a category (paginated)

@RestController
@RequestMapping("/api/categories")
public class CategoryController {
    private final CategoryRepository categoryRepo;
    private final TaskRepository taskRepo;

    public CategoryController(CategoryRepository categoryRepo, TaskRepository taskRepo) {
        this.categoryRepo = categoryRepo; this.taskRepo = taskRepo;
    }

    // TODO: implement GET /api/categories
    @GetMapping
    public List<Category> getAll() { return categoryRepo.findAll(); }

    // TODO: implement POST /api/categories
    @PostMapping
    public ResponseEntity<Category> create(@RequestBody Category category) {
        return ResponseEntity.status(201).body(categoryRepo.save(category));
    }

    // TODO: implement GET /api/categories/{id}/tasks
    @GetMapping("/{id}/tasks")
    public Page<TaskResponse> getTasksForCategory(@PathVariable Long id, Pageable pageable) {
        return Page.empty(); // TODO: implement using taskRepo
    }
}
