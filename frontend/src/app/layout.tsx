import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import { Sidebar } from "@/components/layout/Sidebar";
import { ThemeToggle } from "@/components/layout/ThemeToggle";
import { SearchModal } from "@/components/layout/SearchModal";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: "Secpol AI Compliance OS",
  description: "AI Governance and Compliance Mapping",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased flex h-screen overflow-hidden`}
      >
        <Sidebar />
        <div className="flex-1 flex flex-col h-screen overflow-hidden relative">
          <header className="h-16 flex items-center justify-between px-8 border-b border-slate-200 dark:border-slate-800 bg-surface-light dark:bg-surface-dark">
            <div className="flex items-center text-sm text-slate-500">
              <span className="font-mono bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded text-xs">Press ⌘K to search</span>
            </div>
            <div className="flex items-center gap-4">
              <ThemeToggle />
            </div>
          </header>
          <main className="flex-1 overflow-auto p-8 bg-background-light dark:bg-background-dark">
            {children}
          </main>
        </div>
        <SearchModal />
      </body>
    </html>
  );
}
