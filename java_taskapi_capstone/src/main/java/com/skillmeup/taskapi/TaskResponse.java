package com.skillmeup.taskapi;

public class TaskResponse {
    private Long   id;
    private String title;
    private String description;
    private String status;
    private String dueDate;
    private String categoryName; // TODO Exercise 4: populated when category is assigned

    public TaskResponse(Long id, String title, String description, String status, String dueDate) {
        this.id = id; this.title = title; this.description = description;
        this.status = status; this.dueDate = dueDate;
    }

    public TaskResponse(Long id, String title, String description, String status, String dueDate, String categoryName) {
        this(id, title, description, status, dueDate);
        this.categoryName = categoryName;
    }

    public Long   getId()           { return id; }
    public String getTitle()        { return title; }
    public String getDescription()  { return description; }
    public String getStatus()       { return status; }
    public String getDueDate()      { return dueDate; }
    public String getCategoryName() { return categoryName; }
}
