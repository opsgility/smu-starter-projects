//! Procedural macro crate for the plugin system.
//!
//! Exercise 5 adds a #[derive(PluginRegistration)] macro.

use proc_macro::TokenStream;

#[proc_macro_derive(PluginRegistration)]
pub fn derive_registration(_input: TokenStream) -> TokenStream {
    // Exercise 5: parse DeriveInput and emit a registration_info() method.
    TokenStream::new()
}
