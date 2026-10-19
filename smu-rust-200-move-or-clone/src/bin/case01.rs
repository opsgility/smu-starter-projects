// case01: Use after move.
//
// EXPECTED ERROR: E0382 — borrow of moved value: `greeting`.
// HINT: `greeting` is a String (non-Copy). The assignment `let louder = greeting;`
//       moves it into `louder`. The last `println!` tries to use `greeting`
//       after the move.
//
// FIX ME: pick ONE of these — do not do both.
//   a) Give `louder` its own copy with `.clone()` so `greeting` is still owned
//      afterwards.
//   b) Read the shouted version via `&louder` in the final println.
//
// Edit between the two `// --- fix below ---` markers only. The test harness
// at the bottom should print `case01 passed` and exit cleanly.

fn main() {
    let greeting = String::from("hello");

    // --- fix below ---
    let louder = greeting; // this moves `greeting` into `louder`
    // --- fix above ---

    println!("louder   = {}", louder);
    println!("greeting = {}", greeting);

    println!("case01 passed");
}
