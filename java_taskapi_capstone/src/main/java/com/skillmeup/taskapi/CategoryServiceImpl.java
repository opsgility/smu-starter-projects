package com.skillmeup.taskapi;

import org.springframework.stereotype.Service;
import java.util.List;
import java.util.stream.Collectors;

// TODO Exercise 2: Implement all CategoryService methods.
// Inject CategoryRepository via constructor.
// For createCategory(): check uniqueness using findByName() before saving.
// For deleteCategory(): check that no tasks are assigned before deleting
//   (throw IllegalStateException("Cannot delete category with assigned tasks") if tasks exist).
// mapToResponse(): return new CategoryResponse(id, name, description, tasks.size())
@Service
public class CategoryServiceImpl implements CategoryService {

    private final CategoryRepository categoryRepo;

    public CategoryServiceImpl(CategoryRepository categoryRepo) {
        this.categoryRepo = categoryRepo;
    }

    @Override
    public List<CategoryResponse> getAllCategories() {
        return categoryRepo.findAll().stream()
            .map(this::mapToResponse)
            .collect(Collectors.toList());
    }

    @Override
    public CategoryResponse getCategory(Long id) {
        // TODO Exercise 2: find by id, throw CategoryNotFoundException if not found
        Category category = categoryRepo.findById(id)
            .orElseThrow(() -> new CategoryNotFoundException(id));
        return mapToResponse(category);
    }

    @Override
    public CategoryResponse createCategory(CategoryRequest request) {
        // TODO Exercise 2: Check uniqueness using categoryRepo.findByName(request.getName())
        // Throw IllegalArgumentException("Category with name 'X' already exists") if found
        Category category = new Category(request.getName(), request.getDescription());
        return mapToResponse(categoryRepo.save(category));
    }

    @Override
    public CategoryResponse updateCategory(Long id, CategoryRequest request) {
        // TODO Exercise 2: find by id, throw CategoryNotFoundException if not found, then save
        Category category = categoryRepo.findById(id)
            .orElseThrow(() -> new CategoryNotFoundException(id));
        category.setName(request.getName());
        category.setDescription(request.getDescription());
        return mapToResponse(categoryRepo.save(category));
    }

    @Override
    public void deleteCategory(Long id) {
        // TODO Exercise 5: Guard against deleting categories with assigned tasks
        if (!categoryRepo.existsById(id)) throw new CategoryNotFoundException(id);
        categoryRepo.deleteById(id);
    }

    private CategoryResponse mapToResponse(Category category) {
        return new CategoryResponse(
            category.getId(),
            category.getName(),
            category.getDescription(),
            category.getTasks().size()
        );
    }
}
