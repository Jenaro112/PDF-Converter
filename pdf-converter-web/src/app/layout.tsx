import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PDF Converter — Editor Markdown a PDF de Alta Calidad",
  description:
    "Redactá, previsualizá en tiempo real y exportá documentos Markdown y DOCX a PDF de alta calidad con 6 temas profesionales, diagramas Mermaid, fórmulas KaTeX y control de paginación A4.",
  keywords: [
    "markdown",
    "pdf",
    "converter",
    "editor",
    "mermaid",
    "katex",
    "latex",
    "A4",
  ],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
