// EXPECTED ERROR: E0499 — cannot borrow `inv.items` as mutable more than once at a time
// HINT: `r1` and `r2` are both `&mut inv.items` and both live until their
//       last use (`touch(r1)`, `trace(r2)`). The compiler rejects `let r2 =
//       ...` while `r1` is still live. Fix: inline the borrow at each
//       function call so NLL ends each `&mut` borrow at its semicolon:
//           let n = touch(&mut inv.items);
//           let t = trace(&mut inv.items);
//           println!("touched {n}, trace said {t}");
// FIX ME: Make this compile.

struct Inv {
    items: Vec<i32>,
}

fn touch(items: &mut Vec<i32>) -> usize {
    items.push(1);
    items.len()
}

fn trace(items: &mut Vec<i32>) -> &'static str {
    items.pop();
    "logged"
}

fn main() {
    let mut inv = Inv { items: vec![10, 20] };

    let r1 = &mut inv.items;
    let r2 = &mut inv.items;

    let n = touch(r1);
    let t = trace(r2);

    println!("touched {n}, trace said {t}");
}
