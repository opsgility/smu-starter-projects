// drill05 — iterator invalidation, and the collect-then-push fix
//
// EXPECTED: as shipped, this file DOES NOT COMPILE. It triggers E0502 because
// the `for &x in &v` loop holds a shared borrow of `v` while the loop body
// tries to mutate `v` with `v.push(x * 10)`.
//
// Your job in exercise 4 is to fix it. The two canonical fixes:
//
//   1. Collect the values to push into a Vec first, then push after the loop:
//
//        let to_push: Vec<i32> = v.iter().map(|&x| x * 10).collect();
//        v.extend(to_push);
//
//   2. Use indexing instead of iteration (less idiomatic but works):
//
//        let len = v.len();
//        for i in 0..len {
//            let doubled = v[i] * 10;
//            v.push(doubled);
//        }
//
// Pick one, make the file compile, and run `cargo run --bin drill05`.
// Expected output when fixed: `drill05 passed` plus the extended vector.

fn main() {
    let mut v: Vec<i32> = vec![1, 2, 3];

    // ↓↓↓ FIX ME: shared borrow of v in `&v` conflicts with mutable push below.
    for &x in &v {
        v.push(x * 10);
    }
    // ↑↑↑ FIX ME

    println!("extended: {:?}", v);
    println!("drill05 passed");
}
