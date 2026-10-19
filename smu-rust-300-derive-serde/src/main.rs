// SMU-RUST-300 Lesson 8 HOL — Derive macros + serde in practice.
//
// The starter deliberately fails to compile. Exercise 2 adds the right
// `#[derive(...)]` + `use serde::...` lines to make this build and run.
//
// Scenario: Terrace Labs ships a tiny service with a config file. The config
// comes in as JSON on disk; the service wants a typed Rust struct it can read
// from. serde + the derive macros turn five lines of boilerplate into one.

const SAMPLE_JSON: &str = r#"{
    "host": "127.0.0.1",
    "port": 8080,
    "debug": true,
    "api_key": "sk-DEMO-NOT-REAL"
}"#;

// TODO (Exercise 2): add #[derive(...)] above this struct and
//                    `use serde::{Deserialize, Serialize};` at the top of the file.
pub struct AppConfig {
    pub host: String,
    pub port: u16,
    pub debug: bool,
    pub api_key: String,
}

fn parse(json: &str) -> Result<AppConfig, serde_json::Error> {
    serde_json::from_str(json)
}

fn main() {
    println!("derive-serde starter — fill in each exercise");
    match parse(SAMPLE_JSON) {
        Ok(cfg) => println!("parsed: {cfg:#?}"),
        Err(e) => eprintln!("parse error: {e}"),
    }
}
