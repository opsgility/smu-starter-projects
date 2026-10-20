fn sum_evens(nums: &[i32]) -> i32 {
    let mut total = 0;
    for n in nums {
        if n % 2 == 0 {
            total += n;
        }
    }
    total
}

fn double_strings(words: &[String]) -> Vec<String> {
    let mut out = Vec::new();
    for w in words {
        out.push(format!("{w}-{w}"));
    }
    out
}

fn zip_names_ages(names: &[String], ages: &[u32]) -> Vec<String> {
    let mut out = Vec::new();
    for i in 0..names.len().min(ages.len()) {
        out.push(format!("{} is {}", names[i], ages[i]));
    }
    out
}

fn flatten_sublists(groups: Vec<Vec<i32>>) -> Vec<i32> {
    let mut out = Vec::new();
    for g in groups {
        for n in g {
            out.push(n);
        }
    }
    out
}

fn count_matching(nums: &[i32], pred: impl Fn(&i32) -> bool) -> usize {
    let mut count = 0;
    for n in nums {
        if pred(n) {
            count += 1;
        }
    }
    count
}

fn main() {
    println!("adapter-practice starter — see README.md\n");

    let nums = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    println!("sum_evens: {}", sum_evens(&nums));

    let words: Vec<String> = ["alpha", "beta", "gamma"].iter().map(|s| s.to_string()).collect();
    println!("double_strings: {:?}", double_strings(&words));

    let names: Vec<String> = ["Imani", "Pavel", "Kenji"].iter().map(|s| s.to_string()).collect();
    let ages: Vec<u32> = vec![42, 37, 29];
    println!("zip_names_ages: {:?}", zip_names_ages(&names, &ages));

    let groups = vec![vec![1, 2, 3], vec![4, 5], vec![6]];
    println!("flatten_sublists: {:?}", flatten_sublists(groups));

    println!("count_matching(> 5): {}", count_matching(&nums, |n| *n > 5));
}
