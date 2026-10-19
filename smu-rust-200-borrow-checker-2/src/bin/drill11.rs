// EXPECTED ERROR: E0499 cannot borrow `inv.items` as mutable more than once
// HINT: `touch(&mut inv.items)` is in a loop and the compiler sees TWO potential
//       mut borrows alive at once from the outer scope + the fn call. BUT: inside
//       touch(), the borrow ends when touch() returns. The compiler SHOULD be
//       fine with the loop pattern IF structured right.
//       The actual bug: the second call `trace(&mut inv.items)` is in the SAME
//       expression as the first — they overlap because of println!'s eager eval.
//       Fix: split into two statements so NLL ends each borrow at the semicolon.

struct Inventory {
    items: Vec<String>,
}

fn touch(items: &mut Vec<String>) -> usize {
    items.len()
}

fn trace(items: &mut Vec<String>) -> &str {
    items.push(String::from("auditor"));
    "logged"
}

fn main() {
    let mut inv = Inventory {
        items: vec![String::from("boots"), String::from("hat")],
    };

    // FIX ME: both touch() and trace() each take &mut inv.items. In the SAME
    //         println! both are evaluated before the format runs — compiler sees
    //         two overlapping mut borrows. Split into two statements:
    //           let n = touch(&mut inv.items);
    //           let t = trace(&mut inv.items);
    //           println!("touched {n}, trace said {t}");
    println!("touched {}, trace said {}", touch(&mut inv.items), trace(&mut inv.items));
}
