# smart-pointers (Course 2, Lesson 7 paired HOL)

Starter for `Trees with Box, graphs with Rc - Lab Exercises` (lab 3276) in
`SMU-RUST-200 The Rust Ownership Model`.

You build three small data structures across the exercises, each picked to
force a different smart-pointer choice:

| Section | Smart pointer | What you build |
|---|---|---|
| 1 | `Box<T>` | A binary tree where each node owns its two children. |
| 2 | `Rc<T>` | A shared-file structure where directories share `File`s without cloning the contents. |
| 3 | `Arc<T>` | The same file structure, moved across a thread boundary. |
| 4 (optional) | Rc vs Arc timing | A trivial counter benchmark showing the atomic-op cost of Arc. |

## Run it

```
cargo run
```

The starter prints:

```
smart-pointers starter — see README.md
```

Each exercise appends code to the three `SECTION` comments in `src/main.rs`
and extends the output.

## Per-exercise additions

| Exercise | Section touched | Adds |
|---|---|---|
| 1 | — | smoke test only |
| 2 | SECTION 1 | `enum Tree`, 7-node balanced tree, `sum_tree` + total print |
| 3 | SECTION 2 | `struct File`, `Vec<Rc<File>>` directories, `Rc::strong_count` observation |
| 4 | SECTION 3 | Arc-wrapped file, `std::thread::spawn` + `join`, verification print |
| 5 | end of main | optional benchmark counting single-thread Rc clones vs Arc clones |

## Notes

- Pure std — no deps in `Cargo.toml`. Course 1 taught `cargo add`; this lab
  stays std-only on purpose so you focus on the smart-pointer choice.
- Keep the three sections visually separated so you can read your main as a
  three-act program.
- For Section 3 (Arc + thread), the compiler will reject `Rc<File>` across
  the thread boundary (`Rc` is not `Send`). That reject IS the point — it's
  why `Arc` exists.
