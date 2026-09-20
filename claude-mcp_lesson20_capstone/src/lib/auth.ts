/*
 * Auth helper stub — Tracks B and C only.
 *
 * Track A (DevOps / stdio) does not need this file. You can delete it.
 *
 * For OAuth 2.1 + PKCE bearer-token validation, see the Lesson 14 starter
 * project (`claude-mcp_lesson14_oauth`). The pattern uses `jose` to verify
 * JWT `iss`, `aud`, `exp`, and signature against the authorization server's
 * JWKS, and exposes a `.well-known/oauth-protected-resource` document.
 *
 * The exports below are placeholders so other modules can import a stable
 * surface while you wire in the real implementation.
 */

// TODO: import { jwtVerify, createRemoteJWKSet } from "jose";

export interface CallerContext {
  /** JWT subject (the authenticated user). */
  sub: string;
  /** Tenant claim, if your IdP issues one. */
  tenantId?: string;
  /** Granted OAuth scopes. */
  scopes: string[];
}

/**
 * TODO: validate the inbound bearer token and return a CallerContext.
 *
 * For Tracks B and C, plug this into your Streamable HTTP middleware and
 * attach the result to AsyncLocalStorage so tool handlers can call
 * `getCallerContext()` to enforce per-user data scoping.
 */
export async function validateBearerToken(_token: string): Promise<CallerContext> {
  throw new Error("validateBearerToken not implemented — see Lesson 14 starter");
}

/**
 * TODO: read the per-request CallerContext from AsyncLocalStorage.
 */
export function getCallerContext(): CallerContext {
  throw new Error("getCallerContext not implemented — wire AsyncLocalStorage in middleware");
}
