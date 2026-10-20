// Exercise 1 (expected): cargo build fails with E0277 — AppConfig doesn't
// derive Deserialize, so serde_json::from_str can't synthesize one.
// Exercise 2 adds `use serde::{Deserialize, Serialize};` + the derive attr.
// Exercise 3 adds field-level serde attributes (default, rename, skip).
// Exercise 4 round-trips through serde_json::to_string_pretty.
// Exercise 5 (optional) tries #[derive(Hash)] on a struct with f64 and
// observes why floats aren't Hash.

pub struct AppConfig {
    pub host: String,
    pub port: u16,
    pub debug: bool,
    pub api_key: String,
}

const SAMPLE_JSON: &str = r#"{
    "host": "127.0.0.1",
    "port": 8080,
    "debug": true,
    "api_key": "sk-DEMO-NOT-REAL"
}"#;

fn parse(json: &str) -> Result<AppConfig, serde_json::Error> {
    serde_json::from_str(json)
}

fn main() -> Result<(), serde_json::Error> {
    println!("derive-serde starter — fill in each exercise");
    let cfg = parse(SAMPLE_JSON)?;
    println!("parsed: {cfg:#?}");
    Ok(())
}
