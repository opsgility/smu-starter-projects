//! SMU-RUST-700 Lesson 8 — Rust wrappers for the vendored C library.
//!
//! Exercises:
//! 1. Smoke test (gcc + cargo build).
//! 2. Wire up build.rs to compile csrc/calc.c.
//! 3. Declare the extern C block + CString/CStr conversion.
//! 4. Reorganize into a private ffi submodule exposing only safe wrappers.

// Exercise 3: declare the three C functions here.
// unsafe extern "C" {
//     pub fn calc_add(a: c_int, b: c_int) -> c_int;
//     pub fn calc_multiply(a: c_int, b: c_int) -> c_int;
//     pub fn calc_greeting(name: *const c_char) -> *const c_char;
// }

/// Exercise 3: wrap calc_add safely.
pub fn add(_a: i32, _b: i32) -> i32 {
    todo!("Exercise 3: call calc_add inside a one-line unsafe block")
}

/// Exercise 3: wrap calc_multiply safely.
pub fn multiply(_a: i32, _b: i32) -> i32 {
    todo!("Exercise 3: call calc_multiply inside a one-line unsafe block")
}

/// Exercise 3: wrap calc_greeting with CString/CStr.
pub fn greeting(_name: &str) -> Result<String, &'static str> {
    todo!("Exercise 3: CString::new(name) + unsafe calc_greeting + CStr::from_ptr")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn add_works() {
        assert_eq!(add(2, 3), 5);
    }

    #[test]
    fn multiply_works() {
        assert_eq!(multiply(4, 5), 20);
    }

    #[test]
    fn greeting_hello() {
        assert_eq!(greeting("world").unwrap(), "Hello, world!");
    }
}
