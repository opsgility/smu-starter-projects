use smu_rust_600_timeout_cancel::fake_fetch;
use tokio_util::sync::CancellationToken;

#[tokio::main]
async fn main() {
    let _ = (fake_fetch, CancellationToken::new());
    todo!("spawn 5 fetch workers sharing a CancellationToken; cancel after 500ms");
}
