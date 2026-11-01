// Facade — picks GCS or Azure based on STORAGE_TRACK. Rest of the app imports
// `storage` and never touches gcs.ts / blob.ts directly.
import { appConfig } from "./config.js";
import { gcs } from "./gcs.js";
import { blob } from "./blob.js";

export const storage = appConfig.track === "gcs" ? gcs : blob;
