# smart-pointers starter

You will fill three sections of `src/main.rs` across the exercises:

- **SECTION 1 — Tree with Box.** Define a recursive `Tree` enum with
  `Leaf(i32)` and `Node(Box<Tree>, Box<Tree>)` variants, a `sum_tree`
  helper, and build + sum a small balanced tree.
- **SECTION 2 — Shared files with Rc.** Define a `File` struct, create three
  files wrapped in `Rc<File>`, and build two directories (`Vec<Rc<File>>`)
  that share one file between them.
- **SECTION 3 — Threads with Arc.** Wrap a file in `Arc<File>`, spawn a
  thread, clone the Arc across the boundary, and verify the main thread
  still sees the file after `.join()`.

Run `cargo run` after each section to confirm the output grows as the
exercises intend. The optional benchmark exercise appends an `Rc::clone` vs
`Arc::clone` timing loop to the end of `main`.
