import nodemailer from "nodemailer";

export const mailer = nodemailer.createTransport({
  host: process.env.SMTP_HOST ?? "localhost",
  port: Number(process.env.SMTP_PORT ?? 1025),
  secure: false,
});

const FROM = process.env.SMTP_FROM ?? "noreply@lumentrail.example.com";
const APP_URL = process.env.APP_URL ?? "http://localhost:3000";

export async function sendVerificationEmail(toEmail: string, token: string): Promise<void> {
  const link = `${APP_URL}/verify-email?token=${token}`;
  await mailer.sendMail({
    from: FROM,
    to: toEmail,
    subject: "Verify your Lumen Trail email",
    text: `Verify by visiting: ${link}`,
    html: `<p><a href="${link}">Verify my email</a></p>`,
  });
}

export async function sendPasswordResetEmail(toEmail: string, token: string): Promise<void> {
  const link = `${APP_URL}/password-reset?token=${token}`;
  await mailer.sendMail({
    from: FROM,
    to: toEmail,
    subject: "Reset your Lumen Trail password",
    text: `Reset by visiting: ${link}`,
    html: `<p><a href="${link}">Reset my password</a></p>`,
  });
}
