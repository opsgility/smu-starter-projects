package com.skillmeup.taskapi;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import java.util.List;

public interface TaskService {
    Page<TaskResponse>  getAllTasks(Pageable pageable);
    Page<TaskResponse>  getByStatus(String status, Pageable pageable);
    TaskResponse        getById(Long id);
    TaskResponse        createTask(TaskRequest request);
    void                deleteTask(Long id);
}
