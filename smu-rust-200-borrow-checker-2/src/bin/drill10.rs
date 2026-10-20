// EXPECTED ERROR: E0382 — borrow of moved value: `jobs`
// HINT: `for job in jobs` desugars to `for job in jobs.into_iter()` which
//       MOVES the Vec. After the loop, `jobs` is consumed, so `jobs.len()`
//       fails. Fix: iterate by reference — `for job in &jobs`.
// FIX ME: Make this compile.

fn main() {
    let jobs = vec![
        String::from("compile"),
        String::from("test"),
        String::from("ship"),
    ];

    for job in jobs {
        println!("running: {job}");
    }

    println!("total jobs seen: {}", jobs.len());
}
