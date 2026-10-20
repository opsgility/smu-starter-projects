// Exercise 2 fills print_each with .iter().
// Exercise 3 fills uppercase_each with .iter_mut().
// Exercise 4 fills consume_longest with .into_iter() + .max_by_key.
// Exercise 5 fills collect_lengths with .iter().map().collect().

#[allow(dead_code)]
fn print_each(_cities: &Vec<String>) {
    todo!("Exercise 2: iterate with .iter() and println! each entry")
}

#[allow(dead_code)]
fn uppercase_each(_cities: &mut Vec<String>) {
    todo!("Exercise 3: iterate with .iter_mut() and uppercase each entry in place")
}

#[allow(dead_code)]
fn consume_longest(_cities: Vec<String>) -> String {
    todo!("Exercise 4: .into_iter().max_by_key(|c| c.chars().count()).unwrap()")
}

#[allow(dead_code)]
fn collect_lengths(_cities: &[String]) -> Vec<usize> {
    todo!("Exercise 5: cities.iter().map(|c| c.chars().count()).collect()")
}

fn main() {
    println!("iterator-basics starter — fill in each exercise");

    let cities: Vec<String> = vec![
        "Reykjavik".to_string(),
        "Oslo".to_string(),
        "Copenhagen".to_string(),
        "Stockholm".to_string(),
        "Helsinki".to_string(),
    ];
    println!("cities loaded: {} entries", cities.len());

    // Exercise 2 — uncomment:
    // print_each(&cities);

    // Exercise 5 — uncomment (must come BEFORE Exercise 4's consume_longest call):
    // let lengths = collect_lengths(&cities);
    // println!("lengths: {:?}", lengths);

    // Exercise 3 — uncomment:
    // let mut mutable_cities = cities.clone();
    // uppercase_each(&mut mutable_cities);
    // println!("uppercased: {:?}", mutable_cities);

    // Exercise 4 — uncomment (last, because .into_iter() moves `cities`):
    // let longest = consume_longest(cities);
    // println!("longest: {}", longest);
}
