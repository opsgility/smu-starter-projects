# SMU-RUST-200 Lesson 1 — Trace an ownership story

A tiny Rust program with 5 commented SCENES that walk through the operations ownership touches: value creation (Copy and non-Copy), moves, borrows, clones, and scope-end drops. Across the paired lab's exercises you'll annotate each scene with what it does, then intentionally break SCENE B by using a moved value, then fix it with `.clone()`.

## Scenario

Hollis Brennan handed you a small warm-up: a 20-line program that touches every ownership operation Course 2 Lesson 1 introduced. Your job is to read it carefully, name what each line does, and prove to yourself the rules by making the program fail — then make it succeed.

## Files

```
smu-rust-200-ownership-story/
  Cargo.toml            # package manifest, edition 2024, no deps
  src/
    main.rs             # 5 SCENES to annotate, Ex 3 uncomments a broken TRY line
  README.md
  .gitignore
```

## How to run

```
cargo run
```

Should print SCENE A through SCENE E lines and the "End of main" footer.

## Notes

- `edition = "2024"` — matches the vscode-rust container's default toolchain.
- No `[dependencies]` — pure std. All exercise additions stay std-only.
- `cargo build` and `cargo run` work out of the box.
