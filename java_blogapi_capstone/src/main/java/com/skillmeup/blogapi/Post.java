package com.skillmeup.blogapi;

import jakarta.persistence.*;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;
import java.time.LocalDateTime;
import java.util.HashSet;
import java.util.Set;

// TODO Exercise 2: Add @EntityListeners(AuditingEntityListener.class) to enable auditing on this entity.
// Then add @CreatedDate on createdAt and @LastModifiedDate on updatedAt.
// Spring will automatically populate these on save/update.

@Entity @Table(name = "posts")
@EntityListeners(AuditingEntityListener.class)
public class Post {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY) private Long id;
    @Version private Long version;

    @Column(nullable = false) private String title;
    @Column(columnDefinition = "TEXT") private String content;
    private String slug;

    // TODO Exercise 3: Add boolean deleted = false field.
    // Add @SQLRestriction("deleted = false") above the @Entity to filter deleted posts from all queries.
    private boolean deleted = false;

    @CreatedDate     private LocalDateTime createdAt;
    @LastModifiedDate private LocalDateTime updatedAt;  // TODO: this should be @LastModifiedDate

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
        this.slug=title.toLowerCase().replaceAll("\\s+", "-");
    }
    public Long getId() { return id; }
    public String getTitle() { return title; }
    public String getContent() { return content; }
    public boolean isDeleted() { return deleted; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public Author getAuthor() { return author; }
    public Set<Tag> getTags() { return tags; }
    public void setTitle(String t) { this.title=t; }
    public void setContent(String c) { this.content=c; }
    public void softDelete() { this.deleted=true; }
}
