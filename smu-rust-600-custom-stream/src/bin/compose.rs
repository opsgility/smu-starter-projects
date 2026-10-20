use smu_rust_600_custom_stream::Ticker;
use std::time::Duration;

#[tokio::main]
async fn main() {
    let _ = Ticker::new(Duration::from_millis(20), 10);
    todo!("map + filter + take + collect on Ticker");
}
