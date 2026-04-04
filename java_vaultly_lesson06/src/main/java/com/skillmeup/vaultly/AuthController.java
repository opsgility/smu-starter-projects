package com.skillmeup.vaultly;

import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController @RequestMapping("/auth")
public class AuthController {
    private final AuthenticationManager authManager;
    private final JwtUtil jwtUtil;

    public AuthController(AuthenticationManager authManager, JwtUtil jwtUtil) {
        this.authManager=authManager; this.jwtUtil=jwtUtil;
    }

    // TODO Exercise 3: Complete the /auth/login endpoint.
    // Authenticate with authManager.authenticate(new UsernamePasswordAuthenticationToken(username, password))
    // If successful, generate JWT and return: Map.of("token", token)
    @PostMapping("/login")
    public ResponseEntity<Map<String,String>> login(@RequestBody LoginRequest req) {
        return ResponseEntity.ok(Map.of("token", "not-implemented")); // TODO: implement
    }
}
