import type { Metadata } from "next";
import { Inter, Outfit } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-sans",
  subsets: ["latin"],
});

const outfit = Outfit({
  variable: "--font-heading",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "CareerPilot | AI Career Coach & Resume Tailoring Agent",
  description: "An intelligent, end-to-end AI career mentor that evaluates your resume, calculates your industry readiness, tracks skill gaps, constructs learning roadmaps, and builds ATS-optimized resumes.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${outfit.variable} dark antialiased`}
    >
      <body className="font-sans min-h-screen bg-[#09090b] text-[#fafafa] selection:bg-blue-500/30 selection:text-blue-200">
        {children}
      </body>
    </html>
  );
}
