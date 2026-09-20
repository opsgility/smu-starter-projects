package com.skillmeup.taskapi;

import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface CategoryRepository extends JpaRepository<Category, Long> {
    // TODO Exercise 1: Add findByName(String name) returning Optional<Category>
    // This is used in CategoryServiceImpl to check for duplicate names before saving.
}
