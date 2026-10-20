//! SMU-RUST-700 Lesson 2 — safe wrapper around raw-pointer primitives.
//!
//! You'll complete the `view` function in Exercise 2, then study and remove
//! `bad_view` in Exercise 3.

/// Build a slice view over a borrowed array.
///
/// # Safety invariants to document in Exercise 2:
/// - `ptr` is non-null
/// - alignment is correct for T
/// - lifetime of the result is bounded by the input borrow
/// - no concurrent mutation
pub fn view<T>(_data: &[T]) -> &[T] {
    todo!("Exercise 2: wrap std::slice::from_raw_parts in a safe public API")
}

/// EXERCISE 3: this function LOOKS correct but is unsound.
/// Find the aliasing bug and delete this function.
pub fn bad_view<T>(data: &[T]) -> &mut [T] {
    let ptr = data.as_ptr() as *mut T;
    let len = data.len();
    unsafe { std::slice::from_raw_parts_mut(ptr, len) }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn view_slice_returns_input() {
        let data = vec![1, 2, 3];
        let v = view(&data);
        assert_eq!(v, &[1, 2, 3]);
    }

    #[test]
    fn view_slice_empty() {
        let data: Vec<i32> = vec![];
        let v = view(&data);
        assert!(v.is_empty());
    }

    #[test]
    #[should_panic]
    fn bad_view_aliasing_bug() {
        let data = vec![1, 2, 3];
        let _first_borrow = &data[0];
        let _bad = bad_view(&data);
        panic!("bad_view's aliasing bug demonstrates UB; see src/bug_report.md");
    }
}
