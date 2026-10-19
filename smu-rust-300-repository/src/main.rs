// Course 639 (SMU-RUST-300) Lesson 6 HOL — Repository trait + associated types + PhantomData.
// Hollis Brennan: "Build the type system that makes your API hard to misuse."
//
// Exercise 1 is a smoke test. Exercises 2-5 fill in the stubs below in order.

// EX 2: define `trait Repository` with associated `Item` type.
// trait Repository {
//     type Item;
//     fn add(&mut self, item: Self::Item);
//     fn get(&self, idx: usize) -> Option<&Self::Item>;
//     fn count(&self) -> usize { /* default using get + loop or len via a required method */ }
// }

// EX 3: implement Repository for a generic InMemoryRepo<T>.
pub struct InMemoryRepo<T> {
    items: Vec<T>,
}

impl<T> InMemoryRepo<T> {
    pub fn new() -> Self {
        Self { items: Vec::new() }
    }
}

impl<T> Default for InMemoryRepo<T> {
    fn default() -> Self {
        Self::new()
    }
}

// EX 4: tag structs + AuthRepo<R, State> with PhantomData.
// use std::marker::PhantomData;
// pub struct Anonymous;
// pub struct Authenticated;
// pub struct AuthRepo<R, State> { repo: R, _phantom: PhantomData<State> }

// EX 5 (optional): const-generic SizedRepo.
// pub struct SizedRepo<T, const N: usize> { items: [Option<T>; N] }

fn main() {
    println!("repository starter — fill in each exercise");
    let _repo: InMemoryRepo<String> = InMemoryRepo::new();
    println!("new InMemoryRepo<String> constructed; count method lives in Ex 2's trait.");
}
