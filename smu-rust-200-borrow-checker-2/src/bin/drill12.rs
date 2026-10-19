// EXPECTED ERROR: E0597 `name` does not live long enough
// HINT: `Session` holds a `&'a str` for `label`. Its lifetime can't outlive the
//       String it points at. In this code, `name` is created in an inner scope
//       and the Session referencing it is used outside that scope.
//       Fix: either (a) move the `name` declaration out so it lives as long as
//       the Session, OR (b) change Session.label from `&'a str` to `String` so
//       the Session owns its label.

struct Session<'a> {
    label: &'a str,
    tick: u32,
}

fn main() {
    let session;
    {
        let name = String::from("deploy-run");
        // FIX ME: Session.label references `name`, which only lives inside this
        //         inner scope. Move `let name = ...` up to the outer scope so
        //         name outlives session.
        session = Session { label: &name, tick: 7 };
    }

    println!("session {} at tick {}", session.label, session.tick);
}
