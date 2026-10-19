// EXPECTED ERROR: E0507 cannot move out of index of Vec<String>
// HINT: `v[0]` on a Vec<String> tries to MOVE the String out, but indexing can
//       only COPY (and String isn't Copy). Three fixes, pick one:
//         (a) `v.remove(0)` — removes + returns the first element, shifts rest
//         (b) `v.swap_remove(0)` — removes + returns, swapping last into [0] (fast, order lost)
//         (c) `v[0].clone()` — leave the original in place, take a copy

fn main() {
    let v = vec![
        String::from("alpha"),
        String::from("beta"),
        String::from("gamma"),
    ];

    // FIX ME: this moves v[0] out of the Vec. Pick remove(0), swap_remove(0),
    //         or v[0].clone(). Each has a different semantic.
    let first: String = v[0];

    println!("first was: {first}");
    println!("rest is: {v:?}");
}
