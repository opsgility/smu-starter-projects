# orphan-rule starter

Exercise 1: `cargo build` fails with E0117 because the starter attempts to
`impl ToString for Vec<i32>` — neither `ToString` nor `Vec` belongs to this
crate.

Exercise 2: comment the broken `impl` block out so the project builds.

Exercise 3: uncomment the newtype stub (`struct IntList(Vec<i32>)`) and
implement `Display` on it — now the trait is foreign but the type is ours.

Exercise 4: uncomment the extension-trait stub (`Summable` + blanket impl)
— now the trait is ours and we attach it to every `IntoIterator<Item = i32>`.

Exercise 5 (optional): add `impl Deref<Target = Vec<i32>>` so IntList
inherits every method on `Vec<i32>`.
