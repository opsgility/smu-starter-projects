import type { Request, Response, NextFunction, RequestHandler } from "express";
import { createRemoteJWKSet, jwtVerify, type JWTPayload } from "jose";
import { callerContext } from "../server.js";

export interface BearerTokenOptions {
  jwksUri: string;
  issuer: string;
  audience: string;
}

/**
 * Express middleware that validates an inbound `Authorization: Bearer <jwt>`
 * header against the configured JWKS, issuer, and audience. On success, it
 * runs the rest of the request inside callerContext.run(...) so any tool
 * handler in this process can call getCallerContext() to retrieve the caller's
 * identity, scopes, and the original bearer token (used for forwarding to
 * upstream APIs on the user's behalf).
 *
 * Failures return 401 with a WWW-Authenticate hint pointing back at the
 * .well-known/oauth-protected-resource document.
 */
export function bearerTokenMiddleware(opts: BearerTokenOptions): RequestHandler {
  const jwks = createRemoteJWKSet(new URL(opts.jwksUri));

  return async function (req: Request, res: Response, next: NextFunction) {
    const header = req.headers.authorization;
    if (!header || !header.startsWith("Bearer ")) {
      res.setHeader(
        "WWW-Authenticate",
        `Bearer realm="mcp", resource_metadata="/.well-known/oauth-protected-resource"`,
      );
      res.status(401).json({ error: "missing or malformed Authorization header" });
      return;
    }

    const token = header.slice("Bearer ".length).trim();

    let payload: JWTPayload;
    try {
      const verified = await jwtVerify(token, jwks, {
        issuer: opts.issuer,
        audience: opts.audience,
      });
      payload = verified.payload;
    } catch (err) {
      console.error("bearerToken: verification failed:", (err as Error).message);
      res.setHeader("WWW-Authenticate", `Bearer error="invalid_token"`);
      res.status(401).json({ error: "invalid token" });
      return;
    }

    if (!payload.sub) {
      res.status(401).json({ error: "token missing sub claim" });
      return;
    }

    const scopeClaim = (payload.scope as string | undefined) ?? "";
    const scopes = scopeClaim.split(/\s+/).filter(Boolean);
    const tenantId = (payload.tenant_id as string | undefined) ?? undefined;

    callerContext.run(
      {
        sub: payload.sub,
        tenantId,
        scopes,
        bearerToken: token,
      },
      () => next(),
    );
  };
}
