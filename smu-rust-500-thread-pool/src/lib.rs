use std::thread::JoinHandle;

pub type Job = Box<dyn FnOnce() + Send + 'static>;

pub struct ThreadPool {
    _todo: Vec<JoinHandle<()>>,
}

impl ThreadPool {
    pub fn new(_size: usize) -> Self {
        todo!("Exercise 2: implement new(size) with workers behind an Arc<Mutex<Receiver<Job>>>");
    }

    pub fn execute<F>(&self, _f: F)
    where
        F: FnOnce() + Send + 'static,
    {
        todo!("Exercise 2: implement execute by sending a boxed closure on the channel");
    }

    pub fn worker_count(&self) -> usize {
        self._todo.len()
    }
}

// Exercise 3 adds: impl Drop for ThreadPool
