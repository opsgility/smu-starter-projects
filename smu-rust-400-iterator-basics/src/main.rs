// Starter for Course 4 Lesson 1 paired HOL — Iterator basics.
//
// You will fill in the four `todo!()` functions across the exercises:
//   Ex 2: print_each       — uses .iter()
//   Ex 3: uppercase_each   — uses .iter_mut()
//   Ex 4: consume_longest  — uses .into_iter()
//   Ex 5: collect_lengths  — uses .iter().map(...).collect()
//
// The input is a small Vec<String> of city names. Each function demonstrates
// one of the three IntoIterator flavors or the main consumption patterns from
// Lesson 1.

fn print_each(cities: &Vec<String>) {
    todo!("Ex 2: iterate with cities.iter() and println! each city on its own line")
}

fn uppercase_each(cities: &mut Vec<String>) {
    todo!("Ex 3: iterate with cities.iter_mut() and uppercase each city in place")
}

fn consume_longest(cities: Vec<String>) -> String {
    todo!("Ex 4: use .into_iter().max_by_key(...) to pick the longest city by char count")
}

fn collect_lengths(cities: &[String]) -> Vec<usize> {
    todo!("Ex 5: use .iter().map(...).collect() to return a Vec of each city's char count")
}

fn main() {
    let cities = vec![
        String::from("Reykjavik"),
        String::from("Oslo"),
        String::from("Copenhagen"),
        String::from("Stockholm"),
        String::from("Helsinki"),
    ];

    println!("iterator-basics starter — fill in each exercise");
    println!("cities loaded: {} entries", cities.len());

    // Exercises will progressively uncomment these as they fill in the functions:
    //
    // print_each(&cities);
    //
    // let mut mutable_cities = cities.clone();
    // uppercase_each(&mut mutable_cities);
    // println!("uppercased: {:?}", mutable_cities);
    //
    // let lengths = collect_lengths(&cities);
    // println!("lengths: {:?}", lengths);
    //
    // let longest = consume_longest(cities);
    // println!("longest: {}", longest);
}
