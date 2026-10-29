// TOTP via `otplib` (RFC 6238) and QR codes via `qrcode`.
// On enrollment: generate a secret, build an otpauth:// URL, render it as a QR.
// On signin: compare the 6-digit code the user typed against totp.check(code, secret).

import { randomBytes } from "node:crypto";
import argon2 from "argon2";
import { authenticator } from "otplib";
import QRCode from "qrcode";

authenticator.options = { window: 1, step: 30 };

export function generateTotpSecret(): string {
  return authenticator.generateSecret();
}

export function buildOtpauthUrl(email: string, secret: string): string {
  return authenticator.keyuri(email, "Lumen Trail", secret);
}

export async function qrCodeDataUrl(otpauthUrl: string): Promise<string> {
  return QRCode.toDataURL(otpauthUrl);
}

export function verifyTotp(code: string, secret: string): boolean {
  return authenticator.check(code, secret);
}

// Backup codes: ten random 8-char groups, stored as argon2 hashes.
// Format shown to the user: "abcd-efgh". The dash isn't stored; code input is normalized.
export function generateBackupCodes(count = 10): string[] {
  const codes: string[] = [];
  for (let i = 0; i < count; i++) {
    const raw = randomBytes(4).toString("hex"); // 8 hex chars
    codes.push(`${raw.slice(0, 4)}-${raw.slice(4)}`);
  }
  return codes;
}

export async function hashBackupCode(code: string): Promise<string> {
  return argon2.hash(normalizeBackupCode(code), { type: argon2.argon2id });
}

export async function verifyBackupCode(hash: string, code: string): Promise<boolean> {
  try { return await argon2.verify(hash, normalizeBackupCode(code)); } catch { return false; }
}

function normalizeBackupCode(code: string): string {
  return code.replace(/[^a-f0-9]/gi, "").toLowerCase();
}
