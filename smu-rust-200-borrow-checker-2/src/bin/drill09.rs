// EXPECTED ERROR: E0507 — cannot move out of `profile.name` which is behind a `&` reference
// HINT: `describe` takes `&Profile`. `let name = profile.name;` tries to
//       MOVE `profile.name` out of a shared reference — forbidden. Fix:
//       clone the name (`profile.name.clone()`).
// FIX ME: Make this compile.

struct Profile {
    name: String,
    age: u32,
}

fn describe(profile: &Profile) {
    let name = profile.name;
    println!("{name} is {} years old", profile.age);
}

fn main() {
    let p = Profile {
        name: String::from("Rafiq"),
        age: 29,
    };
    describe(&p);
    println!("original still readable: {} / {}", p.name, p.age);
}
