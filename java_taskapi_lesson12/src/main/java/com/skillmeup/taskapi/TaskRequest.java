package com.skillmeup.taskapi;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;

public class TaskRequest {
    @NotBlank(message = "Title is required")
    private String title;
    private String description;
    @Pattern(regexp = "PENDING|IN_PROGRESS|COMPLETED", message = "Status must be PENDING, IN_PROGRESS, or COMPLETED")
    private String status;
    private String dueDate;

    public String getTitle()       { return title; }
    public String getDescription() { return description; }
    public String getStatus()      { return status; }
    public String getDueDate()     { return dueDate; }
    public void setTitle(String t)       { this.title = t; }
    public void setDescription(String d) { this.description = d; }
    public void setStatus(String s)      { this.status = s; }
    public void setDueDate(String d)     { this.dueDate = d; }
}
