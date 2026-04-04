package com.skillmeup.blogapi;

import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

// TODO Exercise 2: Make this interface extend JpaRepository<Author, Long>.
// Spring Data will auto-implement findAll(), findById(), save(), deleteById().
// Add one derived method: Optional<Author> findByUsername(String username);

public interface AuthorRepository {
    // TODO: extend JpaRepository<Author, Long> and add findByUsername
}
