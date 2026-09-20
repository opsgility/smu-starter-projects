package com.skillmeup.taskapi;

import org.springframework.stereotype.Service;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicLong;

// TODO Exercise 1: Add @Service annotation (already present) and implement TaskService.

// TODO Exercise 2: Add a private List<TaskResponse> tasks = new ArrayList<>() as in-memory store
// and an AtomicLong idCounter = new AtomicLong(1).
// Implement getAllTasks() to return List.copyOf(tasks).

// TODO Exercise 3: Implement createTask(TaskRequest request):
// - Generate id with idCounter.getAndIncrement()
// - Create TaskResponse and add to tasks list, return it.
// Implement getById(Long id) — search the list.
// Implement deleteTask(Long id) — remove from list.

@Service
public class TaskServiceImpl implements TaskService {
    // TODO: add fields and implement methods

    @Override public List<TaskResponse> getAllTasks()             { return new ArrayList<>(); }
    @Override public TaskResponse       getById(Long id)         { return null; }
    @Override public TaskResponse       createTask(TaskRequest r){ return null; }
    @Override public void               deleteTask(Long id)      { }
}
