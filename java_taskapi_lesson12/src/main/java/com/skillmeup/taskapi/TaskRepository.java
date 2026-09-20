package com.skillmeup.taskapi;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TaskRepository extends JpaRepository<Task, Long> {
    // TODO Exercise 1: Add a method to filter by status with pagination:
    //   Page<Task> findByStatus(String status, Pageable pageable);
    // Spring Data derives the query from the method name automatically.
}
