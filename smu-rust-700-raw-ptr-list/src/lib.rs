//! SMU-RUST-700 Lesson 4 — build a singly-linked list using raw pointers + NonNull.
//!
//! Exercises:
//! 1. Smoke test.
//! 2. Implement `push` using Box::into_raw + NonNull::new_unchecked.
//! 3. Implement `pop` + the iterator.
//! 4. Add Drop + Send + Sync impls (with SAFETY justifications).

use std::ptr::NonNull;

pub struct Node<T> {
    pub value: T,
    pub next: Option<NonNull<Node<T>>>,
}

pub struct List<T> {
    pub head: Option<NonNull<Node<T>>>,
    pub len: usize,
    pub _marker: std::marker::PhantomData<T>,
}

impl<T> List<T> {
    pub fn new() -> Self {
        Self { head: None, len: 0, _marker: std::marker::PhantomData }
    }

    pub fn len(&self) -> usize {
        self.len
    }

    pub fn is_empty(&self) -> bool {
        self.len == 0
    }

    pub fn push(&mut self, _value: T) {
        todo!("Exercise 2: use Box::into_raw + NonNull::new_unchecked to prepend")
    }

    pub fn pop(&mut self) -> Option<T> {
        todo!("Exercise 3: use Box::from_raw to re-own the head node")
    }

    pub fn iter(&self) -> Iter<'_, T> {
        todo!("Exercise 3: build an Iter cursor from self.head")
    }
}

pub struct Iter<'a, T> {
    pub cursor: *const Node<T>,
    pub _marker: std::marker::PhantomData<&'a Node<T>>,
}

impl<'a, T> Iterator for Iter<'a, T> {
    type Item = &'a T;
    fn next(&mut self) -> Option<&'a T> {
        todo!("Exercise 3: dereference the cursor and advance")
    }
}

impl<T> Default for List<T> {
    fn default() -> Self { Self::new() }
}

impl<T> Drop for List<T> {
    fn drop(&mut self) {
        todo!("Exercise 4: loop while pop returns Some(_)")
    }
}

// Exercise 4: add these two impls with SAFETY justifications.
// unsafe impl<T: Send> Send for List<T> {}
// unsafe impl<T: Sync> Sync for List<T> {}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn push_increments_len() {
        let mut l: List<i32> = List::new();
        l.push(10);
        l.push(20);
        assert_eq!(l.len(), 2);
    }

    #[test]
    fn push_updates_head() {
        let mut l: List<i32> = List::new();
        l.push(10);
        assert!(l.head.is_some());
    }

    #[test]
    fn pop_from_empty_returns_none() {
        let mut l: List<i32> = List::new();
        assert_eq!(l.pop(), None);
    }

    #[test]
    fn pop_returns_in_lifo_order() {
        let mut l: List<i32> = List::new();
        l.push(1);
        l.push(2);
        l.push(3);
        assert_eq!(l.pop(), Some(3));
        assert_eq!(l.pop(), Some(2));
        assert_eq!(l.pop(), Some(1));
    }

    #[test]
    fn iter_yields_all_values() {
        let mut l: List<i32> = List::new();
        l.push(1);
        l.push(2);
        l.push(3);
        let collected: Vec<i32> = l.iter().copied().collect();
        assert_eq!(collected, vec![3, 2, 1]);
    }

    #[test]
    fn iter_empty_yields_nothing() {
        let l: List<i32> = List::new();
        let v: Vec<i32> = l.iter().copied().collect();
        assert!(v.is_empty());
    }
}
