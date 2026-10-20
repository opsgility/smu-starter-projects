use smu_rust_600_timeout_cancel::fake_fetch;

#[tokio::main]
async fn main() {
    let _ = fake_fetch;
    todo!("wrap fake_fetch with tokio::time::timeout; print success and timeout cases");
}
