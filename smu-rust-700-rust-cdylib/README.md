# smu-rust-700-rust-cdylib (mycalc)

Starter for Course 7 Lesson 10 — build a cdylib + generate C header + C driver.

```
cargo build --release
cbindgen --config cbindgen.toml --crate mycalc --output include/mycalc.h
```

Exercises:
1. Smoke test — gcc + cargo build succeed.
2. Set crate-type ["cdylib"] + add no_mangle extern "C" entries.
3. Generate the C header with cbindgen.
4. Compile the C driver + install catch_unwind panic boundaries.
