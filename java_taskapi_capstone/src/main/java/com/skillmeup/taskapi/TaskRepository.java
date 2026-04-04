package com.skillmeup.taskapi;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TaskRepository extends JpaRepository<Task, Long> {
    Page<Task> findByStatus(String status, Pageable pageable);
    Page<Task> findByCategoryId(Long categoryId, Pageable pageable);
}
