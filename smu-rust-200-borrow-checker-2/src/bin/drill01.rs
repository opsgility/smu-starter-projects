// EXPECTED ERROR: E0382 — use of moved value: `message` (loop iteration moves)
// HINT: `send(payload: String)` consumes the String on every call. The loop
//       moves `message` out on the first iteration; the second iteration
//       then uses a moved value. The idiomatic fix changes `send`'s param
//       to `&str` so each call borrows instead of taking ownership.
// FIX ME: Make this compile.

fn send(payload: String) {
    println!("sending: {payload}");
}

fn main() {
    let message = String::from("ownership checkpoint");

    for round in 1..=3 {
        println!("round {round}:");
        send(message);
    }
}
