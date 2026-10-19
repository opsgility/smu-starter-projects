// Course 640 — SMU-RUST-400 Lesson 4 paired HOL
// Starter for "Fn, FnMut, FnOnce — closure drills"
//
// Each `// EX N:` section is empty on purpose. The exercises walk you
// through filling in one section at a time. `cargo run` will print the
// welcome line + whatever sections you've uncommented so far.

fn main() {
    println!("closures-practice starter — fill in each exercise");

    // EX 2: Fn callback
    // Define `apply_twice` and `doubler` here, then uncomment:
    // println!("ex 2: apply_twice(doubler, 5) = {}", apply_twice(doubler, 5));

    // EX 3: FnMut counter
    // Build a closure that captures a mutable counter, then uncomment:
    // let mut count = 0;
    // let mut incr = || { count += 1; count };
    // println!("ex 3: incr -> {} {} {}", incr(), incr(), incr());

    // EX 4: FnOnce consumer
    // Build a `move` closure that consumes a captured String, then uncomment:
    // let name = String::from("Rust");
    // let greet = move || {
    //     println!("ex 4: hello, {name}");
    //     drop(name);
    // };
    // greet();

    // EX 5: struct holding a closure
    // Define `Handler` + build one + call it, then uncomment:
    // let h = Handler {
    //     f: Box::new(|msg| println!("ex 5: handler got {msg}")),
    // };
    // (h.f)("hello from main");

    // EX 6 (optional): return a closure from a function
    // Define `multiplier` and call it, then uncomment:
    // let times3 = multiplier(3);
    // println!("ex 6: times3(7) = {}", times3(7));
}
