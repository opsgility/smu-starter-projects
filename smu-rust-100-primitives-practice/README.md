# SMU-RUST-100 Lesson 2 paired HOL — Values, types, and variables practice

A pure-practice starter that exercises the Rust type system and binding mechanics covered in Lesson 2 of the *Programming Foundations with Rust* course. There is no narrative here and no cloud backing — the student declares variables of each primitive type, moves between `String` and `&str`, shadows a variable to change its type, and observes integer overflow behavior in debug vs release builds. All code lives in a single `src/main.rs` divided into four commented sections.

## Scenario

Hollis Brennan hands the student a scratch pad: "Lesson 2 is a lot of syntax rules all at once. The only way they stick is to type each one out at least once." Each exercise fills in one of the four sections below.

## Files

```
smu-rust-100-primitives-practice/
  README.md
  Cargo.toml                     # package name "primitives_practice", edition 2024, no deps
  .gitignore                     # /target, Cargo.lock
  src/
    main.rs                      # welcome print + 4 commented section stubs students fill in
```

## How to run

1. Open the folder in VS Code (it opens automatically in the lab container).
2. From the integrated terminal, run:

    cargo run

   You should see:

       primitives starter — fill in each section as you work through the exercises

3. As you complete each exercise, re-run `cargo run` to see the output grow.

## Sections

- **SECTION 1 — integer types** (Exercise 2). Declare `i8`, `i32`, `u64`, `usize` variables, print each with `{}` and `{:?}`. Trip the compile error with an out-of-range literal, then fix it.
- **SECTION 2 — floats, bool, char** (Exercise 3). Declare and print one of each.
- **SECTION 3 — strings** (Exercise 3). Build a `String` three different ways, borrow it as `&str`, and print both forms.
- **SECTION 4 — shadowing** (Exercise 4). Shadow a `&str` into an `i32`. Then try the same with a mutable rebind and read the compiler error.
- **Optional — overflow** (Exercise 5). Trigger `attempt to add with overflow` in debug mode, then rebuild `--release` and watch the value wrap.

## Notes

- No external dependencies. Everything is in `std`.
- The lab container ships Rust 1.99.1 with the 2024 edition toolchain — no setup needed.
- If `cargo run` fails to find a target, confirm the terminal's working directory is the project root (where `Cargo.toml` lives).
