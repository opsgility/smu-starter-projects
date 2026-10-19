// EXPECTED ERROR: E0382 use of moved value
// HINT: Inside the loop, `message` is moved into send() on iteration 1. On
//       iteration 2 the compiler says: "value moved here, in a previous iteration".
//       Fix: either `.clone()` before send() so iteration 2 gets a fresh copy,
//       OR change send() to take &String / &str so no move happens.

fn send(payload: String) {
    println!("sending: {payload}");
}

fn main() {
    let message = String::from("ownership checkpoint");

    // FIX ME: the compiler says `message` was moved on the previous iteration.
    //         Pick the fix: clone before send(), or change send() to take &str.
    for round in 1..=3 {
        println!("round {round}:");
        send(message);
    }
}
