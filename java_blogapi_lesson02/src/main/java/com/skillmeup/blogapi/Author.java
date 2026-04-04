package com.skillmeup.blogapi;

import jakarta.persistence.*;
import java.time.LocalDateTime;

// TODO Exercise 1: Add @Entity and @Table(name = "authors") annotations.
// Add @Id and @GeneratedValue(strategy = GenerationType.IDENTITY) on the id field.
// Add @Column(nullable = false, unique = true) on username.
// Add @Column(nullable = false) on email.

// TODO Exercise 2: Add all fields: Long id, String username, String email,
//   String displayName, LocalDateTime createdAt.
// Add a no-arg constructor and a constructor(username, email, displayName)
//   that also sets createdAt = LocalDateTime.now().

// TODO Exercise 3: Add getters for all fields. No setters needed (immutable after creation).
// Verify Hibernate creates the table: run the app and check the logs for "create table authors".

public class Author {
    // TODO: add annotations and implement
}
