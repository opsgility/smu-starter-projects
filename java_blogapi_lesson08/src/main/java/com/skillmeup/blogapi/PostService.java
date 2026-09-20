package com.skillmeup.blogapi;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;

@Service
public class PostService {
    private final PostRepository postRepo;
    private final AuthorRepository authorRepo;
    public PostService(PostRepository postRepo, AuthorRepository authorRepo) {
        this.postRepo=postRepo; this.authorRepo=authorRepo;
    }

    // TODO Exercise 2: Add @Transactional(readOnly = true) to this method.
    // readOnly=true tells Hibernate to skip dirty checking and flush — more efficient for reads.
    public List<Post> getAll() { return postRepo.findAll(); }

    // TODO Exercise 3: Add @Transactional(rollbackFor = Exception.class) to createPost.
    // This ensures that if anything throws (e.g., author not found), the entire transaction rolls back.
    public Post createPost(String title, String content, Long authorId) {
        Author author = authorRepo.findById(authorId)
            .orElseThrow(() -> new RuntimeException("Author not found: " + authorId));
        return postRepo.save(new Post(title, content, author));
    }

    @Transactional
    public Post updatePost(Long id, String title, String content) {
        Post post = postRepo.findById(id).orElseThrow(() -> new RuntimeException("Post not found: " + id));
        post.setTitle(title);
        post.setContent(content);
        return postRepo.save(post); // JPA version check happens here
    }
}
