use tokio::time::{sleep, Duration};

pub async fn fake_fetch(name: &str, ms: u64) -> String {
    sleep(Duration::from_millis(ms)).await;
    format!("{name}:ok")
}
