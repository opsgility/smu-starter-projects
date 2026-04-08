package com.skillmeup.taskapi;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import java.util.List;

public interface CategoryService {
    List<CategoryResponse>  getAllCategories();
    CategoryResponse        getCategory(Long id);
    CategoryResponse        createCategory(CategoryRequest request);
    CategoryResponse        updateCategory(Long id, CategoryRequest request);
    void                    deleteCategory(Long id);
}
