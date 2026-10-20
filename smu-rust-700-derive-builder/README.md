# smu-rust-700-derive-builder

Starter for Course 7 Lesson 14 — write a #[derive(Builder)] proc macro.

```
cargo build
cargo test -p consumer
```

Exercises:
1. Smoke test — workspace builds.
2. Scaffold the proc-macro crate.
3. Parse DeriveInput with syn.
4. Emit the builder with quote! and verify.
