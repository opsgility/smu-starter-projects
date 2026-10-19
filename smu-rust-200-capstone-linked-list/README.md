# SMU-RUST-200 Capstone — Convert a linked list from Box to Rc<RefCell>

Course 2 synthesis. You start with a correct `Box<Node>`-based singly-linked list and refactor it to `Rc<RefCell<Node>>` so two lists can share a tail subtree AND mutate the shared tail through either list.

## Files

- `Cargo.toml` — `capstone_linked_list`, Rust 2024 edition, no deps (pure std).
- `src/main.rs` — the Box-based list. Compiles and runs cleanly in the starter state.

## Run

```
cargo run
```

Starter output:

```
[1, 2, 3]
len() = 3
```

## What you build across the exercises

| Exercise | Addition |
|---:|---|
| 1 | Smoke test — run the Box-based starter and confirm the output. |
| 2 | Define `type Link = Option<Rc<RefCell<Node>>>` and refactor the struct + `push_front`. Output unchanged. |
| 3 | Add a second list that shares the tail of the first. Both lists print the shared tail. |
| 4 | Mutate the shared tail through list1; verify list2 sees the change. |
| 5 | Observe `Rc::strong_count()` on the shared node; pop list1's head and watch the count drop. |
| 6 | (Optional) Add an iterator over the Rc<RefCell>-based list. |

## Notes

Every change happens in `src/main.rs`. Nothing in `Cargo.toml` needs to change — no external dependencies.

Compiler errors along the way are expected during each exercise's refactor step. Read them, follow the `help:` suggestions, and the final state of each exercise should compile cleanly.
