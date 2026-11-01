// Presigned URL helpers — end-state of Lesson 3.
import { storage } from "./storage.js";

export async function issuePutUrl(key: string, contentType: string): Promise<string> {
  return storage.getSignedPutUrl(key, contentType, 900);
}

export async function issueGetUrl(key: string): Promise<string> {
  return storage.getSignedGetUrl(key, 300);
}
