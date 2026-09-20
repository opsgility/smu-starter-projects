package com.skillmeup.blogapi;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class CommentController {
    private final CommentService commentService;
    public CommentController(CommentService commentService) { this.commentService=commentService; }

    // TODO: wire the CommentService methods to these endpoints:
    @PostMapping("/posts/{postId}/comments")
    public ResponseEntity<Comment> create(@PathVariable Long postId, @RequestBody CommentRequest req) {
        return ResponseEntity.status(201).body(commentService.createComment(postId, req.authorId, req.body));
    }
    @GetMapping("/posts/{postId}/comments")
    public Page<Comment> list(@PathVariable Long postId, Pageable pageable) {
        return commentService.getCommentsByPost(postId, pageable);
    }
    @DeleteMapping("/comments/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        commentService.softDeleteComment(id); return ResponseEntity.noContent().build();
    }
}
