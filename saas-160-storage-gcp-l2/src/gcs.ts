// GCS wrapper — hides the Storage SDK behind a tiny four-method surface the
// rest of the API uses. V4 signed URLs (Google's current signature version);
// see https://cloud.google.com/storage/docs/access-control/signed-urls.
import { Storage } from "@google-cloud/storage";
import { appConfig } from "./config.js";

const storage = new Storage({
  projectId: appConfig.gcs.projectId || undefined,
});

function bucket() {
  if (!appConfig.gcs.bucket) {
    throw new Error("GCS_BUCKET not set — see .env.example");
  }
  return storage.bucket(appConfig.gcs.bucket);
}

export const gcs = {
  async upload(buffer: Buffer, key: string, contentType: string): Promise<string> {
    await bucket().file(key).save(buffer, { contentType });
    return `https://storage.googleapis.com/${appConfig.gcs.bucket}/${key}`;
  },

  async getSignedPutUrl(key: string, contentType: string, expiresSec = 900): Promise<string> {
    const [url] = await bucket().file(key).getSignedUrl({
      action: "write",
      version: "v4",
      expires: Date.now() + expiresSec * 1000,
      contentType,
    });
    return url;
  },

  async getSignedGetUrl(key: string, expiresSec = 300): Promise<string> {
    const [url] = await bucket().file(key).getSignedUrl({
      action: "read",
      version: "v4",
      expires: Date.now() + expiresSec * 1000,
    });
    return url;
  },

  async setPublicRead(key: string): Promise<void> {
    await bucket().file(key).makePublic();
  },

  publicUrl(key: string): string {
    return `https://storage.googleapis.com/${appConfig.gcs.bucket}/${key}`;
  },
};
