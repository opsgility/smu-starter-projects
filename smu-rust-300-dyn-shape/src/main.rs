// Course 3 Lesson 5 HOL — Heterogeneous shapes with Vec<Box<dyn Shape>>.
//
// Starter ships with Shape trait + Circle/Rectangle/Triangle impls complete,
// copied forward from Lesson 4's work. Your job is to use dyn Shape to store
// different shape types in a single collection.

use std::f64::consts::PI;

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

impl Shape for Circle {
    fn area(&self) -> f64 {
        PI * self.radius * self.radius
    }
    fn perimeter(&self) -> f64 {
        2.0 * PI * self.radius
    }
}

#[derive(Debug)]
pub struct Rectangle {
    pub w: f64,
    pub h: f64,
}

impl Shape for Rectangle {
    fn area(&self) -> f64 {
        self.w * self.h
    }
    fn perimeter(&self) -> f64 {
        2.0 * (self.w + self.h)
    }
}

#[derive(Debug)]
pub struct Triangle {
    pub a: f64,
    pub b: f64,
    pub c: f64,
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

    // Three concrete shapes you'll put into a heterogeneous collection.
    let _c = Circle { radius: 2.0 };
    let _r = Rectangle { w: 3.0, h: 4.0 };
    let _t = Triangle { a: 3.0, b: 4.0, c: 5.0 };

    // EX 2: build `let shapes: Vec<Box<dyn Shape>> = vec![...];` and iterate.

    // EX 3: compute total area with .iter().map(|s| s.area()).sum::<f64>().

    // EX 4: add a NOT-object-safe method to Shape and observe the error.

    // EX 5 (optional): convert Vec<Box<dyn Shape>> to Vec<&dyn Shape>.
}
