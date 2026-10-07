# FleetBoard Core

FleetBoard is NorthPeak Robotics' internal task and operator service for coordinating warehouse robot work. This repository is the Node.js reference implementation used by the Fleet Engineering squad.

## Modules

- `src/tasks.js` — in-memory task CRUD + the FleetBoard task state machine
- `src/users.js` — fleet operator roster with role-based task permissions
- `src/utils.js` — formatting + validation helpers (ingredients for few-shot prompting)
- `src/validators.js` — intentionally empty; the Copilot prompting lab builds this out

## State machine (task statuses)

FleetBoard tasks move through four statuses. See `docs/architecture.md` for the full transition map.

```
open  →  in-progress  →  in-review  →  done
```

## Operator roles

Four operator roles exist in FleetBoard: `admin`, `developer`, `designer`, `qa`. See `docs/architecture.md` for the role-to-task permission map.

## Running

```
npm install
npm start
```
