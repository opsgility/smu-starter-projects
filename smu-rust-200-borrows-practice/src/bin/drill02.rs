// drill02 — split borrows across struct fields.
//
// Compiles as shipped. The borrow checker tracks borrows per memory
// location, not per name — &mut s.a and &s.b touch different fields of the
// same struct, so they can coexist.

struct S {
    a: i32,
    b: String,
}

fn main() {
    let mut s = S {
        a: 10,
        b: String::from("initial"),
    };

    let a_ref: &mut i32 = &mut s.a;
    let b_ref: &String = &s.b;

    println!("field b (shared borrow) = {b_ref}");
    *a_ref += 5;
    println!("field a (after +=5)     = {}", s.a);
    println!("final s = (a={}, b={})", s.a, s.b);
    println!("drill02 passed");
}
