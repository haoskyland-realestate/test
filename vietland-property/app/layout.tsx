import type { Metadata } from "next";
import "./globals.css";
import Navbar from "../components/Navbar";
import MarqueeTicker from "../components/MarqueeTicker";
import Footer from "../components/Footer";
import FloatingContacts from "../components/FloatingContacts";

export const metadata: Metadata = {
  title: "Vietland — Vietnam Real Estate for Foreign Buyers",
  description:
    "Vetted, legal, multilingual property advisory for foreigners buying apartments, villas and condotels in Vietnam.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,500&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap"
          rel="stylesheet"
        />
      </head>
      <body id="top">
        <Navbar />
        <MarqueeTicker />
        <main>{children}</main>
        <Footer />
        <FloatingContacts />
      </body>
    </html>
  );
}
