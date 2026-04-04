package com.skillmeup.vaultly;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.provisioning.InMemoryUserDetailsManager;
import org.springframework.security.web.SecurityFilterChain;

@Configuration @EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/tasks").permitAll()
                .anyRequest().authenticated())
            .httpBasic(org.springframework.security.config.Customizer.withDefaults());
        return http.build();
    }

    // TODO Exercise 1: Add form login — replace .httpBasic() with .formLogin(withDefaults()).
    // Test by visiting http://localhost:8080/login in a browser.

    // TODO Exercise 2: Replace InMemoryUserDetailsManager with a database-backed UserDetailsService.
    // Create a User entity with username, password (BCrypt hashed), enabled fields.
    // Create a UserRepository extending JpaRepository<User, Long>.
    // Create a CustomUserDetailsService that implements UserDetailsService and loads users from the repo.

    @Bean
    public UserDetailsService users() {
        return new InMemoryUserDetailsManager(
            User.withDefaultPasswordEncoder().username("user1").password("password").roles("USER").build(),
            User.withDefaultPasswordEncoder().username("admin").password("adminpass").roles("ADMIN").build()
        );
    }
}
