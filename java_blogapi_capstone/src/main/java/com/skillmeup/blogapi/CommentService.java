package com.skillmeup.blogapi;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class CommentService {
    private final CommentRepository commentRepo;
    private final PostRepository postRepo;
    private final AuthorRepository authorRepo;

    public CommentService(CommentRepository commentRepo, PostRepository postRepo, AuthorRepository authorRepo) {
        this.commentRepo=commentRepo; this.postRepo=postRepo; this.authorRepo=authorRepo;
    }

    // TODO Capstone Exercise 2: Implement createComment(Long postId, Long authorId, String body)
    // - Find post by postId, throw RuntimeException if not found
    // - Find author by authorId (optional — null if anonymous)
    // - Create new Comment(body, post, author) and save
    @Transactional
    public Comment createComment(Long postId, Long authorId, String body) {
        return null; // TODO: implement
    }

    // TODO Capstone Exercise 3: Implement getCommentsByPost(Long postId, Pageable pageable)
    // Add a method to CommentRepository:
    //   Page<Comment> findByPostIdAndDeletedFalse(Long postId, Pageable pageable);
    // Call it here.
    public Page<Comment> getCommentsByPost(Long postId, Pageable pageable) {
        return Page.empty(); // TODO: implement
    }

    // TODO Capstone Exercise 3 (continued): Implement softDeleteComment(Long commentId)
    @Transactional
    public void softDeleteComment(Long commentId) {
        // TODO: implement
    }
}
