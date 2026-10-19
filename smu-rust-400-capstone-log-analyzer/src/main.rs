use std::collections::HashMap;
use std::env;
use std::fs;
use std::io;

#[derive(Debug, Clone)]
#[allow(dead_code)]
pub struct LogEntry {
    pub timestamp: String,
    pub method: String,
    pub path: String,
    pub status: u16,
    pub latency_ms: u32,
}

/// Parse a single log line into a LogEntry.
///
/// Expected format (whitespace-separated, 5 fields):
///   <timestamp> <method> <path> <status> <latency_ms>
///
/// Example line:
///   2026-10-19T14:00:01Z GET /api/users 200 42
///
/// Return `None` if the line is malformed (missing fields, non-numeric
/// status, non-numeric latency). You will implement this in Exercise 2.
pub fn parse_line(_line: &str) -> Option<LogEntry> {
    None
}

/// Read a log file and return a Vec of successfully-parsed entries.
/// Malformed lines are silently dropped via filter_map.
///
/// You will implement this in Exercise 2.
pub fn load_entries(_path: &str) -> io::Result<Vec<LogEntry>> {
    Ok(Vec::new())
}

/// Return only entries whose HTTP status is < 400 (success + redirect).
/// You will implement this in Exercise 3.
#[allow(dead_code)]
pub fn ok_entries(entries: &[LogEntry]) -> impl Iterator<Item = &LogEntry> {
    entries.iter()
}

/// Group latency samples by request path.
/// You will implement this in Exercise 4.
#[allow(dead_code)]
pub fn group_latencies_by_path(_entries: &[LogEntry]) -> HashMap<&str, Vec<u32>> {
    HashMap::new()
}

/// Compute (path, count, avg_ms, p95_ms) per path, sorted by count descending.
/// You will implement this in Exercise 5.
#[allow(dead_code)]
pub fn per_path_stats(_entries: &[LogEntry]) -> Vec<(String, usize, f64, u32)> {
    Vec::new()
}

/// Print the top-N report. You will implement this in Exercise 6.
#[allow(dead_code)]
pub fn report(_entries: &[LogEntry], _top_n: usize) {
    println!("report: implement me in Exercise 6");
}

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    let path = args.get(1).map(String::as_str).unwrap_or("fixtures/access.log");

    println!("log-analyzer starter — see README.md");
    println!("reading from: {path}");

    let raw_lines = fs::read_to_string(path)?;
    let line_count = raw_lines.lines().count();
    println!("line count: {line_count}");

    Ok(())
}
