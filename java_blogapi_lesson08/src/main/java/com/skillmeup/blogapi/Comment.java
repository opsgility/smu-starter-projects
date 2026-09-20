package com.skillmeup.blogapi;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "comments")
public class Comment {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(columnDefinition = "TEXT", nullable = false)
    private String body;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "post_id", nullable = false)
    private Post post;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "author_id")
    private Author author;

    private LocalDateTime createdAt;

    public Comment() {}
    public Comment(String body, Post post, Author author) {
        this.body=body; this.post=post; this.author=author; this.createdAt=LocalDateTime.now();
    }
    public Long getId() { return id; }
    public String getBody() { return body; }
    public Post getPost() { return post; }
    public Author getAuthor() { return author; }
    public LocalDateTime getCreatedAt() { return createdAt; }
}
