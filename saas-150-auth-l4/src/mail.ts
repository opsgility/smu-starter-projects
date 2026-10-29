// Local SMTP transport pointing at MailHog (localhost:1025 in the lab container).
// In production you'd point SMTP_HOST at Resend / SES / SendGrid.
//
// MailHog UI: open http://localhost:8025 in the lab's preview browser to see
// every email the server sent.

import nodemailer from "nodemailer";

export const mailer = nodemailer.createTransport({
  host: process.env.SMTP_HOST ?? "localhost",
  port: Number(process.env.SMTP_PORT ?? 1025),
  secure: false,
  // MailHog accepts any auth; real providers do.
});

const FROM = process.env.SMTP_FROM ?? "noreply@lumentrail.example.com";
const APP_URL = process.env.APP_URL ?? "http://localhost:3000";

export async function sendVerificationEmail(toEmail: string, token: string): Promise<void> {
  const link = `${APP_URL}/verify-email?token=${token}`;
  await mailer.sendMail({
    from: FROM,
    to: toEmail,
    subject: "Verify your Lumen Trail email",
    text: `Welcome to Lumen Trail! Verify your email by visiting:\n\n${link}\n\nThis link expires in 1 hour.`,
    html: `<p>Welcome to Lumen Trail! Verify your email by clicking the link below:</p>
<p><a href="${link}">Verify my email</a></p>
<p>This link expires in 1 hour.</p>`,
  });
}

export async function sendPasswordResetEmail(toEmail: string, token: string): Promise<void> {
  const link = `${APP_URL}/password-reset?token=${token}`;
  await mailer.sendMail({
    from: FROM,
    to: toEmail,
    subject: "Reset your Lumen Trail password",
    text: `A password reset was requested for your Lumen Trail account. Reset by visiting:\n\n${link}\n\nThis link expires in 1 hour. If you didn't request this, you can ignore this email.`,
    html: `<p>A password reset was requested. Click the link below to set a new password:</p>
<p><a href="${link}">Reset my password</a></p>
<p>This link expires in 1 hour. If you didn't request this, you can ignore this email.</p>`,
  });
}
