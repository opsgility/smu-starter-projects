package com.skillmeup.vaultly;

// TODO Exercise 1: Add spring-boot-starter-security to pom.xml (the dependency is already listed — just uncomment it).
// After adding the dependency, ALL endpoints will require HTTP Basic auth automatically.

// TODO Exercise 2: Create a SecurityConfig class with @Configuration and @EnableWebSecurity.
// Inject a SecurityFilterChain bean that:
//   - Permits GET /api/tasks without authentication (permitAll)
//   - Requires authentication for POST, DELETE
//   - Enables HTTP Basic

// TODO Exercise 3: Add an InMemoryUserDetailsManager bean with two users:
//   user: username="user1" password="{noop}password" roles="USER"
//   admin: username="admin" password="{noop}adminpass" roles="ADMIN"
// {noop} means no password encoding — only for development/learning!

// Placeholder so project compiles (remove when you add spring-boot-starter-security):
public class SecurityConfig { }
