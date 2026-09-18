import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Risk Lens | Credit explainability",
  description: "Transparent credit risk decisions for every borrower.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}