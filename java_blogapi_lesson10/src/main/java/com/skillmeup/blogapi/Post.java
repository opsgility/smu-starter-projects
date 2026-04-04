package com.skillmeup.blogapi;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.HashSet;
import java.util.Set;

@Entity
@Table(name = "posts")
public class Post {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String title;

    @Column(columnDefinition = "TEXT")
    private String content;

    private String slug;
    private boolean published;
    private LocalDateTime createdAt;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "author_id", nullable = false)
    private Author author;

    @ManyToMany
    @JoinTable(name = "post_tags",
        joinColumns = @JoinColumn(name = "post_id"),
        inverseJoinColumns = @JoinColumn(name = "tag_id"))
    private Set<Tag> tags = new HashSet<>();

    public Post() {}
    public Post(String title, String content, Author author) {
        this.title=title; this.content=content; this.author=author;
        this.published=false; this.createdAt=LocalDateTime.now();
        this.slug=title.toLowerCase().replaceAll("\\s+", "-");
    }
    public Long getId() { return id; }
    public String getTitle() { return title; }
    public String getContent() { return content; }
    public String getSlug() { return slug; }
    public boolean isPublished() { return published; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public Author getAuthor() { return author; }
    public Set<Tag> getTags() { return tags; }
    public void setPublished(boolean p) { this.published=p; }
    public void addTag(Tag t) { tags.add(t); }
}
