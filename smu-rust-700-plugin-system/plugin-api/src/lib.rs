//! Shared plugin interface — ABI version + Plugin trait + FFI entry-point signatures.
//!
//! Exercise 2 of Lesson 15 will populate this with real content.

/// Plugin ABI version. Increment on breaking changes.
pub const PLUGIN_ABI_VERSION: u32 = 1;

pub const PLUGIN_OK: i32 = 0;
pub const PLUGIN_ERR: i32 = -1;

/// Trait each plugin implements (internal — not FFI).
pub trait Plugin {
    fn name(&self) -> &'static str;
    fn greet(&self, input: &str) -> String;
}

// Exercise 5: add the `plugin!` declarative macro here.
