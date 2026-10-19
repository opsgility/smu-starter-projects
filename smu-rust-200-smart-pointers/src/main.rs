// smart-pointers starter — fill in each section as you go.
//
// Section 1: Tree with Box
// Section 2: Shared files with Rc
// Section 3: Threads with Arc
//
// Exercise 1 just runs this stub and prints the welcome line below.

fn main() {
    println!("smart-pointers starter — see README.md");

    // SECTION 1: Tree with Box
    // (Exercise 2 fills this in — define `enum Tree`, construct a 7-node
    // balanced tree, call sum_tree + print the total here.)

    // SECTION 2: Shared files with Rc
    // (Exercise 3 fills this in — define `struct File`, wrap in Rc<File>,
    // create 3 files + 2 directories each holding a Vec<Rc<File>>,
    // print each directory's files + Rc::strong_count on a shared file.)

    // SECTION 3: Threads with Arc
    // (Exercise 4 fills this in — define File_arc or re-use the File struct,
    // Arc-wrap it, spawn a thread that reads the file name through the Arc,
    // join + verify the main thread still sees it.)
}
