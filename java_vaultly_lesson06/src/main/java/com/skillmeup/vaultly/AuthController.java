package com.skillmeup.vaultly;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
@RequestMapping("/auth")
public class AuthController {

    private final AppUserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final AuthenticationManager authenticationManager;
    private final JwtUtil jwtUtil;

    public AuthController(AppUserRepository userRepository,
                          PasswordEncoder passwordEncoder,
                          AuthenticationManager authenticationManager,
                          JwtUtil jwtUtil) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.authenticationManager = authenticationManager;
        this.jwtUtil = jwtUtil;
    }

    @PostMapping("/register")
    public ResponseEntity<String> register(@RequestBody RegisterRequest request) {
        if (userRepository.findByUsername(request.username()).isPresent()) {
            return ResponseEntity.status(HttpStatus.CONFLICT)
                .body("Username already exists: " + request.username());
        }
        String encodedPassword = passwordEncoder.encode(request.password());
        userRepository.save(new AppUser(request.username(), encodedPassword, "USER"));
        return ResponseEntity.status(HttpStatus.CREATED)
            .body("User registered: " + request.username());
    }

    // TODO Exercise 6: Implement the /auth/login endpoint.
    // 1. Call authenticationManager.authenticate(new UsernamePasswordAuthenticationToken(username, password))
    //    Catch BadCredentialsException and return HTTP 401 with {"error": "Invalid username or password"}
    // 2. On success, call jwtUtil.generateToken(request.username()) to get the token
    // 3. Return HTTP 200 with {"token": token, "username": username, "expiresIn": 86400000}
    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginRequest request) {
        return ResponseEntity.ok(Map.of("token", "not-implemented")); // TODO: implement
    }
}
