// collections-practice starter — fill in each exercise.
//
// Each stub below reads a doc comment that states what the function should do
// and which std collection the exercise asks you to use. The bodies all panic
// via `todo!()` until you fill them in.

fn main() {
    println!("collections-practice starter — fill in each exercise");

    // Ex 2:
    // task_queue_demo();

    // Ex 3:
    // word_frequency_sorted();

    // Ex 4:
    // let unique = dedup_ids(&[7, 1, 7, 3, 1, 9]);
    // println!("unique: {unique:?}");

    // Ex 5:
    // let top = leaderboard_top3(&[42, 17, 93, 58, 11, 76, 65]);
    // println!("top3: {top:?}");

    // Ex 6:
    // user_cache_lookup();
}

/// Simulate a 3-task FIFO work queue.
///
/// Push three task names onto the back of the queue, then pop two from the
/// front and print each one. Print the final length and the remaining task.
///
/// Required collection: `std::collections::VecDeque<&str>`.
fn task_queue_demo() {
    todo!("Ex 2: use VecDeque — push_back three tasks, pop_front two, print the rest");
}

/// Count how often each word appears in a short sentence and print the counts
/// alphabetically by word.
///
/// Required collection: `std::collections::BTreeMap<String, u32>` (so the
/// iteration order is sorted by key).
fn word_frequency_sorted() {
    todo!("Ex 3: use BTreeMap — count words in a sentence, print alphabetically");
}

/// Return the unique values from `ids`, in any order.
///
/// Required collection: `std::collections::HashSet<u64>`.
fn dedup_ids(ids: &[u64]) -> Vec<u64> {
    todo!("Ex 4: use HashSet — insert each id, collect the result into Vec<u64>");
}

/// Return the three highest scores from `scores`, in descending order.
///
/// Required collection: a sort-descending structure. Use `BTreeSet` with a
/// wrapper type whose `Ord` impl is reversed, OR use `std::collections::BinaryHeap`
/// (which is a max-heap by default).
fn leaderboard_top3(scores: &[i32]) -> Vec<i32> {
    todo!("Ex 5: use BinaryHeap or BTreeSet with reversed Ord — return top 3 descending");
}

/// Look up a user name by numeric id.
///
/// Build a small `HashMap<u64, String>` with 3 entries, then print the lookup
/// results for one key that exists and one that does not.
///
/// Required collection: `std::collections::HashMap<u64, String>`.
fn user_cache_lookup() {
    todo!("Ex 6 (optional): use HashMap — insert 3 (id, name) pairs, .get() two, print the Option<&String> results");
}
