import "./globals.css";
import { useEffect } from "react";
import { useSearchParams } from "next/navigation";
import { CanvasProvider } from "next/font/google";

import "lucide-react/styles.css";

// Ariba Security Platform font - Inter
const inter = await import("next/font/google");
const interFont = inter({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  display: "swap",
});

export const metadata = {
  title: "Ariba Security Platform - SOC Dashboard",
  description: "Ariba Security Platform - Endpoint Detection, Investigation, and Response",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={interFont.className}>
      <body className={interFont.className}>
        {children}
      </body>
    </html>
  );
}