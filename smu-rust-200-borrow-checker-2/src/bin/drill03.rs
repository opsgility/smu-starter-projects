// EXPECTED ERROR: E0502 — cannot borrow `inv.items` as mutable because it
//                          is also borrowed as immutable
// HINT: `first_item` holds `&inv.items[0]`. The `inv.items.push(...)` call
//       needs `&mut inv.items`. Both borrows go through the same field.
//       Fix via NLL: print `first_item` BEFORE `push`, so the shared borrow
//       is released at its last use before the mutable borrow begins.
// FIX ME: Make this compile.

struct Inventory {
    items: Vec<String>,
}

fn main() {
    let mut inv = Inventory {
        items: vec![String::from("belt"), String::from("hat")],
    };

    let first_item = &inv.items[0];
    inv.items.push(String::from("shoes"));
    println!("first item was: {first_item}");
    println!("items now: {:?}", inv.items);
}
