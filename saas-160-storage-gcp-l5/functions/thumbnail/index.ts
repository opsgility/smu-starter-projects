// Lumen Trail thumbnail trigger — SAAS-160 Lesson 5 starter.
//
// This is a Cloud Functions (2nd gen) HTTP/CloudEvent entry point stub.
// Deploy with:
//   gcloud functions deploy lumen-trail-thumbnail \
//     --gen2 \
//     --runtime=nodejs22 \
//     --region=us-central1 \
//     --source=. \
//     --entry-point=onPhotoFinalize \
//     --trigger-event-filters=type=google.cloud.storage.object.v1.finalized \
//     --trigger-event-filters=bucket=$GCS_BUCKET
//
// The L5 exercises direct Claude Code to:
//   1. Parse the CloudEvent payload to pull the storage_key.
//   2. Download the object with the Storage SDK.
//   3. Resize it with sharp (preinstalled in the lab).
//   4. Upload the thumbnail back under photos/thumbs/<key>.
//   5. Call markReady() on the API with the final width/height.
//
// The equivalent Azure trigger lives in a sibling folder on the SAAS-165
// branch (parallel-module reading in SAAS-160's exercises).

import type { CloudEvent } from "@google-cloud/functions-framework";

type StorageObjectData = {
  bucket: string;
  name: string;
  contentType?: string;
  size?: string;
};

export async function onPhotoFinalize(event: CloudEvent<StorageObjectData>): Promise<void> {
  const data = event.data;
  if (!data) return;
  const key = data.name;
  const contentType = data.contentType ?? "unknown";
  console.log(`[thumbnail] finalized ${data.bucket}/${key} (${contentType})`);

  // TODO (L5 Exercises 2-4): download, resize with sharp, upload thumb, call markReady.
  // The exercises walk the full build using Claude Code.
}
