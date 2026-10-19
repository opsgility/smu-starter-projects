// Course 3 Lesson 2 paired HOL — build chained Option/Result pipelines
// with .map / .and_then / ? instead of nested matches.
//
// Each exercise fills in one of the stubs below. By the end you can read
// a port out of a HashMap-backed config, parse it, and validate a batch
// of CLI inputs — all with linear chained combinators.

use std::collections::HashMap;

// EX 2: implement using `.parse::<u16>().map_err(|e| format!("bad port: {e}"))`.
fn parse_port(_s: &str) -> Result<u16, String> {
    todo!("Exercise 2: fill this in")
}

// Looks up a key in the config map. Returns `None` if the key is absent.
// You will NOT change this fn — Exercise 3 CALLS it as part of the chain.
fn lookup_config<'a>(key: &str, data: &'a HashMap<String, String>) -> Option<&'a str> {
    data.get(key).map(|s| s.as_str())
}

// EX 3: build this with a chained .and_then / ? pipeline — no nested match.
fn load_port(_data: &HashMap<String, String>) -> Result<u16, String> {
    todo!("Exercise 3: fill this in")
}

// EX 4: implement with `.iter().map(|s| parse_port(s)).collect::<Result<Vec<_>, _>>()`.
fn validate_all(_ports: &[&str]) -> Result<Vec<u16>, String> {
    todo!("Exercise 4: fill this in")
}

fn sample_config() -> HashMap<String, String> {
    let mut m = HashMap::new();
    m.insert("port".to_string(), "8080".to_string());
    m.insert("host".to_string(), "localhost".to_string());
    m
}

fn main() {
    println!("result-pipelines starter — fill in each exercise");
    println!("sample config has keys: port, host");

    let config = sample_config();
    let _ = (parse_port, lookup_config, load_port, validate_all, config);
}
