# az-dev-110-rest-api

Anchorline Outdoors' Todos REST API on Azure Functions.

## Endpoints

- `GET /api/todos` — list all
- `GET /api/todos/{id}` — get one
- `POST /api/todos` — create (added in Exercise 2)
- `PUT /api/todos/{id}` — update (added in Exercise 2)
- `DELETE /api/todos/{id}` — delete (added in Exercise 2)
- `GET /api/swagger/ui` — Swagger UI

## Storage

In-memory `ConcurrentDictionary` for lab simplicity — state resets on each function-app instance restart. In production this would be Cosmos or Table Storage (Module 7 shows the input/output binding pattern).
