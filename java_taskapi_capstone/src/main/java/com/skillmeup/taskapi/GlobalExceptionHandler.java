package com.skillmeup.taskapi;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import java.util.Map;
import java.util.stream.Collectors;

@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Map<String, Object>> handleValidation(MethodArgumentNotValidException ex) {
        var errors = ex.getBindingResult().getFieldErrors().stream()
            .collect(Collectors.toMap(e -> e.getField(), e -> e.getDefaultMessage(), (a,b) -> a));
        return ResponseEntity.badRequest().body(Map.of("errors", errors));
    }

    // TODO Exercise 5: Add @ExceptionHandler(CategoryNotFoundException.class) that returns 404
    // TODO Exercise 5: Add @ExceptionHandler(IllegalArgumentException.class) that returns 409 Conflict
    //   for "already exists" messages

    @ExceptionHandler(RuntimeException.class)
    public ResponseEntity<Map<String, String>> handleRuntime(RuntimeException ex) {
        if (ex.getMessage() != null && ex.getMessage().toLowerCase().contains("not found"))
            return ResponseEntity.status(404).body(Map.of("error", ex.getMessage()));
        if (ex.getMessage() != null && ex.getMessage().toLowerCase().contains("already exists"))
            return ResponseEntity.status(409).body(Map.of("error", ex.getMessage()));
        return ResponseEntity.status(500).body(Map.of("error", "Internal server error"));
    }
}
