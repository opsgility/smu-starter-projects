# az-dev-120-dms-capstone

Anchorline Document Management System — end-to-end demo tying together:

- Per-tenant blob containers (`tenant-{id}`).
- User-delegation SAS for browser-direct uploads (no bytes through the API).
- Metadata + blob index tags applied post-upload.
- Server-side tag query via `FindBlobsByTagsAsync`.

## Endpoints

- `POST /api/upload/prepare?tenantId=X&name=Y` — issues a 15-min write SAS.
- `POST /api/docs` — registers metadata + tags after upload.
- `GET /api/docs?tenantId=X&documentType=Y&year=Z` — searches via blob index tags.
- `/` — minimal HTML UI for the upload + search flows.

The API's identity needs `Storage Blob Data Contributor` + `Storage Blob Delegator` on the storage account.
