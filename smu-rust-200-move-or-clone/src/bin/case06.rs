// case06: Try to use a String in two places as if it were Copy.
//
// EXPECTED ERROR: E0382 — borrow of moved value: `title`.
// HINT: `title` is a String. The first `make_badge(title)` call moves it into
//       the function. The second call then uses the moved value.
//
// FIX ME: You need two separate owners. `.clone()` the first argument so each
//         call gets its own copy. `.to_string()` on a `&str` would also work
//         if you converted from a literal, but here the source is already a
//         String, so `.clone()` is the direct fix.
//
// Do NOT change `make_badge`'s signature — Strings are legitimately moved
// into some functions (think "appends to a database"); the lesson is that
// the CALLER sometimes chooses to clone to keep ownership.

fn make_badge(label: String) -> String {
    format!("[ {} ]", label)
}

fn main() {
    let title = String::from("gold");

    let badge_a = make_badge(title);
    let badge_b = make_badge(title);

    println!("badge_a = {}", badge_a);
    println!("badge_b = {}", badge_b);

    println!("case06 passed");
}
