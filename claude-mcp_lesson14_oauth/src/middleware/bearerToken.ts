import type { Request, Response, NextFunction } from "express";

// TODO (Task 2): Implement bearer-token validation against the auth server's
// JWKS using `jose`. The four steps are:
//
//   1) Parse the Authorization header
//      - Expect `Authorization: Bearer <jwt>`.
//      - If missing or malformed, return 401 with a `WWW-Authenticate: Bearer`
//        header pointing at /.well-known/oauth-protected-resource.
//
//   2) jwtVerify with JWKS from JWKS_URL
//      - Use `createRemoteJWKSet(new URL(process.env.JWKS_URL!))` (cache the
//        JWKS at module scope so you don't refetch per request).
//      - Call `await jwtVerify(token, jwks, { ... })`.
//
//   3) Check issuer
//      - The verified payload's `iss` MUST equal process.env.EXPECTED_ISSUER.
//      - Pass `issuer` into jwtVerify so the library enforces it for you.
//
//   4) Check audience
//      - The verified payload's `aud` MUST equal process.env.EXPECTED_AUDIENCE
//        (your /mcp resource URL). This is the critical defense against token
//        replay across services. Pass `audience` into jwtVerify.
//
// On success: attach the verified claims to res.locals.auth (so tool handlers
// can read sub/scope) and call next().
//
// On failure: return 401 with a JSON body `{ error: "invalid_token", ... }`
// and the WWW-Authenticate header from step 1.

export async function requireBearerToken(
  _req: Request,
  res: Response,
  _next: NextFunction,
): Promise<void> {
  // TODO: replace this stub with the real implementation described above.
  res
    .status(501)
    .json({ error: "bearer_token_middleware_not_implemented" });
}
