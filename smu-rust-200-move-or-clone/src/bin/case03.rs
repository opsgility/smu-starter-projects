// EXPECTED ERROR: E0382 — borrow of moved value: `names`
// HINT: `for name in names` desugars to `for name in names.into_iter()`,
//       which moves each String OUT of the Vec and leaves `names` dropped.
//       The idiomatic fix is `for name in &names` — iterate by borrow.
// FIX ME: Make this program compile and print `case03 passed`.

fn main() {
    let names = vec![
        String::from("alice"),
        String::from("bob"),
        String::from("carol"),
    ];

    for name in names {
        println!("hello, {name}");
    }

    println!("names has {} entries", names.len());
    println!("case03 passed");
}
