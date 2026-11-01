// Thumbnail-status helper — writes trail_photos.status transitions in response
// to object-finalize events. The thumbnail function (functions/thumbnail/)
// POSTs here when it finishes work; the API also exposes a webhook on
// GET /photos/:id/thumb-url (L5 Exercise 4).
import { query } from "./db.js";

export async function markReady(
  storageKey: string,
  dims: { width: number; height: number },
): Promise<void> {
  await query(
    "UPDATE trail_photos SET status = 'ready', width_px = $2, height_px = $3 WHERE storage_key = $1",
    [storageKey, dims.width, dims.height],
  );
}

export async function markFailed(storageKey: string): Promise<void> {
  await query(
    "UPDATE trail_photos SET status = 'failed' WHERE storage_key = $1",
    [storageKey],
  );
}
