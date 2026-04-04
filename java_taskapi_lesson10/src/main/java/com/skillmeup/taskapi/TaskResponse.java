package com.skillmeup.taskapi;

public class TaskResponse {
    private Long   id;
    private String title;
    private String description;
    private String status;
    private String dueDate;

    public TaskResponse(Long id, String title, String description, String status, String dueDate) {
        this.id = id; this.title = title; this.description = description;
        this.status = status; this.dueDate = dueDate;
    }
    public Long   getId()          { return id; }
    public String getTitle()       { return title; }
    public String getDescription() { return description; }
    public String getStatus()      { return status; }
    public String getDueDate()     { return dueDate; }
}
