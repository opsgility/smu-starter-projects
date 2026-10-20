// Exercise 2 adds apply_twice<F: Fn(i32) -> i32> + doubler and uncomments EX 2.
// Exercise 3 uncomments EX 3 (FnMut counter closure).
// Exercise 4 uncomments EX 4 (FnOnce consumer with move + drop).
// Exercise 5 defines struct Handler { f: Box<dyn Fn(&str)> } and uncomments EX 5.
// Exercise 6 (optional) adds multiplier() factory and uncomments EX 6.

fn main() {
    println!("closures-practice starter — fill in each exercise");

    // EX 2: Fn callback
    // println!("ex 2: apply_twice(doubler, 5) = {}", apply_twice(doubler, 5));

    // EX 3: FnMut counter
    // let mut count = 0;
    // let mut incr = || {
    //     count += 1;
    //     count
    // };
    // println!("ex 3: incr -> {} {} {}", incr(), incr(), incr());

    // EX 4: FnOnce consumer
    // let name = String::from("Rust");
    // let greet = move || {
    //     println!("ex 4: hello, {name}");
    //     drop(name);
    // };
    // greet();

    // EX 5: struct holding a closure
    // let h = Handler {
    //     f: Box::new(|msg| println!("ex 5: handler got {msg}")),
    // };
    // (h.f)("hello from main");

    // EX 6 (optional): return a closure from a function
    // let times3 = multiplier(3);
    // println!("ex 6: times3(7) = {}", times3(7));
}
