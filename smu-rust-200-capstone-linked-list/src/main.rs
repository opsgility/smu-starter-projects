// Course 2 capstone starter: Box<Node>-based singly-linked list.
// The code compiles and runs. Your job across the exercises is to
// REFACTOR it to Rc<RefCell<Node>> so two lists can share and mutate
// the same tail. No bug fixes needed in the starter.

struct Node {
    value: i32,
    next: Option<Box<Node>>,
}

impl Node {
    fn new(value: i32) -> Self {
        Node { value, next: None }
    }
}

struct List {
    head: Option<Box<Node>>,
}

impl List {
    fn new() -> Self {
        List { head: None }
    }

    fn push_front(&mut self, value: i32) {
        let mut new_node = Box::new(Node::new(value));
        new_node.next = self.head.take();
        self.head = Some(new_node);
    }

    fn print(&self) {
        let mut cursor = &self.head;
        print!("[");
        let mut first = true;
        while let Some(node) = cursor {
            if !first {
                print!(", ");
            }
            print!("{}", node.value);
            first = false;
            cursor = &node.next;
        }
        println!("]");
    }

    fn len(&self) -> usize {
        let mut n = 0;
        let mut cursor = &self.head;
        while let Some(node) = cursor {
            n += 1;
            cursor = &node.next;
        }
        n
    }
}

fn main() {
    let mut list = List::new();
    // Push 3 then 2 then 1 so the printed order is [1, 2, 3].
    list.push_front(3);
    list.push_front(2);
    list.push_front(1);

    list.print();
    println!("len() = {}", list.len());
}
