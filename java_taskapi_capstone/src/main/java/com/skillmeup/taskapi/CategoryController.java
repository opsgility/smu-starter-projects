package com.skillmeup.taskapi;

import jakarta.validation.Valid;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

// TODO Exercise 3: Wire all endpoints through CategoryService (not direct repository calls).
// TODO Exercise 3: Add GET /api/categories/{id} — single category by id
// TODO Exercise 3: Add PUT /api/categories/{id} — update category
// TODO Exercise 3: Add DELETE /api/categories/{id} — delete category (204 No Content)
// TODO Exercise 3: Add @Valid to @RequestBody parameters

@RestController
@RequestMapping("/api/categories")
public class CategoryController {

    private final CategoryService categoryService;
    private final TaskRepository taskRepo;

    public CategoryController(CategoryService categoryService, TaskRepository taskRepo) {
        this.categoryService = categoryService;
        this.taskRepo = taskRepo;
    }

    // TODO Exercise 3: Implement using categoryService.getAllCategories()
    @GetMapping
    public List<CategoryResponse> getAll() {
        return categoryService.getAllCategories();
    }

    // TODO Exercise 3: Implement using categoryService.createCategory(request), return 201 Created
    @PostMapping
    public ResponseEntity<CategoryResponse> create(@Valid @RequestBody CategoryRequest request) {
        return ResponseEntity.status(201).body(categoryService.createCategory(request));
    }

    // TODO Exercise 3: Add @GetMapping("/{id}") — return categoryService.getCategory(id)
    // TODO Exercise 3: Add @PutMapping("/{id}") — return categoryService.updateCategory(id, request)
    // TODO Exercise 3: Add @DeleteMapping("/{id}") — call categoryService.deleteCategory(id), return 204

    // TODO Exercise 3: Implement GET /api/categories/{id}/tasks using taskRepo.findByCategoryId()
    @GetMapping("/{id}/tasks")
    public Page<TaskResponse> getTasksForCategory(@PathVariable Long id, Pageable pageable) {
        return taskRepo.findByCategoryId(id, pageable).map(Task::toResponse);
    }
}
