// Starter — a working Box<Node>-based singly-linked list. Exercise 2
// refactors each Node to Rc<RefCell<Node>> so Exercise 3 can share subtrees
// between two lists. The capstone ends with real shared, mutable graph
// state and an optional iterator impl.

struct Node {
    value: i32,
    next: Option<Box<Node>>,
}

struct List {
    head: Option<Box<Node>>,
}

impl List {
    fn new() -> Self {
        List { head: None }
    }

    fn push_front(&mut self, value: i32) {
        let new_node = Box::new(Node {
            value,
            next: self.head.take(),
        });
        self.head = Some(new_node);
    }

    fn print(&self) {
        print!("[");
        let mut cursor = &self.head;
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
    list.push_front(3);
    list.push_front(2);
    list.push_front(1);

    list.print();
    println!("len() = {}", list.len());
}
