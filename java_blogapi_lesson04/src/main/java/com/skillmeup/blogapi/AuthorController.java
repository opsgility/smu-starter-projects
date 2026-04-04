package com.skillmeup.blogapi;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;
@RestController @RequestMapping("/api/authors")
public class AuthorController {
    private final AuthorRepository repo;
    public AuthorController(AuthorRepository repo) { this.repo=repo; }
    @GetMapping public List<Author> getAll() { return repo.findAll(); }
    @PostMapping public ResponseEntity<Author> create(@RequestBody Author a) { return ResponseEntity.status(201).body(repo.save(a)); }
    @GetMapping("/{id}") public ResponseEntity<Author> getById(@PathVariable Long id) {
        return repo.findById(id).map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build());
    }
}
