# log-analyzer capstone starter

A six-exercise synthesis lab for Course 4. The starter ships:

- `fixtures/access.log` — 51 valid + 2 malformed lines (53 total).
- `LogEntry` struct + six function stubs under `#[allow(dead_code)]`:
  - `parse_line` — Exercise 2 (whitespace-split + parse status + latency).
  - `load_entries` — Exercise 2 (read file + filter_map parse_line).
  - `ok_entries` — Exercise 3 (status < 400 iterator chain).
  - `group_latencies_by_path` — Exercise 4 (HashMap group-by).
  - `per_path_stats` — Exercise 5 (count + avg + p95 per path).
  - `report` — Exercise 6 (formatted top-N table).

Smoke-test run:

```
cargo run -- fixtures/access.log
```

Expected: `line count: 53`.
