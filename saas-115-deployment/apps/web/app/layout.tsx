import type { ReactNode } from "react";

export const metadata = {
  title: "Lumen Trail — Featured Routes",
  description: "A tiny hiking-route marketplace."
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body
        style={{
          fontFamily:
            "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif",
          margin: 0,
          padding: 0,
          background: "#f7faf5",
          color: "#1b2b1b"
        }}
      >
        {children}
      </body>
    </html>
  );
}
