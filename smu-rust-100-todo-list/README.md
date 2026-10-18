# smu-rust-100-todo-list

Starter project for **Lesson 14 — Build a tiny in-memory todo list** (capstone of SMU-RUST-100: Programming Foundations with Rust).

Across the lab exercises you grow this empty-ish starter into a working interactive todo list that lives in memory for a single session. You will define a `Todo` struct, keep a `Vec<Todo>`, build a REPL loop that accepts commands, parse command arguments, and validate indices without ever panicking.

## Run

```
cargo run
```

On the starter you will see:

```
todo-list starter — type 'help' once the REPL loop is in place
```

Each exercise replaces this `main()` with a little more functionality.

## What each exercise adds

| # | Exercise | What `main()` can do after it |
|---|---|---|
| 1 | Open the project and run the smoke test | Prints the welcome line |
| 2 | Define the `Todo` struct and pre-populate a `Vec<Todo>` | Prints the three sample todos via `{:?}` |
| 3 | Add the REPL loop with `list` and `quit` | Reads commands from stdin, prints todos on `list`, exits on `quit` |
| 4 | Add `add <text>` | Appends a new todo with an auto-incrementing id |
| 5 | Add `done <n>` and `remove <n>` | Marks or removes a todo by its 1-based number; prints a helpful error on bad input |
| 6 | (Optional) Polish with checkboxes + `help` | Pretty-prints todos with `[x]` / `[ ]` and lists all commands |

## Command vocabulary (end state)

| Command | Example | Behavior |
|---|---|---|
| `list` | `list` | Print every todo, 1-based, with a checkbox if Exercise 6 is complete |
| `add` | `add buy milk` | Append a new todo |
| `done` | `done 1` | Mark todo #1 as done |
| `remove` | `remove 2` | Remove todo #2 |
| `help` | `help` | Print the command vocabulary (Exercise 6) |
| `quit` | `quit` | Exit the REPL |

## Container

Runs on the `vscode-rust` container variant (CodeEditorType = 16). Rust 1.99.1, 2024 edition. No external crates.

## Learning context

This is the capstone of Course 1 (Programming Foundations with Rust). Course 2 (The Rust Ownership Model) takes the `&mut Vec<Todo>` method pattern you build here and makes the ownership + borrowing story explicit.
