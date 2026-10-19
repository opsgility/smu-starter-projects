# Shared vs exclusive borrows practice — starter

Course: **The Rust Ownership Model** (SMU-RUST-200), Lesson 3 paired hands-on.

You just finished the teaching lesson *References and borrowing — the full picture*. This lab turns that into muscle memory: five small drills, each exercising one of the borrow patterns from the lesson.

## Files you'll touch

```
smu-rust-200-borrows-practice/
├── Cargo.toml
├── README.md
└── src/
    ├── main.rs          # prints the drill menu
    └── bin/
        ├── drill01.rs   # shared vs mutable + the E0502 break
        ├── drill02.rs   # split borrows across struct fields
        ├── drill03.rs   # NLL — borrow ends at last use
        ├── drill04.rs   # reborrow — pass `&mut *outer`, keep outer
        └── drill05.rs   # fix iterator invalidation with collect-then-push
```

Four of the five drills ship compiling. Drill 5 is intentionally broken — you fix it in the last exercise.

## How to run

```
cargo build --bins
cargo run --bin drill01
cargo run --bin drill02
cargo run --bin drill03
cargo run --bin drill04
cargo run --bin drill05
```

Each passing drill prints `drillNN passed` on the last line.

## What each drill is practicing

| Drill | Pattern | Error you'll see on break |
|-------|---------|---------------------------|
| 01    | Shared borrow + mutable borrow in sequence (fine), overlapping (E0502) | E0502 |
| 02    | Split borrows across struct fields (always compiles) | — |
| 03    | NLL: borrow ends at last use, not scope end | — |
| 04    | Reborrow: `&mut *outer` lets inner fn work, outer stays usable | — |
| 05    | Iterator invalidation + collect-then-push fix | E0502 |

## What's deliberately NOT here

- Lifetimes with explicit `'a` syntax — that's Lesson 6.
- Smart pointers (`Rc`, `RefCell`) — those are Lessons 7 and 8.

Stay focused on `&T` and `&mut T` today.
