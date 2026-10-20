use smu_rust_600_timeout_cancel::fake_fetch;

#[tokio::main]
async fn main() {
    let _ = fake_fetch;
    todo!("50 fetches with Semaphore(8) bounded concurrency; print elapsed");
}
