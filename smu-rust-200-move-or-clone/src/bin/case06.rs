// EXPECTED ERROR: E0382 — borrow of moved value: `title`
// HINT: `make_badge(title)` MOVES `title` into the function on each call.
//       The second call then sees `title` already gone. The idiomatic fix is
//       to clone on the first call so the second call still has an owned
//       String to move: `make_badge(title.clone());`.
// FIX ME: Make this program compile and print `case06 passed`.

fn make_badge(mut text: String) -> String {
    text.insert_str(0, "[BADGE] ");
    text
}

fn main() {
    let title = String::from("rustacean");

    let badge_a = make_badge(title);
    let badge_b = make_badge(title);

    println!("a: {badge_a}");
    println!("b: {badge_b}");
    println!("case06 passed");
}
