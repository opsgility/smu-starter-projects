package com.skillmeup.meridian.controller;

import com.skillmeup.meridian.model.NotificationLog;
import com.skillmeup.meridian.repository.NotificationLogRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * Admin endpoints for monitoring and operations.
 *
 * TODO Capstone Exercise 5: Inject NotificationLogRepository and implement
 * GET /admin/notification-log returning paginated NotificationLog entries.
 */
@RestController
@RequestMapping("/admin")
public class AdminController {
    private final NotificationLogRepository notificationLogRepository;

    public AdminController(NotificationLogRepository notificationLogRepository) {
        this.notificationLogRepository = notificationLogRepository;
    }

    // TODO Exercise 5: Implement this endpoint
    // @GetMapping("/notification-log")
    // public ResponseEntity<Page<NotificationLog>> getNotificationLog(
    //         @RequestParam(defaultValue = "0") int page,
    //         @RequestParam(defaultValue = "20") int size) {
    //     return ResponseEntity.ok(notificationLogRepository.findAllByOrderByProcessedAtDesc(
    //         PageRequest.of(page, size)));
    // }
}
