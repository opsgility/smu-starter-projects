package com.skillmeup.taskapi;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import java.util.Map;
import java.util.stream.Collectors;

// TODO Exercise 3: Implement the two exception handlers below.

@RestControllerAdvice
public class GlobalExceptionHandler {

    // TODO: Handle MethodArgumentNotValidException — extract field errors and return 400
    // Return: ResponseEntity.badRequest().body(Map.of("errors", fieldErrorMessages))
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Map<String, Object>> handleValidation(MethodArgumentNotValidException ex) {
        return ResponseEntity.badRequest().body(Map.of("error", "Validation failed")); // TODO: improve
    }

    // TODO: Handle RuntimeException — return 404 if message contains "not found", else 500
    @ExceptionHandler(RuntimeException.class)
    public ResponseEntity<Map<String, String>> handleRuntime(RuntimeException ex) {
        if (ex.getMessage() != null && ex.getMessage().toLowerCase().contains("not found")) {
            return ResponseEntity.status(404).body(Map.of("error", ex.getMessage()));
        }
        return ResponseEntity.status(500).body(Map.of("error", "Internal server error"));
    }
}
