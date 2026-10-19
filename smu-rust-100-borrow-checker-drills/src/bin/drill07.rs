// FIX ME: Make this program compile and print `HELLO!` twice then `drill 07 passed`.
// EXPECTED ERROR: E0382 — use of moved value: `greeting`
// Hint: `shout` takes `String` BY VALUE — the first call moves `greeting`
//       into the function and consumes it. The second call has nothing left.
//       Simplest fix: pass a clone on the first call so the owned String
//       stays available for the second.

fn shout(s: String) {
    println!("{}!", s.to_uppercase());
}

fn main() {
    let greeting = String::from("hello");
    shout(greeting);
    shout(greeting);
    println!("drill 07 passed");
}
