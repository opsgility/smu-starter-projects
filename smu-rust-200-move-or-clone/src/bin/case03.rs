// case03: Loop that moves each String out of the Vec.
//
// EXPECTED ERROR: E0507 — cannot move out of index of `Vec<String>`.
// (With a plain `for name in names`, the compiler iterates by value and moves
//  each element — but you then try to use `names` after the loop, which fails.)
//
// FIX ME: iterate by reference with `for name in &names` so each `name` is a
//         borrowed `&String`, and `names` stays owned by main().
//
// Do NOT clone the Vec. Do NOT change `names`'s type. The idiomatic fix for
// "iterate without consuming" is `&collection`.

fn main() {
    let names = vec![
        String::from("Hollis"),
        String::from("Kenji"),
        String::from("Imani"),
    ];

    for name in names {
        println!("hello, {}", name);
    }

    println!("roster size: {}", names.len());

    println!("case03 passed");
}
