use std::time::Instant;
use tokio::sync::broadcast;

#[derive(Clone, Debug)]
pub struct ChatMsg {
    pub from_id: usize,
    pub text: String,
}

pub type Tx = broadcast::Sender<ChatMsg>;

#[derive(Debug)]
pub struct ConnectionState {
    pub id: usize,
    pub nick: String,
    pub joined_at: Instant,
}

impl ConnectionState {
    pub fn new(id: usize) -> Self {
        Self { id, nick: format!("user_{}", id), joined_at: Instant::now() }
    }
}
