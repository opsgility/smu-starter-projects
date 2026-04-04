package com.skillmeup.blogapi;

import jakarta.persistence.*;
import java.util.HashSet;
import java.util.Set;

// TODO Exercise 1: Add @Entity and @Table(name="posts").
// Add id, title, content, slug, published, createdAt fields with JPA annotations.

// TODO Exercise 2: Add the @ManyToOne relationship to Author:
//   @ManyToOne(fetch = FetchType.LAZY)
//   @JoinColumn(name = "author_id", nullable = false)
//   private Author author;
// Add @ManyToMany to Tag:
//   @ManyToMany
//   @JoinTable(name="post_tags", ...)
//   private Set<Tag> tags = new HashSet<>();

// TODO Exercise 3: Add constructors and getters. Implement addTag(Tag t) and setPublished(boolean p).

public class Post {
    // TODO: implement
}
