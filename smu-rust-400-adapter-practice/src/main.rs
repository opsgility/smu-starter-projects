// adapter-practice starter — see README.md
//
// Each of the five functions below ships with a WORKING imperative body
// (a plain `for` loop). Across the exercises you refactor each one into
// an equivalent iterator-adapter chain. The behavior must stay the same;
// only the shape of the implementation changes.
//
// Keep a copy of each original body in a `//` comment above the function
// so you can diff old vs new as you go.

fn sum_evens(nums: &[i32]) -> i32 {
    // TODO: refactor to adapter chain
    let mut total = 0;
    for n in nums {
        if n % 2 == 0 {
            total += n;
        }
    }
    total
}

fn double_strings(words: &[String]) -> Vec<String> {
    // TODO: refactor to adapter chain
    let mut out = Vec::new();
    for w in words {
        out.push(format!("{w}-{w}"));
    }
    out
}

fn zip_names_ages(names: &[String], ages: &[u32]) -> Vec<String> {
    // TODO: refactor to adapter chain
    let mut out = Vec::new();
    for i in 0..names.len() {
        out.push(format!("{} is {}", names[i], ages[i]));
    }
    out
}

fn flatten_sublists(groups: Vec<Vec<i32>>) -> Vec<i32> {
    // TODO: refactor to adapter chain
    let mut out = Vec::new();
    for g in groups {
        for n in g {
            out.push(n);
        }
    }
    out
}

fn count_matching(nums: &[i32], pred: impl Fn(&i32) -> bool) -> usize {
    // TODO: refactor to adapter chain
    let mut count = 0;
    for n in nums {
        if pred(n) {
            count += 1;
        }
    }
    count
}

fn main() {
    let nums = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    let words = vec!["alpha".to_string(), "beta".to_string(), "gamma".to_string()];
    let names = vec!["Imani".to_string(), "Pavel".to_string(), "Kenji".to_string()];
    let ages = vec![42, 37, 29];
    let groups = vec![vec![1, 2], vec![3, 4, 5], vec![6]];

    println!("adapter-practice starter — see README.md");
    println!();
    println!("sum_evens: {}", sum_evens(&nums));
    println!("double_strings: {:?}", double_strings(&words));
    println!("zip_names_ages: {:?}", zip_names_ages(&names, &ages));
    println!("flatten_sublists: {:?}", flatten_sublists(groups.clone()));
    println!("count_matching(> 5): {}", count_matching(&nums, |n| *n > 5));
}
