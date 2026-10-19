// EXPECTED ERROR: E0507 cannot move out of a shared reference
// HINT: `profile.name` is a String. Accessing it through `&profile` means moves
//       out of fields are forbidden — a &T cannot destructure its fields by move.
//       Three fixes:
//         (a) `profile.name.clone()` — leave the original String in place
//         (b) `&profile.name` — borrow instead of move (change the let binding
//              to accept &String or &str)
//         (c) take `profile` by value instead of by reference — change the fn
//              signature. Rarely the right fix; (a) or (b) is better.

struct Profile {
    name: String,
    age: u32,
}

fn describe(profile: &Profile) -> String {
    // FIX ME: moving profile.name out of a shared ref is forbidden. Use .clone()
    //         on name, or borrow it (&profile.name) and format with the borrow.
    let name = profile.name;
    format!("{name} is {} years old", profile.age)
}

fn main() {
    let p = Profile { name: String::from("Rafiq"), age: 29 };
    let desc = describe(&p);
    println!("{desc}");
    println!("original still readable: {} / {}", p.name, p.age);
}
