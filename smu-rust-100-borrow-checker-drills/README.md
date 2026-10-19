# SMU-RUST-100 Lesson 12 — Fix the borrow checker

Twelve small broken Rust programs. Each one triggers exactly one borrow-checker
or ownership error from Lesson 12. Your job: read the compiler message, locate
the problem line, apply the smallest fix, re-run until each one prints
`drill NN passed`.

The point is not to invent new programs. The point is to get comfortable
reading Rust's error messages and recognising the fix pattern they're pointing
at — because 90% of the "I'm fighting the borrow checker" days you'll have in
Rust look exactly like these drills.

## Scenario

You're pairing with Hollis Brennan, the Rust mentor from the Course 1 teaching
lessons. Hollis has handed you a folder of twelve broken programs from a
colleague's PR review. "The compiler is already telling us what's wrong," Hollis
says. "Walk through each one, read what rustc says, apply the fix. By the end,
you'll trust the compiler as a teaching tool."

## Files

```
smu-rust-100-borrow-checker-drills/
  README.md                        # this file
  .gitignore                       # target/, Cargo.lock, editor noise
  Cargo.toml                       # package 'borrow_checker_drills', edition 2024, std-only
  src/
    main.rs                        # welcome print — not where the exercises live
    bin/
      drill01.rs                   # E0382 — use of moved value
      drill02.rs                   # E0384 — cannot assign twice to immutable
      drill03.rs                   # E0596 — cannot borrow immutable as mutable
      drill04.rs                   # E0502 — cannot borrow mutable while borrowed
      drill05.rs                   # E0507 — cannot move out of index
      drill06.rs                   # E0505 — cannot move out of borrowed
      drill07.rs                   # E0382 — moved into function on first call
      drill08.rs                   # E0596 — Vec::sort needs mut Vec
      drill09.rs                   # E0382 — fn takes Vec by value instead of by reference
      drill10.rs                   # E0499 — two active &mut borrows
      drill11.rs                   # E0597 — borrowed value does not live long enough
      drill12.rs                   # E0308 — mismatched types, &str vs String
```

## How to run

Each drill is its own binary under `src/bin/`. Run them one at a time:

```
cargo run --bin drill01
cargo run --bin drill02
...
cargo run --bin drill12
```

Each one will fail to compile until you fix it. Rust's error output tells you
the exact file + line + error code. The expected success output for every drill
is a single line ending in `drill NN passed` (where NN is the two-digit drill
number).

## Reading a compiler error

Rust compiler errors have four parts you care about:

1. **The error code** — `error[E0382]` for example. Each code has a specific
   fix pattern. Each drill in this project tells you which code you'll see.
2. **The one-line summary** — `use of moved value: 's'` tells you exactly
   what Rust is complaining about.
3. **The source line with carets `^^^^^`** — the exact character range of
   the problem.
4. **The `help:` note** — Rust often tells you the fix. Read it last so you
   can first try the fix on your own, but definitely read it before changing
   files you weren't planning to touch.

## Hollis's rule

If you have to change more than one line to fix a drill, you've over-corrected.
Each drill has a one-line fix. The hint comment at the top of every drill names
the smallest change that works — treat it as the escalation ladder's "Guide"
step. Try the fix on your own first; drop to the hint if you're stuck for more
than two minutes.

## Notes

- Zero external dependencies. Everything compiles against std under Rust 2024
  / stable 1.99.1.
- Fixing drill N does NOT depend on drill N-1 compiling. The drills are fully
  independent, so you can tackle them in any order.
- If `cargo run --bin drillNN` prints `drill NN passed`, that drill is done.
  Move to the next one.
