# custom-iterator starter

Two struct declarations, no `Iterator` impls yet.

- Exercise 2 adds `impl Iterator for Fibonacci` (type Item = u64).
- Exercise 3 adds `impl<'a> Iterator for Words<'a>` yielding `&'a str`.
- Exercise 4 adds `size_hint` on Fibonacci + overridden `count` on Words.
- Exercise 5 (optional) rewrites Fibonacci using `std::iter::from_fn`.
