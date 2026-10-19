// borrows_practice — Course 638 Lesson 3 paired HOL
//
// This default binary just prints the drill menu. The exercises walk the
// student through each `drill01.rs` through `drill05.rs` binary one at a
// time; run them with:
//
//     cargo run --bin drill01
//     cargo run --bin drill02
//     ...
//
// See README.md for the exercise sequence.

fn main() {
    println!("borrows practice — pick a drill:");
    println!("  cargo run --bin drill01   # shared vs mutable borrows + E0502 break");
    println!("  cargo run --bin drill02   # split borrows across struct fields");
    println!("  cargo run --bin drill03   # NLL — borrow ends at last use");
    println!("  cargo run --bin drill04   # reborrow — pass &mut *outer, keep outer");
    println!("  cargo run --bin drill05   # fix iterator invalidation with collect-then-push");
}
