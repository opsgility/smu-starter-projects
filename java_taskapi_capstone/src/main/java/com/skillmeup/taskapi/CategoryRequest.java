package com.skillmeup.taskapi;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public class CategoryRequest {

    @NotBlank(message = "Category name is required")
    @Size(max = 100, message = "Category name must not exceed 100 characters")
    private String name;

    @Size(max = 500, message = "Description must not exceed 500 characters")
    private String description;

    public CategoryRequest() {}

    public String getName()        { return name; }
    public String getDescription() { return description; }
    public void setName(String n)        { this.name = n; }
    public void setDescription(String d) { this.description = d; }
}
