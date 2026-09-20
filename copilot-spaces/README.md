# ForgeBoard - Task Management for PixelForge Studios

ForgeBoard is a web-based sprint/task management tool built with Node.js and Express. It helps game development teams at PixelForge Studios track tasks, manage sprints, and collaborate on projects.

## Architecture
- **Backend:** Node.js + Express REST API
- **Database:** SQLite (development), PostgreSQL (production)
- **Auth:** JWT-based authentication
- **Frontend:** Server-rendered HTML (planned: React SPA)

## Key Modules
- `src/tasks.js` — Task CRUD operations
- `src/users.js` — User management
- `src/index.js` — Express server and routing
