package com.skillmeup.vaultly;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

// TODO Exercise 4: Inject AuditService and add GET /admin/audit-log endpoint
@RestController
@RequestMapping("/admin")
public class AdminController {

    private final AppUserRepository userRepository;

    public AdminController(AppUserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @GetMapping("/users")
    public ResponseEntity<List<AppUser>> getAllUsers() {
        return ResponseEntity.ok(userRepository.findAll());
    }

    @GetMapping("/users/role/{role}")
    public ResponseEntity<List<AppUser>> getUsersByRole(@PathVariable UserRole role) {
        return ResponseEntity.ok(userRepository.findByRole(role));
    }
}
