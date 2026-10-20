# smu-rust-700-raw-ptr-list

Starter for Course 7 Lesson 4 — build a singly-linked list with raw pointers + NonNull.

```
cargo build
cargo test
```

Exercises:
1. Smoke test.
2. Implement `push` using Box::into_raw.
3. Implement `pop` + the iterator.
4. Add Drop + Send + Sync impls with SAFETY comments.
