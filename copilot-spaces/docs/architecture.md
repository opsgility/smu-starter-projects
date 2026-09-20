# ForgeBoard Architecture

## Overview

ForgeBoard is a task management API for game development teams at PixelForge Studios. It is built with Express.js and uses an in-memory data store for simplicity.

## Components

1. **API Layer** — Express routes handling HTTP requests for tasks and users
2. **Task Module** (`src/tasks.js`) — Business logic and data for task management
3. **User Module** (`src/users.js`) — Team member management and role definitions
4. **Server** (`src/index.js`) — Express application setup and route mounting

## Task Module

### Data Model

Each task has the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | number | Unique identifier |
| `title` | string | Short description of the task |
| `status` | string | Current state (see Task State Machine below) |
| `priority` | string | `low`, `medium`, `high`, or `critical` |
| `assigneeId` | number | ID of the assigned team member |
| `createdAt` | ISO 8601 | Timestamp when task was created |

### Task State Machine

Tasks move through the following states:

```
Open → In Progress → In Review → Done
           ↑               |
           └───────────────┘
          (only In Review can return to Open)
```

**Allowed transitions:**
- `open` → `in-progress` (developer picks up the task)
- `in-progress` → `in-review` (developer submits for review)
- `in-review` → `done` (reviewer approves)
- `in-review` → `open` (reviewer requests changes — task goes back to queue)

**Business rules:**
- Only tasks in `in-review` status may transition back to `open`
- Tasks that are `done` cannot be re-opened (create a new task instead)
- A task must pass through `in-review` before it can be marked `done`

### Valid Statuses

The `VALID_STATUSES` array in `tasks.js` defines the allowed values:

```javascript
const VALID_STATUSES = ['open', 'in-progress', 'in-review', 'done'];
```

## User Module

### Roles and Permissions

ForgeBoard has four user roles:

| Role | Can Create Tasks | Can Update Status | Can Delete Tasks | Can Manage Users |
|------|-----------------|------------------|------------------|-----------------|
| `admin` | Yes | Yes | Yes | Yes |
| `developer` | Yes | Yes (own tasks) | No | No |
| `designer` | Yes | Yes (own tasks) | No | No |
| `qa` | No | Yes (to `in-review` or `done`) | No | No |

### Valid Roles

The `VALID_ROLES` array in `users.js` defines the allowed values:

```javascript
const VALID_ROLES = ['admin', 'developer', 'designer', 'qa'];
```

## API Endpoints

### Tasks

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/tasks` | List all tasks (supports `?status=` and `?priority=` filters) |
| GET | `/api/tasks/:id` | Get a task by ID |
| POST | `/api/tasks` | Create a new task |
| PUT | `/api/tasks/:id` | Update a task |

### Users

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/users` | List all team members |
| GET | `/api/users/:id` | Get a user by ID |

## Known Limitations

- The `updateTaskStatus` function in `tasks.js` does not enforce the state machine transitions — it accepts any valid status regardless of the current status. This is a known discrepancy between the architecture specification and the implementation.
- Data is stored in memory and resets when the server restarts.
- There is no authentication middleware — all endpoints are public.
