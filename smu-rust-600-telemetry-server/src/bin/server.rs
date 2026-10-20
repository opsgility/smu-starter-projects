use smu_rust_600_telemetry_server::{ChatMsg, Tx};
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;
use tokio::net::TcpListener;
use tokio::sync::broadcast;

#[tokio::main]
async fn main() -> std::io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:0").await?;
    let addr = listener.local_addr()?;
    println!("telemetry server listening on {}", addr);

    let (tx, _rx0): (Tx, _) = broadcast::channel::<ChatMsg>(128);
    let next_id = Arc::new(AtomicUsize::new(0));

    loop {
        let (sock, peer) = listener.accept().await?;
        let id = next_id.fetch_add(1, Ordering::Relaxed);
        let tx_c = tx.clone();
        tokio::spawn(async move {
            println!("[{}] accepted {}", id, peer);
            drop(sock); drop(tx_c);
        });
    }
}
