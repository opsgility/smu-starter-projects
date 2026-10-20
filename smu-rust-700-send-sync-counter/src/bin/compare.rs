//! Driver that invokes both benches and prints the ratio.

#[path = "../../benches/counter_bench.rs"]
mod counter_bench;

fn main() {
    let threads = 8;
    let iterations = 1_000_000;
    let atomic = counter_bench::bench_atomic(threads, iterations);
    let mutex = counter_bench::bench_mutex(threads, iterations);
    let ratio = mutex.as_secs_f64() / atomic.as_secs_f64();
    println!("atomic: {:?}", atomic);
    println!("mutex:  {:?}", mutex);
    println!("ratio:  {:.1}x faster", ratio);
}
