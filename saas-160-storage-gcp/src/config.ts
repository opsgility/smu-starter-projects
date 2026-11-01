// Centralized config — reads env once and exposes a typed object.
// STORAGE_TRACK picks between GCS (primary, what the lab runs) and Azure
// (parallel-module alternative — run it against your own Azure account).
import { config } from "dotenv";

config();

type StorageTrack = "gcs" | "azure";

const rawTrack = (process.env.STORAGE_TRACK ?? "gcs").toLowerCase();
if (rawTrack !== "gcs" && rawTrack !== "azure") {
  throw new Error(`STORAGE_TRACK must be gcs or azure (got ${rawTrack})`);
}

export const appConfig = {
  track: rawTrack as StorageTrack,
  gcs: {
    projectId: process.env.GCS_PROJECT_ID ?? "",
    bucket: process.env.GCS_BUCKET ?? "",
  },
  azure: {
    account: process.env.AZURE_STORAGE_ACCOUNT ?? "",
    container: process.env.AZURE_STORAGE_CONTAINER ?? "photos",
  },
  databaseUrl: process.env.DATABASE_URL ?? "",
  port: Number(process.env.PORT ?? 3000),
};
