package com.skillmeup.meridian.config;

import org.springframework.context.annotation.Configuration;

/**
 * Azure Application Insights telemetry configuration.
 *
 * TelemetryClient is auto-configured by applicationinsights-spring-boot-starter.
 * Simply inject TelemetryClient where needed — no manual bean creation required.
 */
@Configuration
public class TelemetryConfig {
    // TelemetryClient is auto-configured — inject directly in services
}
