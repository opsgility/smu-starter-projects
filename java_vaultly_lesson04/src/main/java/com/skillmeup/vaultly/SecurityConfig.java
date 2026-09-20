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

    // TODO Exercise 1: Create AppUser.java entity (@Entity, @Table(name="app_users"), id/username/password/role fields)
    // TODO Exercise 1: Create AppUserRepository.java (extends JpaRepository<AppUser, Long>, findByUsername method)

    // TODO Exercise 2: Create CustomUserDetailsService.java implementing UserDetailsService
    //   - @Service annotation
    //   - loadUserByUsername() looks up AppUser from AppUserRepository, returns Spring Security User
    //   - Throw UsernameNotFoundException if user is not found

    // TODO Exercise 3: Remove InMemoryUserDetailsManager bean below.
    //   - Add CustomUserDetailsService field (constructor inject)
    //   - Add .userDetailsService(customUserDetailsService) to filterChain
    //   - Add PasswordEncoder @Bean returning new BCryptPasswordEncoder()
    //   - Add AuthenticationManager @Bean via AuthenticationConfiguration
    //   - Add .requestMatchers("/auth/**").permitAll() to filterChain

    // TODO Exercise 4: Create RegisterRequest.java record (username, password fields)
    // TODO Exercise 4: Create AuthController.java with POST /auth/register
    //   - Check for duplicate usernames (return 409 Conflict)
    //   - Encode password with passwordEncoder.encode() before saving

    @Bean
    public UserDetailsService users() {
        return new InMemoryUserDetailsManager(
            User.withDefaultPasswordEncoder().username("user1").password("password").roles("USER").build(),
            User.withDefaultPasswordEncoder().username("admin").password("adminpass").roles("ADMIN").build()
        );
    }
}
