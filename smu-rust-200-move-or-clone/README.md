# Move or clone? Practice choosing

Starter for Course **SMU-RUST-200** (The Rust Ownership Model), the hands-on
paired lab for the "Values, moves, and Copy — in depth" teaching lesson.

The whole project is six broken Rust programs. Each one fails because of a
wrong move / clone / Copy / borrow choice. Your job is to decide which tool
Rust wants for the situation, apply the smallest fix, and watch the program
compile and print `caseNN passed`.

## Files

| Path | What it is |
|---|---|
| `Cargo.toml` | Workspace manifest, no external deps |
| `src/main.rs` | Lists the six cases + how to run them |
| `src/bin/case01.rs` | Use after move — needs `.clone()` **or** read via `&` |
| `src/bin/case02.rs` | Vec consumed by value — needs `&[T]` parameter |
| `src/bin/case03.rs` | Loop moves Strings out of Vec — needs `for name in &names` |
| `src/bin/case04.rs` | Shared borrow where exclusive is needed — needs `&mut` |
| `src/bin/case05.rs` | Idiom check — pass primitives by value, not by `&` |
| `src/bin/case06.rs` | Same String used in two calls — needs `.clone()` |

Each file has three comment headers at the top: **EXPECTED ERROR**, **HINT**,
and **FIX ME**. Read all three before touching the code.

## How to run a case

```
cargo run --bin case01
```

The first run will print a compiler error. Read the whole error — the Rust
compiler is unusually clear. Then apply the fix the comment hints at, save,
and re-run. When the program compiles cleanly and prints `caseNN passed`,
move to the next case.

## Where this fits

- **Course 1** (SMU-RUST-100) Lesson 12 gently introduced the move / Copy /
  clone vocabulary.
- **Course 2** (SMU-RUST-200) Lesson 2 "Values, moves, and Copy — in depth"
  made the trait rules precise.
- This lab trains the judgment of which tool to reach for in context, which
  is the real skill behind the ownership model.

Hollis Brennan — the mentor voice across the Rust skill path — will be on
your left-hand pane, holding back and letting you try. If you stall for more
than a few minutes, type a question into the LeftAgent and ask for a nudge.
