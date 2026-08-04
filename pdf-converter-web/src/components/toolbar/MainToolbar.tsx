'use client';

import React, { useRef, useState } from 'react';
import { useEditorStore } from '@/store/editor-store';
import { ThemeSelector } from './ThemeSelector';
import { CoverDialog } from './CoverDialog';
import { THEMES, type ThemeKey } from '@/lib/themes';
import { generateCoverHtml } from '@/lib/covers';
import '@/styles/toolbar.css';

export function MainToolbar() {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const fileName = useEditorStore((s) => s.fileName);
  const theme = useEditorStore((s) => s.theme);
  const coverConfig = useEditorStore((s) => s.coverConfig);
  const showCover = useEditorStore((s) => s.showCover);
  const setFileName = useEditorStore((s) => s.setFileName);
  const setMarkdown = useEditorStore((s) => s.setMarkdown);

  const [isExportingPDF, setIsExportingPDF] = useState(false);
  const [isCoverDialogOpen, setIsCoverDialogOpen] = useState(false);

  const handleFileNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFileName(e.target.value);
  };

  const handleOpenClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const nameWithoutExt = file.name.replace(/\.(md|markdown|txt)$/i, '');
    setFileName(nameWithoutExt);

    const reader = new FileReader();
    reader.onload = (event) => {
      const content = event.target?.result as string;
      setMarkdown(content);
    };
    reader.readAsText(file);
    e.target.value = '';
  };

  const handleExportPDF = async () => {
    if (isExportingPDF) return;
    setIsExportingPDF(true);

    try {
      // Get rendered content from preview page
      const previewElement = document.querySelector('.preview-container');
      const innerHtml = previewElement ? previewElement.innerHTML : '';

      // Build CSS variables for selected theme
      const t = THEMES[theme as ThemeKey] || THEMES.minimal;
      const cssVars = Object.entries(t)
        .filter(([key]) => key !== 'name' && key !== 'pygmentsStyle')
        .map(([key, value]) => `--${key.replace(/([A-Z])/g, '-$1').toLowerCase()}: ${value};`)
        .join('\n    ');

      const fullHtml = `<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <title>${fileName || 'documento'}</title>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;600&family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;0,7..72,700;1,7..72,400&family=Outfit:wght@400;600;700;800&family=Playfair+Display:wght@700;800&family=Poppins:wght@600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap" />
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" />
  <style>
    :root {
      ${cssVars}
    }
    @page { size: A4; margin: 0; }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html, body {
      width: 210mm;
      margin: 0;
      padding: 0;
      background-color: var(--page-bg) !important;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }
    .preview-container {
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .page, .preview-page {
      width: 210mm;
      min-height: 297mm;
      box-sizing: border-box;
      background-color: var(--page-bg) !important;
      padding: 20mm;
      margin: 0;
      font-family: var(--font-family-content);
      font-size: 11pt;
      line-height: 1.6;
      color: var(--text-color);
      text-align: justify;
      page-break-after: always !important;
      break-after: page !important;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }
    .preview-page h1, .preview-page h2, .preview-page h3, .preview-page h4, .preview-page h5, .preview-page h6 {
      font-family: var(--font-family-headings);
      color: var(--heading-color);
      margin-top: 0;
    }
    .preview-page h1:first-child, .preview-page h2:first-child { margin-top: 0; }
    .preview-page h1 { font-size: 20pt; font-weight: 700; margin-top: 10mm; margin-bottom: 4mm; border-bottom: var(--h1-border-width) solid var(--h1-border-color); padding-bottom: 2mm; }
    .preview-page h2 { font-size: 14pt; font-weight: 600; margin-top: 7mm; margin-bottom: 3mm; }
    .preview-page h3 { font-size: 12pt; font-weight: 600; margin-top: 5mm; margin-bottom: 2mm; font-style: italic; }
    .preview-page p { margin-bottom: 3mm; }
    .preview-page .codehilite, .preview-page .highlight, .preview-page pre {
      border-radius: 8px; padding: 10px 16px; margin: 12px 0; overflow: visible !important;
      border: 1px solid var(--code-border); font-size: 9pt; background: var(--code-bg);
    }
    .preview-page pre, .preview-page pre code {
      background: transparent !important; border: none !important; padding: 0 !important;
      font-family: 'JetBrains Mono', Consolas, 'Courier New', monospace !important;
      font-size: inherit; color: var(--code-color);
    }
    .preview-page :not(pre) > code {
      background: var(--inline-code-bg); color: var(--inline-code-color); padding: 0.2em 0.4em;
      border-radius: 6px; font-family: 'JetBrains Mono', Consolas, 'Courier New', monospace !important;
      font-size: 8.5pt; border: 1px solid var(--inline-code-border);
    }
    .preview-page blockquote {
      border-left: 4px solid var(--accent-color); padding: 8px 16px; margin: 12px 0;
      background: rgba(0, 0, 0, 0.02); border-radius: 0 8px 8px 0; font-style: italic; color: var(--muted-color);
    }
    .preview-page table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 10pt; }
    .preview-page th, .preview-page td { padding: 8px 12px; border: 1px solid var(--table-border); text-align: left; }
    .preview-page th { background-color: var(--table-header-bg) !important; color: var(--table-header-fg) !important; font-family: var(--font-family-headings); font-weight: 600; }
    .preview-page tr:nth-child(even) { background-color: var(--table-row-even-bg); }
    .preview-page ul, .preview-page ol { padding-left: 24px; margin-bottom: 12px; }
    .preview-page li { margin-bottom: 4px; }
    .preview-page img { max-width: 100%; height: auto; display: block; margin: 6mm auto; }
    .preview-page hr { border: none; border-top: 1px solid var(--accent-color); opacity: 0.3; margin: 6mm 0; }
    .preview-page .math-display, .preview-page .katex-display { text-align: center; margin: 4mm 0; overflow-x: auto; }
    .preview-page .math-inline { white-space: nowrap; }
    .preview-page strong { color: var(--heading-color); }
    .preview-page .mermaid-diagram { max-width: 100%; display: block; margin: 6mm auto; text-align: center; }
    .preview-page .mermaid-diagram svg { max-width: 100%; height: auto; display: block; margin: 0 auto; }
    .page-break, .pagebreak { page-break-after: always !important; break-after: page !important; display: block !important; height: 0 !important; margin: 0 !important; padding: 0 !important; border: none !important; }
    mark { padding: 1px 5px; border-radius: 4px; color: inherit; }

    /* Cover Page PDF styles */
    .cover-page { position: relative; display: flex; flex-direction: column; justify-content: space-between; min-height: 297mm !important; }
    .cover-inner { display: flex; flex-direction: column; justify-content: space-between; height: 100%; }
    .cover-header { display: flex; flex-direction: column; gap: 12px; }
    .cover-logo { max-height: 70px; max-width: 200px; object-fit: contain; }
    .logo-pos-left { align-self: flex-start; }
    .logo-pos-center { align-self: center; }
    .logo-pos-right { align-self: flex-end; }
    .cover-kicker { font-size: 9pt; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: var(--accent-color); }
    .cover-body { margin: auto 0; }
    .cover-title { font-family: var(--font-family-headings); font-size: 28pt; font-weight: 800; line-height: 1.25; color: var(--heading-color); border: none !important; }
    .cover-subtitle { font-size: 14pt; color: var(--muted-color); }
    .cover-footer-meta { display: flex; flex-direction: column; gap: 8px; padding-top: 20px; border-top: 2px solid var(--accent-color); }
    .cover-meta-item { display: flex; font-size: 10.5pt; }
    .meta-label { font-weight: 700; width: 120px; color: var(--heading-color); }
    .cover-style-classic { text-align: center; border: 4px double var(--accent-color); }
    .cover-style-sidebar { padding-left: 35mm !important; }
    .cover-sidebar-stripe { position: absolute; top: 0; left: 0; bottom: 0; width: 18mm; background: var(--accent-color); }
  </style>
</head>
<body>
  <div class="preview-container">
    ${innerHtml}
  </div>
</body>
</html>`;

      const response = await fetch('/api/export/pdf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          html: fullHtml,
          filename: `${fileName || 'documento'}.pdf`,
          footerText: fileName || '',
        }),
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.details || errData.error || 'Error al generar el PDF');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${fileName || 'documento'}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Export PDF error:', error);
      alert(`Error al exportar PDF: ${error instanceof Error ? error.message : String(error)}`);
    } finally {
      setIsExportingPDF(false);
    }
  };

  const handleExportDOCX = () => {
    alert('Próximamente: Exportación a Word (.docx)');
  };

  return (
    <>
      <header className="main-toolbar">
        <div className="toolbar-left">
          <div className="toolbar-brand">
            <span className="brand-badge">PDF</span>
            <span className="brand-text">Converter</span>
          </div>

          <div className="file-name-container">
            <span className="file-name-icon">✏️</span>
            <input
              type="text"
              className="file-name-input"
              value={fileName}
              onChange={handleFileNameChange}
              placeholder="Documento sin título"
            />
          </div>
        </div>

        <div className="toolbar-center">
          <button className="toolbar-btn" onClick={handleOpenClick} title="Abrir archivo Markdown">
            <span className="btn-icon">📂</span>
            <span>Abrir</span>
          </button>
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept=".md,.markdown,.txt,text/markdown,text/plain"
            style={{ display: 'none' }}
          />

          <button
            className={`toolbar-btn cover-btn ${showCover ? 'active' : ''}`}
            onClick={() => setIsCoverDialogOpen(true)}
            title="Configurar Portada / Carátula"
          >
            <span className="btn-icon">📖</span>
            <span>Portada</span>
            {showCover && <span className="active-dot" />}
          </button>

          <div className="toolbar-divider" />

          <ThemeSelector />
        </div>

        <div className="toolbar-right">
          <button
            className="export-btn btn-pdf"
            onClick={handleExportPDF}
            disabled={isExportingPDF}
            title="Exportar a PDF A4 de alta calidad"
          >
            <span className="btn-icon">{isExportingPDF ? '⏳' : '📄'}</span>
            <span>{isExportingPDF ? 'Generando...' : 'Exportar PDF'}</span>
          </button>

          <button
            className="export-btn btn-docx"
            onClick={handleExportDOCX}
            title="Exportar a Microsoft Word (.docx)"
          >
            <span className="btn-icon">📝</span>
            <span>DOCX</span>
          </button>
        </div>
      </header>

      <CoverDialog
        isOpen={isCoverDialogOpen}
        onClose={() => setIsCoverDialogOpen(false)}
      />
    </>
  );
}
