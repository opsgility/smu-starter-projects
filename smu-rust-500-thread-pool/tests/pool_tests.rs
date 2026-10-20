use rust_concurrent_thread_pool::ThreadPool;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;

#[test]
fn test_constructor_creates_workers() {
    let pool = ThreadPool::new(4);
    assert_eq!(pool.worker_count(), 4);
}

#[test]
fn test_execute_runs_a_job() {
    let flag = Arc::new(AtomicUsize::new(0));
    {
        let pool = ThreadPool::new(2);
        let f = Arc::clone(&flag);
        pool.execute(move || { f.store(42, Ordering::Relaxed); });
        std::thread::sleep(std::time::Duration::from_millis(100));
    }
    assert_eq!(flag.load(Ordering::Relaxed), 42);
}

#[test]
fn test_many_jobs() {
    let count = Arc::new(AtomicUsize::new(0));
    {
        let pool = ThreadPool::new(4);
        for _ in 0..1000 {
            let c = Arc::clone(&count);
            pool.execute(move || { c.fetch_add(1, Ordering::Relaxed); });
        }
    }
    assert_eq!(count.load(Ordering::Relaxed), 1000);
}

#[test]
fn test_drop_joins_cleanly() {
    let count = Arc::new(AtomicUsize::new(0));
    {
        let pool = ThreadPool::new(4);
        for _ in 0..100 {
            let c = Arc::clone(&count);
            pool.execute(move || {
                std::thread::sleep(std::time::Duration::from_millis(10));
                c.fetch_add(1, Ordering::Relaxed);
            });
        }
        // Pool drops here. If Drop is correct, all 100 jobs run before this
        // function returns.
    }
    assert_eq!(count.load(Ordering::Relaxed), 100);
}
