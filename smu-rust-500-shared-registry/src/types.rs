#[derive(Debug, Clone)]
pub struct Station {
    pub id: String,
    pub name: String,
    pub lat: f64,
    pub lon: f64,
    pub last_seen_unix_ms: u64,
}

impl Station {
    pub fn new(id: impl Into<String>) -> Self {
        let id = id.into();
        Self {
            name: format!("Station {id}"),
            id,
            lat: 0.0,
            lon: 0.0,
            last_seen_unix_ms: 0,
        }
    }
}
