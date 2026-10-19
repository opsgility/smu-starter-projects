// enum-match starter — see README.md
//
// Scenario: you are routing ticket Requests through a `handle` function.
// Course 639 Lesson 1 covered exhaustive match, if-let, let-else, guards,
// and @ bindings. The exercises walk you through:
//   Ex 2: add the missing variant
//   Ex 3: implement handle with exhaustive match + a guard
//   Ex 4: refactor one branch to use let-else
//   Ex 5 (optional): add an @ binding

enum Request {
    Health,
    // TODO (Exercise 2): add the missing variant
    //   Metrics { verbose: bool }
    Submit { id: u64, payload: String },
}

fn handle(_r: Request) {
    todo!("Exercise 3: implement handle with an exhaustive match")
}

fn main() {
    println!("enum-match starter — type `cargo run` after each exercise.");

    // Three sample requests exercise 3 will route through `handle`.
    let samples = [
        Request::Health,
        // Request::Metrics { verbose: true },  // uncomment after Exercise 2
        Request::Submit {
            id: 42,
            payload: String::from("hello"),
        },
        Request::Submit {
            id: 7,
            payload: String::new(),
        },
    ];

    for r in samples {
        handle(r);
    }
}
