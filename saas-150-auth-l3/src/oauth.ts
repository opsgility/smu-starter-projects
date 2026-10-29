// GitHub OAuth2 setup using `arctic` — a small, well-maintained OAuth client
// library that handles the authorization-code dance for us.

import { GitHub } from "arctic";

if (!process.env.GITHUB_CLIENT_ID || !process.env.GITHUB_CLIENT_SECRET) {
  // Not fatal on import — Lesson 2 Exercise 1 is where the student creates the OAuth app
  // and sets these env vars. Routes that need them will throw a clearer error.
  console.warn("[warn] GITHUB_CLIENT_ID / GITHUB_CLIENT_SECRET are not set — OAuth routes will fail until they are.");
}

export const github = new GitHub(
  process.env.GITHUB_CLIENT_ID ?? "",
  process.env.GITHUB_CLIENT_SECRET ?? "",
  process.env.GITHUB_REDIRECT_URI ?? "http://localhost:3000/oauth/github/callback"
);
