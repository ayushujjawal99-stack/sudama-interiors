import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Sudama CRM",
  description: "CRM Dashboard",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="h-full">

        <div className="flex h-screen">

          {/* Sidebar */}
          <aside className="w-64 bg-black text-white p-6">
            <h2 className="text-xl font-bold mb-6">Sudama CRM</h2>

            <nav className="space-y-3">
              <a href="/" className="block hover:text-gray-300">
                Dashboard
              </a>
              <a href="/leads" className="block hover:text-gray-300">
                Leads
              </a>
            </nav>
          </aside>

          {/* Main Content */}
          <main className="flex-1 bg-gray-100 overflow-y-auto">
            {children}
          </main>

        </div>

      </body>
    </html>
  );
}