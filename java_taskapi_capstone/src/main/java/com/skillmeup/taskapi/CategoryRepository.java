package com.skillmeup.taskapi;

import org.springframework.data.jpa.repository.JpaRepository;

// TODO Capstone Exercise 2: Create a CategoryRepository extending JpaRepository<Category, Long>.
// Add: Page<Task> findByCategoryId(Long categoryId, Pageable pageable) in TaskRepository instead.
public interface CategoryRepository extends JpaRepository<Category, Long> {
}
