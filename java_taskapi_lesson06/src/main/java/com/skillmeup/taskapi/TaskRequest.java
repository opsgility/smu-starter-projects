package com.skillmeup.taskapi;

public class TaskRequest {
    private String title;
    private String description;
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
