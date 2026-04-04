package com.skillmeup.taskapi;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import java.util.stream.Collectors;

@Service
public class TaskServiceImpl implements TaskService {
    private final TaskRepository repo;
    public TaskServiceImpl(TaskRepository repo) { this.repo = repo; }

    // TODO Exercise 2: Implement getAllTasks(Pageable pageable)
    // Call repo.findAll(pageable) and map results: .map(Task::toResponse)
    @Override public Page<TaskResponse> getAllTasks(Pageable pageable) {
        return Page.empty(); // TODO: implement
    }

    // TODO Exercise 3: Implement getByStatus(String status, Pageable pageable)
    // Call repo.findByStatus(status, pageable).map(Task::toResponse)
    @Override public Page<TaskResponse> getByStatus(String status, Pageable pageable) {
        return Page.empty(); // TODO: implement
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
