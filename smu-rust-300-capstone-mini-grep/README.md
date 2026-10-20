# mini-grep capstone starter

Cargo workspace with two member crates:

- `grep-core/` — library. Three empty sub-modules (`error`, `pattern`,
  `source`) you fill in across Exercises 2, 3, and 4.
- `grep-cli/` — binary. Exercise 5 wires `clap::Parser` + a generic
  `run<P: Pattern>` fn + `anyhow::Context`.

Fixture at `fixtures/sample.txt` is the Gettysburg Address — small enough
to eyeball matches, long enough that the regex and literal flags both
produce visible output.

Expected final shape:

```
cargo run -p grep-cli -- --regex "n[aei]tion" fixtures/sample.txt
```
