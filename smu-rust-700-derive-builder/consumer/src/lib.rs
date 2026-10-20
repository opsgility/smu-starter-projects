//! Consumer tests for the Builder derive macro.
//!
//! All tests fail until the macro is fully implemented.

use mymacros::Builder;

#[derive(Builder)]
#[allow(dead_code)]
pub struct Config {
    pub host: String,
    pub port: u16,
    pub timeout: u32,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn builder_builds_full_config() {
        let cfg = Config::builder()
            .host("localhost".to_string())
            .port(8080)
            .timeout(30)
            .build()
            .unwrap();
        assert_eq!(cfg.host, "localhost");
        assert_eq!(cfg.port, 8080);
        assert_eq!(cfg.timeout, 30);
    }

    #[test]
    fn builder_missing_field_errors() {
        let result = Config::builder()
            .host("localhost".to_string())
            .port(8080)
            .build();
        assert!(result.is_err());
    }
}
