use tokio::net::TcpListener;

#[tokio::main]
async fn main() -> std::io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:0").await?;
    println!("listening on {}", listener.local_addr()?);
    smu_rust_600_tcp_echo::run(listener).await
}
