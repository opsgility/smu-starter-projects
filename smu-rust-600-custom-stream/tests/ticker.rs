use smu_rust_600_custom_stream::Ticker;
use std::time::Duration;
use tokio_stream::StreamExt;

#[tokio::test]
async fn yields_three_ticks() {
    let t = Ticker::new(Duration::from_millis(50), 3);
    tokio::pin!(t);
    let mut received = vec![];
    while let Some(n) = t.next().await {
        received.push(n);
    }
    assert_eq!(received, vec![1, 2, 3]);
}
