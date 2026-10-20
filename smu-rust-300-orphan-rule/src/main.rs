// --- Ex 1 / 2: Observe E0117, then comment it out ---
//
// This starter attempts to implement a std trait (`ToString`) for a std
// type (`Vec<i32>`). The compiler refuses — the orphan rule says at least
// one side of an impl must be local to the current crate. Here, neither is.

impl ToString for Vec<i32> {
    fn to_string(&self) -> String {
        format!("int vec with {} entries", self.len())
    }
}

// --- Ex 3: Newtype stub (uncomment the block in Exercise 3) ---
//
// struct IntList(Vec<i32>);
//
// impl std::fmt::Display for IntList {
//     fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
//         todo!("Exercise 3: write out the vec contents as \"[1, 2, 3]\"")
//     }
// }

// --- Ex 4: Extension trait + blanket impl (uncomment the block in Exercise 4) ---
//
// trait Summable {
//     fn sum_as_str(&self) -> String;
// }
//
// impl<T> Summable for T
// where
//     T: IntoIterator<Item = i32> + Clone,
// {
//     fn sum_as_str(&self) -> String {
//         todo!("Exercise 4: sum the iterator and format as \"sum = N\"")
//     }
// }

// --- Ex 5 (optional): Deref so IntList inherits Vec's methods for free ---
//
// use std::ops::Deref;
//
// impl Deref for IntList {
//     type Target = Vec<i32>;
//     fn deref(&self) -> &Self::Target {
//         &self.0
//     }
// }

fn main() {
    println!("orphan-rule starter — see README.md");
}
