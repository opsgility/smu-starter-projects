# smu-rust-700-call-c-lib

Starter for Course 7 Lesson 8 — call a C library from Rust.

```
cargo build
cargo test
```

Exercises:
1. Smoke test — verify gcc + starter files.
2. Compile csrc/calc.c via build.rs + cc crate.
3. Declare extern "C" block + CString/CStr conversion.
4. Reorganize into a private `ffi` submodule.
