# smu-rust-300-repository

Starter project for Course **SMU-RUST-300** Lesson 6 HOL — **Build a Repository trait with associated types**.

You will build a small type-system walk through Rust's associated-type + generic-parameter + PhantomData trio: design a `Repository` trait with an associated `Item` type, implement it for a generic `InMemoryRepo<T>`, then layer a type-state (`Anonymous` → `Authenticated`) pattern with `PhantomData<State>` so the compiler enforces an auth check.

## Files

- `Cargo.toml` — `repository`, edition 2024, no deps initially (Ex 4 + 5 stay dep-free).
- `src/main.rs` — scaffold with `InMemoryRepo<T>` + commented stubs for Ex 2 (trait), Ex 4 (tag structs + AuthRepo), Ex 5 (const-generic SizedRepo).
- `.gitignore` — standard Rust (`target/`, `Cargo.lock`).

## Run it

```
cargo run
```

Should print the welcome lines. Exercises 2-5 extend `main` as the trait + impls land.

## Per-exercise additions

| Ex | What you add | Where |
|---:|---|---|
| 1 | Nothing — just `cargo run` the smoke test | — |
| 2 | `trait Repository` with associated `Item` + required `add` / `get` + default `count` | top of `main.rs` |
| 3 | `impl<T> Repository for InMemoryRepo<T>` with `type Item = T` + `main` test calls | top of `main.rs` + bottom of `main` |
| 4 | `use std::marker::PhantomData;`, `struct Anonymous`, `struct Authenticated`, `struct AuthRepo<R, State>`, `.authenticate(self) -> AuthRepo<R, Authenticated>`, `.delete(..)` on only the authenticated form | module-level |
| 5 (optional) | `struct SizedRepo<T, const N: usize>` + `impl` + a usage in main | module-level |
