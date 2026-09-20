package com.skillmeup.taskapi;

import jakarta.persistence.*;
import java.util.ArrayList;
import java.util.List;

// TODO Exercise 1: Add the following JPA annotations:
//   - @Entity on the class
//   - @Table(name = "categories") on the class
//   - @Id @GeneratedValue(strategy = GenerationType.IDENTITY) on the id field
//   - @Column(nullable = false, unique = true) on the name field
//   - @OneToMany(mappedBy = "category", fetch = FetchType.LAZY) on the tasks field
// TODO Exercise 1: Add no-arg constructor, two-arg constructor(name, description),
//   and getters/setters for all fields.
public class Category {
    private Long id;

    private String name;
    private String description;

    private List<Task> tasks = new ArrayList<>();

    public Category() {}

    public Category(String name, String description) {
        this.name = name; this.description = description;
    }

    public Long       getId()          { return id; }
    public String     getName()        { return name; }
    public String     getDescription() { return description; }
    public List<Task> getTasks()       { return tasks; }
    public void setName(String n)        { this.name = n; }
    public void setDescription(String d) { this.description = d; }
}
