package com.skillmeup.taskapi;

import org.springframework.stereotype.Service;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class TaskServiceImpl implements TaskService {
    private final TaskRepository repo;
    public TaskServiceImpl(TaskRepository repo) { this.repo = repo; }

    @Override public List<TaskResponse> getAllTasks() {
        return repo.findAll().stream().map(Task::toResponse).collect(Collectors.toList());
    }
    @Override public TaskResponse getById(Long id) {
        return repo.findById(id).map(Task::toResponse).orElse(null);
    }
    @Override public TaskResponse createTask(TaskRequest req) {
        Task t = new Task(req.getTitle(), req.getDescription(),
                req.getStatus() != null ? req.getStatus() : "PENDING", req.getDueDate());
        return repo.save(t).toResponse();
    }
    @Override public void deleteTask(Long id) { repo.deleteById(id); }
}
