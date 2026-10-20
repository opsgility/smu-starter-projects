#[derive(Debug, Clone)]
pub struct RawPacket {
    pub source_id: u32,
    pub seq: u32,
    pub payload: Vec<u8>,
}

#[derive(Debug, Clone)]
pub struct ParsedReading {
    pub source_id: u32,
    pub seq: u32,
    pub byte_sum: u64,
}
