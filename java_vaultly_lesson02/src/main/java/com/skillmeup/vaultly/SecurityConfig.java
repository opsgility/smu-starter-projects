package com.skillmeup.vaultly;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;

// TODO Exercise 2: Add @Configuration and @EnableWebSecurity annotations to this class.
// TODO Exercise 2: Define a SecurityFilterChain bean that:
//   - Permits GET /api/tasks without authentication (permitAll)
//   - Requires authentication for all other requests
//   - Enables HTTP Basic
// TODO Exercise 3: Add a PasswordEncoder bean returning new BCryptPasswordEncoder()
// TODO Exercise 3: Add an InMemoryUserDetailsManager bean with two BCrypt-encoded users:
//   - username="user"  password=encoder.encode("password")  roles="USER"
//   - username="admin" password=encoder.encode("admin")      roles="ADMIN"
public class SecurityConfig {
    // TODO: implement
}
