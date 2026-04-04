package com.skillmeup.taskapi;

import jakarta.persistence.*;

// TODO Capstone Exercise 1: Add @Entity and @Table(name="categories").
// Add fields: Long id, String name, String description.
// Add @Id, @GeneratedValue, @Column(unique=true, nullable=false) on name.
// Add getters/setters and a toResponse() returning CategoryResponse.
@Entity
@Table(name = "categories")
public class Category {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(unique = true, nullable = false)
    private String name;
    private String description;

    public Category() {}
    public Long   getId()          { return id; }
    public String getName()        { return name; }
    public String getDescription() { return description; }
    public void setName(String n)        { this.name = n; }
    public void setDescription(String d) { this.description = d; }
}
