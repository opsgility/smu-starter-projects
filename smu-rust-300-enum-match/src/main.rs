// Exercise 2 adds the missing Metrics variant.
// Exercise 3 replaces the todo!() body of handle with an exhaustive match.
// Exercise 4 refactors Submit to let-else.
// Exercise 5 adds an @ binding on low IDs.

enum Request {
    Health,
    // TODO (Exercise 2): add the missing variant
    Submit { id: u32, payload: String },
}

fn handle(_r: Request) {
    todo!("Exercise 3: implement handle with an exhaustive match")
}

fn main() {
    println!("enum-match starter — type `cargo run` after each exercise.");

    let samples = vec![
        Request::Health,
        // Request::Metrics { verbose: true },
        Request::Submit { id: 42, payload: String::from("hello") },
        Request::Submit { id: 7, payload: String::new() },
    ];

    for r in samples {
        handle(r);
    }
}
