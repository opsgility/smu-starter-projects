package com.skillmeup.taskapi;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

@Service
public class TaskServiceImpl implements TaskService {
    private final TaskRepository repo;
    public TaskServiceImpl(TaskRepository repo) { this.repo = repo; }

    @Override public Page<TaskResponse> getAllTasks(Pageable p) { return repo.findAll(p).map(Task::toResponse); }
    @Override public Page<TaskResponse> getByStatus(String s, Pageable p) { return repo.findByStatus(s, p).map(Task::toResponse); }
    @Override public TaskResponse getById(Long id) { return repo.findById(id).map(Task::toResponse).orElse(null); }
    @Override public TaskResponse createTask(TaskRequest req) {
        Task t = new Task(req.getTitle(), req.getDescription(),
                req.getStatus() != null ? req.getStatus() : "PENDING", req.getDueDate());
        return repo.save(t).toResponse();
    }
    @Override public void deleteTask(Long id) { repo.deleteById(id); }
}
