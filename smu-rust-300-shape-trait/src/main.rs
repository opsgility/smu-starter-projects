// Exercise 2 defines trait Shape with two required methods (area, perimeter)
// and one default method (describe).
// Exercise 3 adds impl Shape for each of Circle / Rectangle / Triangle.
// Exercise 4 adds a generic report<S: Shape + Debug> fn.
// Exercise 5 (optional) adds total_area<S: Shape>(&[S]).

#[derive(Debug)]
pub struct Circle {
    pub radius: f64,
}

#[derive(Debug)]
pub struct Rectangle {
    pub w: f64,
    pub h: f64,
}

#[derive(Debug)]
pub struct Triangle {
    pub a: f64,
    pub b: f64,
    pub c: f64,
}

// EX 2: Define trait Shape here, with required `area` + `perimeter` and a
// default `describe` that formats the two values. The default body calls
// self.area() and self.perimeter().

// EX 3: Implement Shape for each of Circle, Rectangle, Triangle. Override
// `describe` on Rectangle so the output prefix reads `rectangle (w×h):`.

// EX 4: Define fn report<S: Shape + std::fmt::Debug>(s: &S) that prints
// {s:?}: {s.describe()}.

// EX 5 (optional): Define fn total_area<S: Shape>(shapes: &[S]) -> f64
// that sums .area() across the slice.

fn main() {
    println!("shape-trait starter — fill in each exercise");

    let c = Circle { radius: 2.0 };
    let r = Rectangle { w: 3.0, h: 4.0 };
    let t = Triangle { a: 3.0, b: 4.0, c: 5.0 };

    // Exercise 3 replaces this with real `.describe()` + `report` calls.
    let _ = (&c, &r, &t);
}
