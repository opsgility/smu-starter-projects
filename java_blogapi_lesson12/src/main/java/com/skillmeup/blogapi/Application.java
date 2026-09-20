package com.skillmeup.blogapi;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

// TODO Exercise 1: Add @EnableJpaAuditing here to activate Spring Data JPA auditing.
@SpringBootApplication
@EnableJpaAuditing
public class Application {
    public static void main(String[] args) { SpringApplication.run(Application.class, args); }
}
