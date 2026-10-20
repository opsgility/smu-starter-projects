// Starter — Shape trait + three impls already present. Exercise 2 replaces
// the three `let _X = ...;` lines with Vec<Box<dyn Shape>> + a loop.
// Exercise 3 sums total area. Exercise 4 hits the object-safety wall with
// clone_box and applies the Sized where-clause fix. Exercise 5 (optional)
// converts to Vec<&dyn Shape>.

pub trait Shape {
    fn area(&self) -> f64;
    fn perimeter(&self) -> f64;

    fn describe(&self) -> String {
        format!("area={:.2} perimeter={:.2}", self.area(), self.perimeter())
    }
}

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

impl Shape for Circle {
    fn area(&self) -> f64 {
        std::f64::consts::PI * self.radius * self.radius
    }
    fn perimeter(&self) -> f64 {
        2.0 * std::f64::consts::PI * self.radius
    }
}

impl Shape for Rectangle {
    fn area(&self) -> f64 {
        self.w * self.h
    }
    fn perimeter(&self) -> f64 {
        2.0 * (self.w + self.h)
    }
}

impl Shape for Triangle {
    fn area(&self) -> f64 {
        let s = (self.a + self.b + self.c) / 2.0;
        (s * (s - self.a) * (s - self.b) * (s - self.c)).sqrt()
    }
    fn perimeter(&self) -> f64 {
        self.a + self.b + self.c
    }
}

fn main() {
    println!("dyn-shape starter — fill in each exercise");

    // Exercise 2 replaces these three lines with a Vec<Box<dyn Shape>>.
    let _c = Circle { radius: 2.0 };
    let _r = Rectangle { w: 3.0, h: 4.0 };
    let _t = Triangle { a: 3.0, b: 4.0, c: 5.0 };
}
