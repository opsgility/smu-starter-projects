// slice-practice starter — fill in each exercise to refactor these fns.
//
// Four functions ship below. Three take restrictive owned-container
// references and need to be refactored to take slices. One works for
// ASCII but panics on multi-byte chars. One is a stub you'll implement.
//
// Run with `cargo run` to see today's output.

fn main() {
    println!("slice-practice starter — work through each exercise.");

    // Exercise 2: sum takes `&Vec<u32>` — refactor to `&[u32]`.
    let numbers = vec![1, 2, 3, 4, 5];
    println!("sum = {}", sum(&numbers));

    // Exercise 2: count_vowels takes `&String` — refactor to `&str`.
    let message = String::from("hello world");
    println!("vowels in \"{}\" = {}", message, count_vowels(&message));

    // Exercise 3: first_three_chars works for ASCII, panics on multi-byte.
    println!("first three of \"hello\" = {}", first_three_chars("hello"));
    // TRY (Exercise 3): uncomment and watch the panic.
    // println!("first three of \"🦀🦀🦀\" = {}", first_three_chars("🦀🦀🦀"));

    // Exercise 4: tokens stub — returns an empty Vec today. Implement to
    // return slices into the input (no per-token allocation).
    let line = "the quick brown fox";
    println!("tokens of \"{}\" = {:?}", line, tokens(line));
}

// EX 2: refactor the parameter to `&[u32]`.
fn sum(v: &Vec<u32>) -> u32 {
    let mut total = 0;
    for &n in v {
        total += n;
    }
    total
}

// EX 2: refactor the parameter to `&str`.
fn count_vowels(s: &String) -> usize {
    s.chars()
        .filter(|c| matches!(c, 'a' | 'e' | 'i' | 'o' | 'u'))
        .count()
}

// EX 3: works for ASCII, panics on multi-byte boundaries.
// Fix by taking the first three chars (not bytes) and returning an owned String.
fn first_three_chars(s: &str) -> &str {
    &s[0..3]
}

// EX 4: implement — return slices into `s`, no allocation per token.
// Hint: `str::split_whitespace` yields `&str` slices borrowed from `s`.
fn tokens(_s: &str) -> Vec<&str> {
    Vec::new()
}
