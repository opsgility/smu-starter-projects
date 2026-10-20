// drill04 — reborrow.
//
// Compiles as shipped. `&mut *outer` creates a FRESH `&mut i32` to the same
// memory. The fresh borrow is what `bump` receives; when `bump` returns, the
// fresh borrow is gone and `outer` is usable again. Without the reborrow,
// `bump(outer)` would MOVE `outer` into the call (because `&mut T` is not
// Copy) and the second `bump` call would fail.

fn bump(n: &mut i32) {
    *n += 1;
}

fn main() {
    let mut n = 10;
    let outer: &mut i32 = &mut n;

    bump(&mut *outer);
    println!("after first bump:  {}", *outer);

    bump(outer);
    println!("after second bump: {n}");
    println!("drill04 passed");
}
