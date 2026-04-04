package com.skillmeup.taskapi;

import org.springframework.stereotype.Service;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicLong;

@Service
public class TaskServiceImpl implements TaskService {
    private final List<TaskResponse> tasks = new ArrayList<>();
    private final AtomicLong idCounter = new AtomicLong(1);

    @Override
    public List<TaskResponse> getAllTasks() { return List.copyOf(tasks); }

    @Override
    public TaskResponse getById(Long id) {
        return tasks.stream().filter(t -> t.getId().equals(id)).findFirst().orElse(null);
    }

    @Override
    public TaskResponse createTask(TaskRequest request) {
        Long id = idCounter.getAndIncrement();
        TaskResponse t = new TaskResponse(id, request.getTitle(), request.getDescription(),
                request.getStatus() != null ? request.getStatus() : "PENDING", request.getDueDate());
        tasks.add(t);
        return t;
    }

    @Override
    public void deleteTask(Long id) { tasks.removeIf(t -> t.getId().equals(id)); }
}
