use std::collections::HashMap;
use std::env;
use std::fs;
use std::io;

#[derive(Debug, Clone)]
pub struct LogEntry {
    pub timestamp: String,
    pub method: String,
    pub path: String,
    pub status: u16,
    pub latency_ms: u32,
}

// Exercise 2 fills these.
#[allow(dead_code)]
pub fn parse_line(_line: &str) -> Option<LogEntry> {
    todo!("Exercise 2: split line into 5 fields, parse status + latency_ms")
}

#[allow(dead_code)]
pub fn load_entries(_path: &str) -> io::Result<Vec<LogEntry>> {
    todo!("Exercise 2: read_to_string + .lines().filter_map(parse_line).collect()")
}

// Exercise 3 fills this.
#[allow(dead_code)]
pub fn ok_entries<'a>(_entries: &'a [LogEntry]) -> impl Iterator<Item = &'a LogEntry> {
    std::iter::empty()
    // todo!("Exercise 3: entries.iter().filter(|e| e.status < 400)")
}

// Exercise 4 fills this.
#[allow(dead_code)]
pub fn group_latencies_by_path(_entries: &[LogEntry]) -> HashMap<&str, Vec<u32>> {
    todo!("Exercise 4: HashMap::entry + .or_insert_with(Vec::new).push(latency)")
}

// Exercise 5 fills this.
#[allow(dead_code)]
pub fn per_path_stats(_entries: &[LogEntry]) -> Vec<(String, usize, f64, u32)> {
    todo!("Exercise 5: group → compute count + avg + p95 → sort by count desc")
}

// Exercise 6 fills this.
#[allow(dead_code)]
pub fn report(_entries: &[LogEntry], _top_n: usize) {
    todo!("Exercise 6: print formatted table with aligned columns")
}

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    let path = args.get(1).map(String::as_str).unwrap_or("fixtures/access.log");

    println!("log-analyzer starter — see README.md");
    println!("reading from: {path}");

    let raw = fs::read_to_string(path)?;
    let count = raw.lines().count();
    println!("line count: {count}");

    Ok(())
}
