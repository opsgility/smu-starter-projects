//! SMU-RUST-700 Lesson 14 — proc macro crate for #[derive(Builder)].
//!
//! Exercises:
//! 1. Smoke test — workspace builds (consumer tests fail — expected).
//! 2. Scaffold the proc-macro crate (add syn/quote imports + parse DeriveInput).
//! 3. Parse the struct's fields with syn.
//! 4. Emit the builder with quote! + verify consumer tests pass.

use proc_macro::TokenStream;

#[proc_macro_derive(Builder)]
pub fn derive_builder(_input: TokenStream) -> TokenStream {
    // Exercise 2+3+4: replace this empty stub with real parsing + emission.
    TokenStream::new()
}
