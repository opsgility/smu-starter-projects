// workspace-split starter — a single-crate program for Course 3 Lesson 9.
// Across the exercises you refactor this flat crate into a cargo workspace
// with a reusable `shapes-core` library + a `shapes-cli` binary.

trait Shape {
    fn area(&self) -> f64;
    fn describe(&self) -> String {
        format!("area = {:.2}", self.area())
    }
}

#[derive(Debug, Clone)]
struct Circle {
    radius: f64,
}

#[derive(Debug, Clone)]
struct Rectangle {
    width: f64,
    height: f64,
}

impl Shape for Circle {
    fn area(&self) -> f64 {
        std::f64::consts::PI * self.radius * self.radius
    }

    fn describe(&self) -> String {
        format!("circle (r={}): area = {:.2}", self.radius, self.area())
    }
}

impl Shape for Rectangle {
    fn area(&self) -> f64 {
        self.width * self.height
    }

    fn describe(&self) -> String {
        format!(
            "rectangle ({}x{}): area = {:.2}",
            self.width,
            self.height,
            self.area()
        )
    }
}

fn print_shapes(shapes: &[&dyn Shape]) {
    for s in shapes {
        println!("{}", s.describe());
    }
}

fn main() {
    let c = Circle { radius: 2.0 };
    let r = Rectangle {
        width: 3.0,
        height: 4.0,
    };
    let shapes: Vec<&dyn Shape> = vec![&c, &r];
    println!("workspace-split starter — single-crate shape printer");
    print_shapes(&shapes);
}
