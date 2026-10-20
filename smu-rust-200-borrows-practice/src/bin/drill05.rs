// drill05 — iterator invalidation. BROKEN AS SHIPPED.
//
// EXPECTED ERROR: E0502 — cannot borrow `v` as mutable because it is also
// borrowed as immutable. The `&v` in the for header holds a shared borrow
// for the entire loop body; the `v.push(...)` inside wants a mutable borrow.
// FIX in Exercise 4: collect the values you want to push during iteration,
// then extend after the shared borrow is released:
//   let to_push: Vec<i32> = v.iter().map(|&x| x * 10).collect();
//   v.extend(to_push);

fn main() {
    let mut v = vec![1, 2, 3];

    for &x in &v {
        v.push(x * 10);
    }

    println!("extended: {v:?}");
    println!("drill05 passed");
}
