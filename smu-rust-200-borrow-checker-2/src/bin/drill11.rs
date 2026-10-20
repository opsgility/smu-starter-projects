// EXPECTED ERROR: E0499 — cannot borrow `inv.items` as mutable more than once at a time
// HINT: `println!("touched {}, trace said {}", touch(&mut inv.items),
//       trace(&mut inv.items));` evaluates both arguments before formatting.
//       Two overlapping `&mut inv.items` borrows exist at the same time.
//       Fix: split the two calls into separate `let` statements. NLL ends
//       each mutable borrow at its semicolon.
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
    println!(
        "touched {}, trace said {}",
        touch(&mut inv.items),
        trace(&mut inv.items)
    );
}
