package com.skillmeup.freightflow.config;

import com.github.benmanes.caffeine.cache.Caffeine;
import org.springframework.cache.CacheManager;
import org.springframework.cache.caffeine.CaffeineCacheManager;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import java.util.concurrent.TimeUnit;

/**
 * Cache configuration using Caffeine.
 *
 * TODO Exercise 3: Uncomment and configure the CacheManager bean
 * TODO Exercise 2 (in Application.java): Add @EnableCaching
 */
@Configuration
public class AppConfig {

    // TODO Exercise 3: Uncomment this bean and configure maximumSize=1000, expireAfterWrite=5m
    // @Bean
    // public CacheManager cacheManager() {
    //     CaffeineCacheManager manager = new CaffeineCacheManager();
    //     manager.setCaffeine(Caffeine.newBuilder()
    //         .maximumSize(1000)
    //         .expireAfterWrite(5, TimeUnit.MINUTES)
    //         .recordStats()
    //     );
    //     return manager;
    // }
}
