# smu-rust-400-collections-practice

Starter for **Course 640 Lesson 5 paired HOL — "Pick the right collection — practice drills."**

The starter ships six stubbed functions. Each exercise fills in ONE function
using the std collection the doc comment specifies.

## Run

```
cargo run
```

The starter prints a welcome line and otherwise does nothing. Each exercise
uncomments the matching call site in `main()` after you fill in the function
body.

## Per-exercise additions

| Exercise | Function | Collection |
|---|---|---|
| 2 | `task_queue_demo` | `VecDeque<&str>` |
| 3 | `word_frequency_sorted` | `BTreeMap<String, u32>` |
| 4 | `dedup_ids` | `HashSet<u64>` |
| 5 | `leaderboard_top3` | `BinaryHeap<i32>` or `BTreeSet<Reverse<i32>>` |
| 6 (optional) | `user_cache_lookup` | `HashMap<u64, String>` |

## Why six stubs instead of one program

Each stub is a self-contained drill. The point of this lab is practicing the
decision — "which std collection is right for this access pattern?" — not
building one app that uses them all.
