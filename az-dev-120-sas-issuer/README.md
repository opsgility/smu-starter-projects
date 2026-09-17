# az-dev-120-sas-issuer

Anchorline direct-browser-upload issuer. ASP.NET Core minimal API with:

- `POST /api/upload/prepare?name={filename}` — returns a user-delegation SAS URL for a 15-min write to `customer-uploads`
- Static `index.html` at `/` — file picker that fetches the SAS and PUTs the file directly to blob

The API's identity (MI or `az login` user) needs `Storage Blob Delegator` + write permission on the target container.
