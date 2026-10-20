// Exercise 2 defines the Repository trait with an associated Item type.
// Exercise 3 implements Repository for InMemoryRepo<T>.
// Exercise 4 adds a type-state AuthRepo<R, State> with PhantomData.
// Exercise 5 (optional) adds a const-generic SizedRepo<T, const N: usize>.

pub struct InMemoryRepo<T> {
    pub items: Vec<T>,
}

impl<T> InMemoryRepo<T> {
    pub fn new() -> Self {
        InMemoryRepo { items: Vec::new() }
    }
}

impl<T> Default for InMemoryRepo<T> {
    fn default() -> Self {
        Self::new()
    }
}

fn main() {
    println!("repository starter — fill in each exercise");
    let _r: InMemoryRepo<String> = InMemoryRepo::new();
    println!("new InMemoryRepo<String> constructed; count method lives in Ex 2's trait.");
}
