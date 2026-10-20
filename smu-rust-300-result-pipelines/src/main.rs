use std::collections::HashMap;

// Exercise 2: implement parse_port with .map_err
#[allow(dead_code)]
fn parse_port(_s: &str) -> Result<u16, String> {
    todo!("Exercise 2: fill this in")
}

// Helper used by load_port — returns the raw string value if present.
#[allow(dead_code)]
fn lookup_config<'a>(key: &str, data: &'a HashMap<String, String>) -> Option<&'a str> {
    data.get(key).map(String::as_str)
}

// Exercise 3: build load_port with .ok_or + .and_then
#[allow(dead_code)]
fn load_port(_data: &HashMap<String, String>) -> Result<u16, String> {
    todo!("Exercise 3: fill this in")
}

// Exercise 4: validate a batch with .collect::<Result<Vec<_>, _>>()
#[allow(dead_code)]
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

    // sample_config() is used by load_port in Exercise 3.
    let _config = sample_config();
    println!("sample config has keys: port, host");
}
