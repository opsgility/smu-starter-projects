mod types;
pub use types::Station;

use std::collections::HashMap;

fn main() {
    let registry: HashMap<String, Station> = HashMap::new();
    println!(
        "single-threaded registry stub — go to Exercise 2 to protect it with Arc<Mutex<_>>  (entries: {})",
        registry.len()
    );
}
