package com.skillmeup.blogapi;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

// TODO Exercise 3: Implement GET /api/authors (return all) and POST /api/authors (create + return 201)
@RestController @RequestMapping("/api/authors")
public class AuthorController {
    private final AuthorRepository repo;
    public AuthorController(AuthorRepository repo) { this.repo = repo; }
    @GetMapping public List<Author> getAll() { return List.of(); } // TODO: implement
    @PostMapping public ResponseEntity<Author> create(@RequestBody Author a) { return ResponseEntity.status(201).body(null); } // TODO
}
