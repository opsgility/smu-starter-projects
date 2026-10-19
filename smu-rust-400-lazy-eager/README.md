# smu-rust-400-lazy-eager

Starter for Course 4 Lesson 6 — **Measure lazy vs eager — iterator benchmarks**.

Iterator chains in Rust are lazy; `.collect()` is where allocations happen. In this lab you'll measure the actual cost of a wasteful intermediate `.collect()` vs a single-pass equivalent, then look at the cases where `.collect()` is actually load-bearing.

## Files

| Path | Role |
|---|---|
| `Cargo.toml` | `lazy_eager`, edition 2024, pure std — no external deps |
| `src/main.rs` | `gen_vec`, two sum stubs (`wasteful_sum`, `direct_sum`), a `time()` helper, and a stub `main` |
| `README.md` | this file |

## Run

```bash
cargo run
```

You should see:

```
lazy-eager starter — fill in each exercise
gen_vec(10) first 5 = [0, 1, 2, 3, 4]
```

The two sum stubs panic with `todo!()` — the exercises fill them in. Build in `--release` when you measure (Exercise 3) so the optimizer actually does its job.

## Per-exercise additions

| Exercise | Adds / changes |
|---|---|
| **1. Smoke test** | Confirm `cargo build` + `cargo run` work |
| **2. Fill both sum stubs** | `wasteful_sum`, `direct_sum`, call both from `main` under `time()` |
| **3. Measure at four N values** | Loop N over [10, 1_000, 100_000, 10_000_000], record ratios in `NOTES.md` |
| **4. `needs_vec`** | Function that returns `(Vec<i32>, usize)` — can't be done without `.collect()` |
| **5. (Optional) collect-for-borrow** | Collect `&str` into `Vec<&str>` to pass to a slice-taking fn |
