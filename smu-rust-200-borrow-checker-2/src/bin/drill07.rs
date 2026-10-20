// EXPECTED ERROR: E0507 — cannot move out of index of `Vec<String>`
// HINT: `v[0]` on a Vec<String> tries to MOVE the String out, but indexing
//       cannot move out of a container. Three fixes exist (`v.remove(0)`,
//       `v.swap_remove(0)`, `v[0].clone()`). Simplest for this drill is
//       `v[0].clone()` — leaves `v` untouched.
// FIX ME: Make this compile.

fn main() {
    let v = vec![
        String::from("alpha"),
        String::from("beta"),
        String::from("gamma"),
    ];

    let first: String = v[0];

    println!("first was: {first}");
    println!("rest is: {:?}", v);
}
