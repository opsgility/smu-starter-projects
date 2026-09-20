package com.skillmeup.taskapi;

import org.springframework.data.jpa.repository.JpaRepository;

// TODO Exercise 2: Make this interface extend JpaRepository<Task, Long>.
// Spring Data will provide findAll(), findById(), save(), deleteById() automatically.
public interface TaskRepository extends JpaRepository<Task, Long> {
    // No additional methods needed for this lesson — JpaRepository provides everything
}
