// Exercise 3 — chat room core. Fill in the per-connection handler.

use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};
use tokio::net::TcpListener;
use tokio::sync::broadcast;

#[tokio::main]
async fn main() -> std::io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:7000").await?;
    let (tx, _rx0) = broadcast::channel::<(usize, String)>(128);
    let mut next_id = 0usize;

    loop {
        let (sock, _) = listener.accept().await?;
        let id = next_id; next_id += 1;
        let tx = tx.clone();
        let rx = tx.subscribe();
        tokio::spawn(async move {
            // TODO: fill in handle(id, sock, tx, rx) per the exercise
            drop(sock); drop(tx); drop(rx);
            let _ = id;
        });
    }
}
