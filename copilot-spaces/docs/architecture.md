# ForgeBoard Architecture

## Components
1. **API Layer** — Express routes handling HTTP requests
2. **Service Layer** — Business logic for tasks, users, sprints
3. **Data Layer** — SQLite database with raw SQL queries
4. **Auth Middleware** — JWT validation on protected routes

## Data Model
- **Task**: id, title, description, status (todo/in-progress/done), priority (low/medium/high/critical), assigneeId, sprintId, createdAt, updatedAt
- **User**: id, name, email, role (developer/lead/manager), teamId
- **Sprint**: id, name, startDate, endDate, status (planning/active/completed)
