package com.skillmeup.vaultly;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.provisioning.InMemoryUserDetailsManager;
import org.springframework.security.web.SecurityFilterChain;

@Configuration @EnableWebSecurity
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.csrf(c -> c.disable())
            .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(a -> a
                .requestMatchers("/auth/**").permitAll()
                .anyRequest().authenticated())
            .httpBasic(org.springframework.security.config.Customizer.withDefaults());
        // TODO Exercise 2: Add JwtAuthenticationFilter before UsernamePasswordAuthenticationFilter
        // .addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class)
        return http.build();
    }
    @Bean public InMemoryUserDetailsManager users() {
        return new InMemoryUserDetailsManager(
            User.withDefaultPasswordEncoder().username("user1").password("password").roles("USER").build(),
            User.withDefaultPasswordEncoder().username("admin").password("adminpass").roles("ADMIN").build()
        );
    }
    @Bean public AuthenticationManager authManager(AuthenticationConfiguration config) throws Exception {
        return config.getAuthenticationManager();
    }
}
