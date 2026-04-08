package com.skillmeup.vaultly;

import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.access.prepost.PostAuthorize;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class TaskService {

    private final TaskRepository taskRepository;

    public TaskService(TaskRepository taskRepository) {
        this.taskRepository = taskRepository;
    }

    public List<Task> getAllTasks() {
        return taskRepository.findAll();
    }

    @PostAuthorize("returnObject.ownerUsername == authentication.name or hasRole('ADMIN')")
    public Task getTaskById(Long id) {
        return taskRepository.findById(id)
            .orElseThrow(() -> new IllegalArgumentException("Task not found: " + id));
    }

    public Task save(Task task) {
        return taskRepository.save(task);
    }

    @PreAuthorize("hasRole('ADMIN')")
    public void deleteTask(Long id) {
        taskRepository.deleteById(id);
    }
}
