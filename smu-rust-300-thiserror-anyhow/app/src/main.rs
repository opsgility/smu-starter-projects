// app: binary crate that uses `config_lib` as a library.
//
// EX 4: wire this main to accept a path from `std::env::args`, call
// `config_lib::load_config(path)` with `.context("loading config file")?`,
// and print the loaded Config.
//
// Keep the return type `anyhow::Result<()>` — anyhow handles any error that
// implements `std::error::Error`, which includes `config_lib::LoadError`.

use anyhow::Result;

fn main() -> Result<()> {
    println!("thiserror + anyhow starter — fill in Exercises 2-4 to make this useful.");
    Ok(())
}
