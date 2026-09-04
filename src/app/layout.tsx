import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'PDF Converter',
  description: 'Editor Markdown & Exportador PDF',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es" suppressHydrationWarning>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=Outfit:wght@400;500;600;700;800&family=IBM+Plex+Sans:wght@400;500;600;700&family=Figtree:wght@400;500;600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap"
          rel="stylesheet"
        />
        <link href="https://api.fontshare.com/v2/css?f[]=cabinet-grotesk@400,500,700,800&f[]=satoshi@400,500,700&display=swap" rel="stylesheet" />
      </head>
      <body suppressHydrationWarning>
        {children}
      </body>
    </html>
  );
}
