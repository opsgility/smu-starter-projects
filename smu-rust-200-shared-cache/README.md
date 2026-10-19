# Shared memoizing cache with Rc\<RefCell\>

Starter project for Course 2 (The Rust Ownership Model), Lesson 8 (Interior mutability — Cell, RefCell) hands-on lab.

The starter ships a slow recursive Fibonacci. The exercises convert it to a shared memoizing cache using `Rc<RefCell<HashMap<u64, u64>>>`, demonstrate shared ownership with two closures, trigger a `BorrowMutError`, and preview `Arc<Mutex<T>>` for threads.

## Run

```
cargo run
```

You'll see each `fib(n)` call take progressively longer — exponential, no memoization. Exercises 2–5 change that.

## Files

| Path | Role |
|---|---|
| `src/main.rs` | Slow recursive Fibonacci + timing loop. You edit this across all 5 exercises. |
| `Cargo.toml` | Package manifest. No dependencies. |

## Per-exercise additions

| Exercise | Adds |
|---|---|
| 1 | Smoke test — observe exponential slowdown |
| 2 | `Cache = Rc<RefCell<HashMap<u64, u64>>>` + memoized `fibonacci(n, cache)` |
| 3 | Two closures sharing one `Rc::clone`-d cache |
| 4 | Intentional `BorrowMutError` panic, then scoped fix |
| 5 (optional) | Replace Rc<RefCell> with Arc<Mutex> and move across threads |

## Notes

- Everything is std-only. No `cargo add` needed.
- Exercise 4's panic is intentional — the point is to see the runtime check that `RefCell` enforces, which the compile-time borrow checker would have caught had you not used interior mutability.
- Hollis Brennan is your mentor on this lab (the recurring Rust-mentor voice across Courses 1–7).
