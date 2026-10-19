// Course 3 Lesson 7 HOL — Work around the orphan rule.
//
// This starter is INTENTIONALLY broken. `cargo build` fails with E0117
// out of the box because the impl below tries to add a std-library trait
// to a std-library type. Exercise 1 asks you to read that error.
// Exercise 2 asks you to comment the broken impl out so the project
// compiles. Exercises 3 and 4 build out the two canonical workarounds.

// --- Ex 1 / 2: Observe E0117, then comment it out ---
//
// Both `ToString` and `Vec<i32>` live in `std` (foreign crates). The orphan
// rule says a crate may implement a trait for a type only when at least
// one of them (trait OR type) is defined in this crate. Here neither is,
// so this impl is rejected with E0117.
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
//         // TODO: write out the vec contents as "[1, 2, 3]"
//         todo!()
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
//         // TODO: iterate, sum, format
//         todo!()
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
