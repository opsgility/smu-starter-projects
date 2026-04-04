package com.skillmeup.blogapi;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "authors")
public class Author {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String username;

    @Column(nullable = false)
    private String email;

    private String displayName;
    private LocalDateTime createdAt;

    public Author() {}
    public Author(String username, String email, String displayName) {
        this.username=username; this.email=email; this.displayName=displayName;
        this.createdAt=LocalDateTime.now();
    }
    public Long getId() { return id; }
    public String getUsername() { return username; }
    public String getEmail() { return email; }
    public String getDisplayName() { return displayName; }
    public LocalDateTime getCreatedAt() { return createdAt; }
}
