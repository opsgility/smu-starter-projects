//! SMU-RUST-700 Lesson 10 — expose Rust functions to C via a cdylib.
//!
//! Exercises:
//! 1. Smoke test (verify gcc + cbindgen + build).
//! 2. Set crate-type = ["cdylib"] and add two #[no_mangle] extern "C" functions.
//! 3. Generate the C header with cbindgen.
//! 4. Compile the C driver + add catch_unwind panic boundaries.

// Exercise 2: add two #[no_mangle] extern "C" entry points here:
//   - mycalc_add(a: c_int, b: c_int) -> c_int
//   - mycalc_name_length(name_ptr: *const c_char) -> c_int

#[cfg(test)]
mod tests {
    #[test]
    fn placeholder() {
        // Smoke test placeholder — real functionality lands in Exercises 2-4.
        assert_eq!(2 + 2, 4);
    }
}
