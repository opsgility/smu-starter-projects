fn main() {
    println!("borrow-checker 2.0 — 12 harder drills");
    println!();
    println!("Run each drill individually:");
    println!("  cargo run --bin drill01   # E0382 use-after-move inside a loop");
    println!("  cargo run --bin drill02   # E0505 move while borrowed");
    println!("  cargo run --bin drill03   # E0502 mut while shared (struct field)");
    println!("  cargo run --bin drill04   # E0499 two mut borrows (NLL fix)");
    println!("  cargo run --bin drill05   # E0596 method takes &self but needs &mut self");
    println!("  cargo run --bin drill06   # E0384 immutable binding (fix at the right line)");
    println!("  cargo run --bin drill07   # E0507 move out of Vec index");
    println!("  cargo run --bin drill08   # E0597 returning &str from local String");
    println!("  cargo run --bin drill09   # E0507 move out of struct field through &");
    println!("  cargo run --bin drill10   # E0382 move via into_iter() in a loop");
    println!("  cargo run --bin drill11   # E0499 across function calls (NLL ends borrow)");
    println!("  cargo run --bin drill12   # E0597 struct holds a reference, forces lifetime");
    println!();
    println!("Each drill ships broken on purpose. Read the compiler message and fix.");
}
