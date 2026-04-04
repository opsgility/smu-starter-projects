package com.skillmeup.taskapi;

import jakarta.persistence.*;

// TODO Exercise 1: Add @Entity and @Table(name = "tasks") annotations.
// Add @Id, @GeneratedValue(strategy = GenerationType.IDENTITY) on the id field.
// Add @Column(nullable = false) on title.

// TODO Exercise 2: Add all fields: Long id, String title, String description, String status, String dueDate.
// Add a no-arg constructor (required by JPA) and a full constructor.

// TODO Exercise 3: Add getters and setters for all fields.
// Also add a convenience method toResponse() that returns new TaskResponse(id, title, description, status, dueDate).

public class Task {
    // TODO: add @Entity, @Table, fields, constructors, getters, setters, toResponse()
}
