package com.skillmeup.taskapi;
import java.util.List;

public interface TaskService {
    List<TaskResponse> getAllTasks();
    TaskResponse       getById(Long id);
    TaskResponse       createTask(TaskRequest request);
    void               deleteTask(Long id);
}
