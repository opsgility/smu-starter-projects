use tokio::time::{sleep, Duration};

pub async fn fake_fetch(name: &str, ms: u64) -> String {
    sleep(Duration::from_millis(ms)).await;
    format!("{name}:ok")
}

pub async fn fake_fetch_fallible(name: &str, ms: u64, fail: bool) -> Result<String, String> {
    sleep(Duration::from_millis(ms)).await;
    if fail {
        Err(format!("{name}:boom"))
    } else {
        Ok(format!("{name}:ok"))
    }
}
