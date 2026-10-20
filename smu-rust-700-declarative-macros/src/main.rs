//! SMU-RUST-700 Lesson 12 — write a vec!-like macro + a tiny HTML DSL.
//!
//! Exercises:
//! 1. Smoke test — cargo build succeeds.
//! 2. Define `my_vec!` for a comma list.
//! 3. Extend `my_vec!` with the [val; count] form.
//! 4. Add an `html!` DSL macro.

// Exercise 2+3: define my_vec! here.
// macro_rules! my_vec { ... }

// Exercise 4: define html! here.
// macro_rules! html { ... }

fn main() {
    // Exercise 2+3: uncomment these once my_vec! is defined.
    // let v1: Vec<i32> = my_vec![1, 2, 3];
    // assert_eq!(v1, vec![1, 2, 3]);
    // let v2: Vec<u8> = my_vec![0u8; 5];
    // assert_eq!(v2, vec![0u8; 5]);
    //
    // Exercise 4: uncomment these once html! is defined.
    // let simple = html!(div { "hello" });
    // assert_eq!(simple, "<div>hello</div>");
    // let nested = html!(div { span { "world" } });
    // assert_eq!(nested, "<div><span>world</span></div>");

    println!("smu-rust-700-declarative-macros starter is ready");
}
