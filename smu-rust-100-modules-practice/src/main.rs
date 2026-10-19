// smu-rust-100-modules-practice
//
// A tiny greeting generator for Course 1 Lesson 13's hands-on practice.
// Everything is in this single file today — your job across the exercises is
// to refactor it into a proper multi-file project with a library crate,
// nested modules, and one external dependency.
//
// Run with:  cargo run
//
// You should see:
//   Good morning, Camila!

fn greeting_for(lang: &str, period: &str) -> &'static str {
    match (lang, period) {
        ("en", "morning") => "Good morning",
        ("en", "afternoon") => "Good afternoon",
        ("en", "evening") => "Good evening",
        ("es", "morning") => "Buenos días",
        ("es", "afternoon") => "Buenas tardes",
        ("es", "evening") => "Buenas noches",
        ("fr", "morning") => "Bonjour",
        ("fr", "afternoon") => "Bon après-midi",
        ("fr", "evening") => "Bonsoir",
        ("de", "morning") => "Guten Morgen",
        ("de", "afternoon") => "Guten Tag",
        ("de", "evening") => "Guten Abend",
        _ => "Hello",
    }
}

fn format_name(name: &str) -> String {
    // Title-case: first char upper, rest lower.
    let mut chars = name.chars();
    match chars.next() {
        Some(first) => first.to_uppercase().collect::<String>() + chars.as_str().to_lowercase().as_str(),
        None => String::new(),
    }
}

fn build_greeting(name: &str, lang: &str, period: &str) -> String {
    let prefix = greeting_for(lang, period);
    let name = format_name(name);
    format!("{}, {}!", prefix, name)
}

fn main() {
    let message = build_greeting("camila", "en", "morning");
    println!("{}", message);
}
