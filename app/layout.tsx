import type { Metadata, Viewport } from "next"
import { Inter, JetBrains_Mono } from "next/font/google"
import "./globals.css"

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
})

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains-mono",
  display: "swap",
})

export const metadata: Metadata = {
  title: "Autonomous Financial DD – Due Diligence UI",
  description:
    "An autonomous, multi-agent platform that ingests financial documents and runs end-to-end due diligence — financial analysis, market intelligence, risk assessment, and a final investment memo.",
  keywords: ["due diligence", "financial analysis", "AI agents", "investment memo", "market intelligence"],
}

export const viewport: Viewport = {
  themeColor: "#0b1120",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`dark ${inter.variable} ${jetbrainsMono.variable}`}>
      <body className="font-sans">{children}</body>
    </html>
  )
}
