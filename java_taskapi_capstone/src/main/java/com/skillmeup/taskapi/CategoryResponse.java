package com.skillmeup.taskapi;

// TODO: Add fields id, name, description, constructor and getters
public class CategoryResponse {
    private Long id; private String name; private String description;
    public CategoryResponse(Long id, String name, String description) {
        this.id = id; this.name = name; this.description = description;
    }
    public Long getId() { return id; }
    public String getName() { return name; }
    public String getDescription() { return description; }
}
