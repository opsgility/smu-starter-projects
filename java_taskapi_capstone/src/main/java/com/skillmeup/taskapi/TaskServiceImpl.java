package com.skillmeup.taskapi;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

@Service
public class TaskServiceImpl implements TaskService {
    private final TaskRepository repo;
    private final CategoryRepository categoryRepo; // TODO Exercise 4: inject CategoryRepository

    public TaskServiceImpl(TaskRepository repo, CategoryRepository categoryRepo) {
        this.repo = repo;
        this.categoryRepo = categoryRepo;
    }

    @Override public Page<TaskResponse> getAllTasks(Pageable p) { return repo.findAll(p).map(Task::toResponse); }
    @Override public Page<TaskResponse> getByStatus(String s, Pageable p) { return repo.findByStatus(s, p).map(Task::toResponse); }
    @Override public TaskResponse getById(Long id) { return repo.findById(id).map(Task::toResponse).orElse(null); }

    @Override
    public TaskResponse createTask(TaskRequest req) {
        Task t = new Task(req.getTitle(), req.getDescription(),
                req.getStatus() != null ? req.getStatus() : "PENDING", req.getDueDate());
        // TODO Exercise 4: if req.getCategoryId() != null, look up the category and call t.setCategory(category)
        // Throw CategoryNotFoundException if the categoryId does not exist
        return repo.save(t).toResponse();
    }

    @Override public void deleteTask(Long id) { repo.deleteById(id); }
}
