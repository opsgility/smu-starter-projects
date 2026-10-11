---
mode: edit
description: Scaffold a full CRUD minimal-API module for a Production.* table in Halcyon.Adventure.Api.
---

Scaffold a complete CRUD endpoint set for the AdventureWorks table named in the chat.

Produce the following files under a new `${input:areaName}/` folder, matching the shape in `Products/`:

- `${input:areaName}Api.cs` — a `public static class` with a `Map${input:areaName}Api` extension method on `RouteGroupBuilder` that registers GET-all, GET-by-id, POST, PUT and DELETE endpoints, each with `.WithName`, `.WithSummary` and `.WithDescription`.
- `${input:entity}Dto.cs` — a `record` projection returned on reads.
- `Create${input:entity}Request.cs` — a `record` request body with the fields a POST must accept.
- `Update${input:entity}Request.cs` — a `record` request body with the fields a PUT must accept.

Follow the Halcyon conventions in `.github/copilot-instructions.md`:

- Endpoints return `TypedResults.*` wrapped in `Results<T1, T2>` where more than one status code is possible.
- Reads are `.AsNoTracking()`.
- Writes set `ModifiedDate = DateTime.UtcNow` and generate a `rowguid` on insert.
- Project EF entities to the DTO via a private static `ToDto` method — no AutoMapper.
- Attach the group to the parent versioned group with `.HasApiVersion(new ApiVersion(1, 0))` and `.WithTags("${input:areaName}")`.
- Do NOT add DataAnnotations yet. Validation lands in a follow-up PR.

Register the new module in `Program.cs` by calling `versionedGroup.Map${input:areaName}Api();` next to the existing `MapProductsApi()` call.

Scaffold the EF entity in `Data/${input:entity}.cs` and add a `DbSet<${input:entity}>` to `AdventureWorksContext`. Match the real column names on `Production.${input:tableName}` — do not guess at column casing.

Finish by listing the three smoke-test curl requests the student should run to verify the CRUD loop (list, create, delete).
