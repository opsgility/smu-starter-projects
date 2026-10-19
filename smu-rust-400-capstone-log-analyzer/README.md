# smu-rust-400-capstone-log-analyzer

Course 4 capstone — streaming log analyzer built from iterator chains.

Student reads NGINX-style access log lines, parses each into a `LogEntry`, filters
by status, groups by path, computes per-path stats (count, average + p95 latency),
and prints a top-N report. Every stage is an iterator chain; `Vec` allocations
only when load-bearing.

## Files you get

| Path | What it is |
|---|---|
| `Cargo.toml` | Pure-std project, edition 2024, no dependencies. |
| `src/main.rs` | `LogEntry` struct, `parse_line`, `load_entries`, `ok_entries`, `group_latencies_by_path`, `per_path_stats`, `report` — all stubs. |
| `fixtures/access.log` | ~53 lines of synthetic log data with 7 distinct paths, varied statuses (200 / 201 / 401 / 403 / 404 / 500), and two intentionally malformed lines. |
| `.gitignore` | Standard Rust ignores. |

## How to run

```
cargo run -- fixtures/access.log
```

The starter prints the line count. You will build up to a top-N report
across six exercises:

| Exercise | Addition |
|---|---|
| 1 | Smoke test — read the file, print the raw line count. |
| 2 | Implement `parse_line` + wire `load_entries`; print the first three parsed entries with `{:#?}`. |
| 3 | Implement `ok_entries` — filter to entries with `status < 400`. |
| 4 | Implement `group_latencies_by_path` — fold entries into `HashMap<&str, Vec<u32>>`. |
| 5 | Implement `per_path_stats` — `(path, count, avg, p95)` sorted by count desc. |
| 6 | Implement `report` — formatted top-N table, invoke from `main`. |

## Log line format

Each valid line is five whitespace-separated fields:

```
<timestamp> <method> <path> <status> <latency_ms>
```

Example:

```
2026-10-19T14:00:01Z GET /api/users 200 42
```

Lines with fewer fields, non-numeric `status`, or non-numeric `latency_ms`
are malformed. `.filter_map(parse_line)` drops them.

## Notes

- Rust 1.99.1 stable, 2024 edition.
- No external crates — everything is `std`.
- Hollis Brennan's final appearance as mentor is at the end of Exercise 6,
  with the hand-off to Phase 2 (Courses 5, 6, 7).
