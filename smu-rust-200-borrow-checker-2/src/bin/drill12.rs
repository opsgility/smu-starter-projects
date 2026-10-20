// EXPECTED ERROR: E0597 — `name` does not live long enough
// HINT: `Session<'a>` holds a `&'a str`. The code builds the Session inside
//       an inner scope where `name` lives, then tries to use the Session
//       OUTSIDE that scope. `name` dies at the inner `}`; the Session's
//       reference would dangle. Fix: move the `let name = ...` binding OUT
//       of the inner scope so it lives for the same scope as `session`.
// FIX ME: Make this compile.

struct Session<'a> {
    label: &'a str,
    tick: u32,
}

fn main() {
    let session;
    {
        let name = String::from("deploy-run");
        session = Session { label: &name, tick: 7 };
    }

    println!("session {} at tick {}", session.label, session.tick);
}
