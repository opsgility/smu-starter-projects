use tokio::net::TcpListener;

pub async fn run(listener: TcpListener) -> std::io::Result<()> {
    loop {
        let (_sock, _) = listener.accept().await?;
        // TODO Exercise 3 — move the per-connection handler here
    }
}
