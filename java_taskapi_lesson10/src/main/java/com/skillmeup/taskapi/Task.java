package com.skillmeup.taskapi;

import jakarta.persistence.*;

@Entity
@Table(name = "tasks")
public class Task {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String title;

    private String description;
    private String status;
    private String dueDate;

    public Task() {}
    public Task(String title, String description, String status, String dueDate) {
        this.title = title; this.description = description; this.status = status; this.dueDate = dueDate;
    }
    public Long   getId()          { return id; }
    public String getTitle()       { return title; }
    public String getDescription() { return description; }
    public String getStatus()      { return status; }
    public String getDueDate()     { return dueDate; }
    public void setTitle(String t)       { this.title = t; }
    public void setDescription(String d) { this.description = d; }
    public void setStatus(String s)      { this.status = s; }
    public void setDueDate(String d)     { this.dueDate = d; }

    public TaskResponse toResponse() {
        return new TaskResponse(id, title, description, status, dueDate);
    }
}
