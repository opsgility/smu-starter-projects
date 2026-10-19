// drill02 — split borrows across struct fields
//
// EXPECTED: this file compiles and runs cleanly. The point: the borrow checker
// understands that `&mut s.a` and `&s.b` touch different memory, so holding
// both at the same time is safe.
//
// Pattern: you can hold a mutable borrow of one field and a shared borrow of
// another field at the same time, even though the WHOLE struct would conflict.

struct Settings {
    a: i32,
    b: String,
}

fn main() {
    let mut s = Settings {
        a: 10,
        b: String::from("initial"),
    };

    // Mutable borrow of ONE field. The struct as a whole would be busy, but
    // the borrow checker sees that only `a` is mutably borrowed.
    let a_ref: &mut i32 = &mut s.a;

    // Shared borrow of ANOTHER field is allowed at the same time — the two
    // borrows don't overlap in memory.
    let b_ref: &String = &s.b;

    println!("field b (shared borrow) = {b_ref}");
    *a_ref += 5;
    println!("field a (after +=5)     = {a_ref}");

    // Both borrows have ended here. Fresh observation:
    println!("final s = (a={}, b={})", s.a, s.b);

    println!("drill02 passed");
}
