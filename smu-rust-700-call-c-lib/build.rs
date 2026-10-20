//! SMU-RUST-700 Lesson 8 — build.rs that compiles csrc/calc.c via the cc crate.
//!
//! Exercise 2: replace this stub with a working cc::Build invocation.

fn main() {
    println!("cargo:warning=TODO (Exercise 2): compile csrc/calc.c with the cc crate.");
    // Rerun this build.rs if csrc/ changes, so the student doesn't have to
    // `touch build.rs` each time they edit the C sources during Exercise 2.
    println!("cargo:rerun-if-changed=csrc/calc.c");
    println!("cargo:rerun-if-changed=csrc/calc.h");
}
