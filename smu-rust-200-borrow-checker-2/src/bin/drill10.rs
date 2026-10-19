// EXPECTED ERROR: E0382 use of moved value: `jobs`
// HINT: `for job in jobs` desugars to `for job in jobs.into_iter()` which MOVES
//       the Vec. After the loop, `jobs` is gone. The student usually thinks they
//       were iterating by reference. Fix: `for job in &jobs` to iterate by
//       shared reference (then `job: &String` inside), or `.iter()` explicitly.

fn main() {
    let jobs = vec![
        String::from("compile"),
        String::from("test"),
        String::from("ship"),
    ];

    // FIX ME: `for job in jobs` moves the Vec. Change to `for job in &jobs`.
    for job in jobs {
        println!("running: {job}");
    }

    println!("total jobs seen: {}", jobs.len());
}
