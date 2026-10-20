fn sum(v: &Vec<u32>) -> u32 {
    let mut total = 0;
    for n in v {
        total += n;
    }
    total
}

fn count_vowels(s: &String) -> usize {
    let mut count = 0;
    for c in s.chars() {
        if matches!(c, 'a' | 'e' | 'i' | 'o' | 'u' | 'A' | 'E' | 'I' | 'O' | 'U') {
            count += 1;
        }
    }
    count
}

fn first_three_chars(s: &str) -> &str {
    &s[0..3]
}

fn tokens(_s: &str) -> Vec<&str> {
    Vec::new()
}

fn main() {
    println!("slice-practice starter — work through each exercise.");

    let numbers = vec![1u32, 2, 3, 4, 5];
    println!("sum = {}", sum(&numbers));

    let message = String::from("hello world");
    println!("vowels in \"hello world\" = {}", count_vowels(&message));

    let greeting = String::from("hello");
    println!("first three of \"hello\" = {}", first_three_chars(&greeting));
    // TRY (Exercise 3): uncomment and watch the panic.
    // println!("first three of \"🦀🦀🦀\" = {}", first_three_chars("🦀🦀🦀"));

    let line = String::from("the quick brown fox");
    println!("tokens of \"the quick brown fox\" = {:?}", tokens(&line));
}
