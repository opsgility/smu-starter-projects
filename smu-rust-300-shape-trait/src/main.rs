// Starter for SMU-RUST-300 Lesson 4 paired HOL — Design a Shape trait with
// default methods. The three structs are already defined; the trait is left
// as a placeholder for the student to flesh out across the exercises.

#[derive(Debug)]
struct Circle {
    radius: f64,
}

#[derive(Debug)]
struct Rectangle {
    w: f64,
    h: f64,
}

#[derive(Debug)]
struct Triangle {
    a: f64,
    b: f64,
    c: f64,
}

// EX 2: Define `trait Shape` here with required methods `area` + `perimeter`
// and a default `describe` method that uses them.
//
// trait Shape {
//     // TODO
// }

// EX 3: Implement `Shape` for each of Circle, Rectangle, Triangle.
// Override `describe` for Rectangle to add a shape-specific label.
//
// impl Shape for Circle {
//     // TODO
// }

// EX 4: Define `fn report<S: Shape + std::fmt::Debug>(s: &S)`.
//
// fn report<S: Shape + std::fmt::Debug>(_s: &S) {
//     todo!("Ex 4")
// }

// EX 5 (optional): Define `fn total_area<S: Shape>(shapes: &[S]) -> f64`.
//
// fn total_area<S: Shape>(_shapes: &[S]) -> f64 {
//     todo!("Ex 5")
// }

fn main() {
    println!("shape-trait starter — fill in each exercise");
    let c = Circle { radius: 2.0 };
    let r = Rectangle { w: 3.0, h: 4.0 };
    let t = Triangle { a: 3.0, b: 4.0, c: 5.0 };

    // The following call will panic at `todo!()` until Ex 2 + Ex 3 land.
    // Uncomment it as you work through the exercises.
    // println!("{}", c.describe());

    // Keep the compiler from complaining about unused shapes while you build.
    let _ = (&c, &r, &t);
}
