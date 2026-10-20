// EXPECTED ERROR: E0382 — borrow of moved value: `greeting`
// HINT: `let louder = greeting;` moves `greeting` into `louder`. The later
//       `println!("{}", greeting)` then uses a moved value. The smallest fix
//       is to clone on the move so both bindings own their own String — but
//       the idiomatic fix is to print `louder` or borrow with `&greeting`.
// FIX ME: Make this program compile and print `case01 passed`.

fn main() {
    let greeting = String::from("hello");
    let louder = greeting;
    println!("louder = {louder}");
    println!("greeting = {greeting}");
    println!("case01 passed");
}
