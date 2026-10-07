# FleetBoard Architecture

## Task state machine

FleetBoard tasks live in one of four statuses. The allowed transitions are:

| From          | To                           |
|---------------|------------------------------|
| `open`        | `in-progress`                |
| `in-progress` | `in-review`, `open`          |
| `in-review`   | `done`, `in-progress`        |
| `done`        | `in-progress` (reopen only)  |

A valid transition must be listed above. `updateTaskStatus(id, newStatus)` in `src/tasks.js` is the only sanctioned entry point for changing a task's status.

## Operator roles

Four roles exist in FleetBoard. Each role has a specific set of permissions on tasks.

| Role        | Permissions                                                                  |
|-------------|------------------------------------------------------------------------------|
| `admin`     | create, read, update, delete; transition any task between any two statuses   |
| `developer` | create, read, update; transition `open` → `in-progress` and `→ in-review`    |
| `designer`  | create, read, update; transition `open` → `in-progress` and `→ in-review`    |
| `qa`        | read, update; transition `in-review` → `done` and `in-review` → `in-progress` |

Only `admin` operators can delete tasks or reopen a `done` task.

## Services

- **Task service** (`src/tasks.js`) — authoritative task store, state machine enforcement
- **Operator service** (`src/users.js`) — operator records and role lookups
- **Validators** (`src/validators.js`) — shared validation helpers (built in the Prompt Engineering lab)
- **Utils** (`src/utils.js`) — formatting + slug helpers used across services
