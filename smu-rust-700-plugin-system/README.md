# smu-rust-700-plugin-system (CAPSTONE)

Starter for Course 7 Lesson 15 — tie unsafe + FFI + macros into a plugin system.

Workspace layout:
- `plugin-api/` — shared trait, ABI version, declarative macro
- `plugin-macros/` — proc-macro crate for PluginRegistration
- `hello-plugin/` — sample cdylib plugin
- `host/` — binary that loads plugins via libloading

```
cargo build --release
cargo run --release --bin host
```

Exercises:
1. Smoke test — workspace builds, dylib produced.
2. Design the Plugin trait + FFI entry-point signatures.
3. Build the first plugin cdylib (hello-plugin).
4. Load the plugin from the host with libloading.
5. Reduce boilerplate with a declarative macro + a derive proc macro.
