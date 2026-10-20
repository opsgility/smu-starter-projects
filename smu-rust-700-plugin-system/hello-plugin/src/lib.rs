//! First plugin cdylib — exports the four required FFI entry points.
//!
//! Exercise 3 of Lesson 15 fills in the four #[unsafe(no_mangle)] extern "C" functions.
//! Exercise 5 refactors to use the plugin! declarative macro.

use plugin_api::PLUGIN_ABI_VERSION;
use std::os::raw::c_char;

#[unsafe(no_mangle)]
pub extern "C" fn plugin_abi_version() -> u32 {
    PLUGIN_ABI_VERSION
}

#[unsafe(no_mangle)]
pub extern "C" fn plugin_name() -> *const c_char {
    // Exercise 3: return a static nul-terminated byte sequence.
    static NAME: &[u8] = b"hello-plugin\0";
    NAME.as_ptr() as *const c_char
}

// Exercise 3: implement plugin_greet and plugin_free with #[unsafe(no_mangle)] pub extern "C" fn.
