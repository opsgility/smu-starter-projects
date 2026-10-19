// drill04 — reborrow: pass `&mut *outer` into a function, keep `outer`
// accessible after the function returns.
//
// EXPECTED: this file compiles and runs cleanly. The reborrow lets you give
// an inner function a FRESH `&mut i32` to work with, without moving the
// outer `&mut i32` into the call — so you keep using the outer binding
// after the call ends.

fn bump(x: &mut i32) {
    *x += 1;
}

fn main() {
    let mut n = 10;
    let outer: &mut i32 = &mut n;

    // Reborrow: `&mut *outer` creates a fresh &mut i32 from the same
    // underlying place. The reborrow lasts only through the function call;
    // when `bump` returns, `outer` is usable again.
    bump(&mut *outer);
    println!("after first bump:  {}", outer);

    // Same pattern a second time.
    bump(&mut *outer);
    println!("after second bump: {}", outer);

    // The compiler can also reborrow implicitly if you write `bump(outer)`
    // directly — try it: swap the two bump calls above for `bump(outer);`
    // and watch it still compile. The reborrow is automatic for &mut T
    // argument positions.

    println!("drill04 passed");
}
