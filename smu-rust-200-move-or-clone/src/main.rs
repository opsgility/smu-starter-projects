fn main() {
    println!("move_or_clone starter — pick a case to run");
    println!("  cargo run --bin case01");
    println!("  cargo run --bin case02");
    println!("  cargo run --bin case03");
    println!("  cargo run --bin case04");
    println!("  cargo run --bin case05");
    println!("  cargo run --bin case06");
    println!();
    println!("Each case is a broken program. Read the compiler error,");
    println!("decide between move / clone / &/&mut, apply the smallest fix,");
    println!("and re-run until you see `caseNN passed`.");
}
