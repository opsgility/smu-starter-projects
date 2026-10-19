// config-lib: library crate used by the sibling `app` binary.
//
// You will design `LoadError` in Exercise 2 and implement `load_config` in Exercise 3.
// For now, both are stubs so the workspace compiles.

use std::collections::HashMap;
use std::path::Path;

/// A loaded configuration — a map of key → value.
pub type Config = HashMap<String, String>;

/// Error type returned by `load_config`.
///
/// EX 2: replace this placeholder with a `thiserror::Error` enum containing
/// `IoError(#[from] std::io::Error)`, `ParseError(String)`, and
/// `MissingKey { key: &'static str }`. Give each an `#[error("...")]` attribute.
#[derive(Debug)]
pub struct LoadError(pub String);

impl std::fmt::Display for LoadError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "config load error: {}", self.0)
    }
}

impl std::error::Error for LoadError {}

/// Read a key=value config file and return the parsed map.
///
/// EX 3: implement this with `std::fs::read_to_string(path)?` + parse each line
/// `key=value` (ignore blank + `#` lines) + verify `host` and `port` keys exist.
pub fn load_config(_path: &Path) -> Result<Config, LoadError> {
    Err(LoadError("load_config not implemented yet".to_string()))
}

#[cfg(test)]
mod tests {
    use super::*;

    // EX 2 adds a test here that constructs each `LoadError` variant and
    // asserts the `Display` text matches the `#[error("...")]` attribute.
    #[test]
    fn placeholder() {
        let err = LoadError("test".to_string());
        assert_eq!(format!("{err}"), "config load error: test");
    }
}
