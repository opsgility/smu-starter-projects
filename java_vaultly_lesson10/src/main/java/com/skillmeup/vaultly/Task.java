package com.skillmeup.vaultly;

import jakarta.persistence.*;

@Entity @Table(name = "tasks")
public class Task {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY) private Long id;
    @Column(nullable=false) private String title;
    private String description;
    private String status;
    private String ownerUsername;

    public Task() {}
    public Task(String title, String description, String ownerUsername) {
        this.title=title; this.description=description; this.ownerUsername=ownerUsername; this.status="PENDING";
    }
    public Long getId() { return id; }
    public String getTitle() { return title; }
    public String getDescription() { return description; }
    public String getStatus() { return status; }
    public String getOwnerUsername() { return ownerUsername; }
    public void setTitle(String t) { this.title=t; }
    public void setStatus(String s) { this.status=s; }
    public void setOwnerUsername(String u) { this.ownerUsername=u; }
}
