// config-lib — placeholder stubs. Exercise 2 rewrites LoadError with
// thiserror; Exercise 3 writes the real load_config body.

use std::collections::HashMap;
use std::path::Path;

pub type Config = HashMap<String, String>;

#[derive(Debug)]
pub struct LoadError(pub String);

impl std::fmt::Display for LoadError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.0)
    }
}

impl std::error::Error for LoadError {}

/// Stub — Exercise 3 replaces with a real file+parse+validate implementation.
pub fn load_config(_path: &Path) -> Result<Config, LoadError> {
    Err(LoadError("load_config not implemented yet".into()))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn load_error_display() {
        let err = LoadError("placeholder".into());
        assert_eq!(format!("{err}"), "placeholder");
    }
}
