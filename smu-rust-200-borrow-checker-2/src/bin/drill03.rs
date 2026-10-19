// EXPECTED ERROR: E0502 cannot borrow `inv.items` as mutable because it is also
//                 borrowed as immutable
// HINT: `first_item` holds `&inv.items[0]`. Then items.push() needs &mut inv.items.
//       Both borrows go through the same field — the compiler can't split them
//       the way it can for distinct struct fields.
//       Fix: use/print first_item BEFORE push (NLL ends the shared borrow),
//       OR copy out the data you need (`let first = inv.items[0].clone()`) and
//       drop the reference before push.

struct Inventory {
    items: Vec<String>,
}

fn main() {
    let mut inv = Inventory {
        items: vec![String::from("belt"), String::from("hat")],
    };

    let first_item = &inv.items[0];

    // FIX ME: push needs &mut inv.items; first_item holds &inv.items[0].
    //         Reorder — use first_item BEFORE push, then NLL releases it.
    inv.items.push(String::from("shoes"));

    println!("first item was: {first_item}");
}
