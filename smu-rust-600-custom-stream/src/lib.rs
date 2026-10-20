use std::pin::Pin;
use std::task::{Context, Poll};
use std::time::Duration;
use futures_core::Stream;
use pin_project_lite::pin_project;
use tokio::time::Sleep;

pin_project! {
    pub struct Ticker {
        count: u64,
        max: u64,
        period: Duration,
        #[pin]
        sleep: Sleep,
    }
}

impl Ticker {
    pub fn new(period: Duration, max: u64) -> Self {
        Self {
            count: 0,
            max,
            period,
            sleep: tokio::time::sleep(period),
        }
    }
}

impl Stream for Ticker {
    type Item = u64;

    fn poll_next(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Option<u64>> {
        let mut this = self.project();
        if *this.count >= *this.max {
            return Poll::Ready(None);
        }

        match this.sleep.as_mut().poll(cx) {
            Poll::Pending => Poll::Pending,
            Poll::Ready(()) => {
                *this.count += 1;
                let next_deadline = tokio::time::Instant::now() + *this.period;
                this.sleep.as_mut().reset(next_deadline);
                Poll::Ready(Some(*this.count))
            }
        }
    }
}
