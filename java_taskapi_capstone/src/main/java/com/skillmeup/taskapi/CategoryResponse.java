package com.skillmeup.taskapi;

public class CategoryResponse {
    private Long   id;
    private String name;
    private String description;
    private int    taskCount;

    public CategoryResponse() {}

    public CategoryResponse(Long id, String name, String description, int taskCount) {
        this.id = id; this.name = name; this.description = description; this.taskCount = taskCount;
    }

    public Long   getId()          { return id; }
    public String getName()        { return name; }
    public String getDescription() { return description; }
    public int    getTaskCount()   { return taskCount; }
    public void setId(Long id)              { this.id = id; }
    public void setName(String name)        { this.name = name; }
    public void setDescription(String d)    { this.description = d; }
    public void setTaskCount(int count)     { this.taskCount = count; }
}
