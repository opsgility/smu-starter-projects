// Presigned URL helper. L3 exercises walk you through filling this in with
// Claude Code — the TODO stubs are the lesson's teaching moments.
import { storage } from "./storage.js";

/**
 * issuePutUrl — hand the browser a short-lived URL it PUTs the upload bytes to.
 * The browser bypasses the API entirely for the actual bytes transfer.
 *
 * TODO (L3 Exercise 1): direct Claude Code to replace this stub with:
 *   return storage.getSignedPutUrl(key, contentType, 900);
 * — then prerecord the trail_photos row before you hand the URL back so an
 *   abandoned upload leaves a status='pending' row the thumbnail trigger (L5)
 *   can scrub later.
 */
export async function issuePutUrl(
  key: string,
  contentType: string,
): Promise<string> {
  void key;
  void contentType;
  throw new Error("TODO — L3 Exercise 1 fills this in");
}

/**
 * issueGetUrl — return a short-lived signed GET URL. Used by the "lock the
 * bucket down to signed-only" lesson in L4.
 *
 * TODO (L4 Exercise 2): direct Claude Code to replace this stub with:
 *   return storage.getSignedGetUrl(key, 300);
 */
export async function issueGetUrl(key: string): Promise<string> {
  void key;
  throw new Error("TODO — L4 Exercise 2 fills this in");
}
