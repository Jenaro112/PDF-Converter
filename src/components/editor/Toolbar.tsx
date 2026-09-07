'use client';

import { useState, useEffect, useCallback } from 'react';
import { useEditorStore } from '@/store/editor-store';
import type { FormatType } from '@/store/editor-store';
import {
  Menu, FolderOpen, Save,
  Bold, Italic, Highlighter, Strikethrough, Code, Sigma,
  Table, Pi, Workflow, Code2,
  Settings, Download, Loader2,
} from 'lucide-react';
import { ExportService } from '@/lib/services/ExportService';

function Divider() {
  return <div className="w-px h-5 bg-[var(--border)] mx-1.5 shrink-0" />;
}

function TBtn({
  onClick, title, active, children,
}: {
  onClick: () => void;
  title: string;
  active?: boolean;
  children: React.ReactNode;
}) {
  return (
    <button
      onClick={onClick}
      title={title}
      className={`p-2 rounded transition-colors shrink-0 ${
        active
          ? 'bg-[var(--accent)]/15 text-[var(--accent)]'
          : 'hover:bg-[var(--bg-preview)] text-[var(--text-main)]'
      }`}
    >
      {children}
    </button>
  );
}

export function Toolbar() {
  const {
    toggleSidebar,
    toggleSettings,
    documentText,
    fileName,
    activeTheme,
    coverConfig,
    isDirty,
    setSnippetToInsert,
    setFormatAction,
    markSaved,
  } = useEditorStore();

  const [isExporting, setIsExporting] = useState(false);
  const [savedFlash, setSavedFlash]   = useState(false);

  const saveNow = useCallback(async () => {
    try {
      await fetch('/api/autosave', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fileName, documentText, activeTheme, coverConfig }),
      });
      markSaved();
      setSavedFlash(true);
      setTimeout(() => setSavedFlash(false), 1500);
    } catch (err) {
      console.error('Error guardando:', err);
    }
  }, [documentText, activeTheme, coverConfig, markSaved]);

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        saveNow();
      }
    };
    document.addEventListener('keydown', down);
    return () => document.removeEventListener('keydown', down);
  }, [saveNow]);

  const handleExport = async () => {
    try {
      setIsExporting(true);
      await ExportService.exportToPDF({ documentText, activeTheme, coverConfig });
    } catch {
      alert('Hubo un problema exportando el PDF.');
    } finally {
      setIsExporting(false);
    }
  };

  const fmt = (type: FormatType) => setFormatAction(type);

  const block = (type: 'table' | 'math' | 'mermaid' | 'code') => {
    const snippets = {
      table:   '\n| Columna 1 | Columna 2 | Columna 3 |\n| :--- | :---: | ---: |\n| Texto | Centrado | Derecha |\n',
      math:    '\n$$\nE = mc^2\n$$\n',
      mermaid: '\n```mermaid\ngraph TD\n    A[Inicio] --> B{Decisión}\n    B -- Sí --> C[Opción 1]\n    B -- No --> D[Opción 2]\n```\n',
      code:    '\n```javascript\n// Tu código aquí\n\n```\n',
    };
    setSnippetToInsert(snippets[type]);
  };

  return (
    <div className="h-14 flex items-center px-4 bg-[var(--toolbar-bg)] border-b border-[var(--border)] z-20 relative">

      {/* Logo — izquierda */}
      <div className="flex items-center gap-2 mr-3 shrink-0">
        <div className="w-6 h-6 rounded bg-[var(--accent)] text-white flex items-center justify-center font-serif font-bold text-sm">
          P
        </div>
        <span className="font-semibold text-[15px] tracking-wide text-[var(--text-main)]">
          PDF Converter
        </span>
      </div>

      {/* Spacer — empuja todo lo siguiente a la derecha */}
      <div className="flex-1" />

      {/* Archivo */}
      <TBtn onClick={toggleSidebar} title="Abrir archivo (docs/)">
        <FolderOpen size={18} strokeWidth={1.75} />
      </TBtn>

      <TBtn onClick={saveNow} title="Guardar (Ctrl+S)" active={savedFlash}>
        <Save
          size={18}
          strokeWidth={savedFlash ? 2.5 : 1.75}
          className={isDirty && !savedFlash ? 'text-[var(--accent)]' : ''}
        />
      </TBtn>

      <Divider />

      {/* Formato inline */}
      <TBtn onClick={() => fmt('bold')}          title="Negrita"><Bold          size={18} strokeWidth={2.5}  /></TBtn>
      <TBtn onClick={() => fmt('italic')}        title="Cursiva"><Italic        size={18} strokeWidth={2}    /></TBtn>
      <TBtn onClick={() => fmt('highlight')}     title="Resaltado"><Highlighter size={18} strokeWidth={1.75} /></TBtn>
      <TBtn onClick={() => fmt('strikethrough')} title="Tachado"><Strikethrough size={18} strokeWidth={1.75} /></TBtn>
      <TBtn onClick={() => fmt('code-inline')}   title="Código inline"><Code   size={18} strokeWidth={1.75} /></TBtn>
      <TBtn onClick={() => fmt('latex-inline')}  title="LaTeX inline"><Sigma   size={18} strokeWidth={1.75} /></TBtn>

      <Divider />

      {/* Bloques */}
      <TBtn onClick={() => block('table')}   title="Insertar tabla"><Table    size={18} strokeWidth={1.75} /></TBtn>
      <TBtn onClick={() => block('math')}    title="Insertar ecuación $$"><Pi size={18} strokeWidth={1.75} /></TBtn>
      <TBtn onClick={() => block('code')}    title="Insertar bloque de código"><Code2    size={18} strokeWidth={1.75} /></TBtn>
      <TBtn onClick={() => block('mermaid')} title="Insertar diagrama Mermaid"><Workflow size={18} strokeWidth={1.75} /></TBtn>

      <Divider />

      {/* Configuración + Exportar */}
      <TBtn onClick={toggleSettings} title="Configuración">
        <Settings size={18} strokeWidth={1.75} />
      </TBtn>

      <button
        onClick={handleExport}
        disabled={isExporting}
        className="flex items-center gap-2 px-4 py-2 rounded-md bg-[var(--accent)] text-white hover:opacity-90 disabled:opacity-50 transition-all text-sm font-medium shadow-sm shrink-0 ml-2"
      >
        {isExporting ? <Loader2 size={16} className="animate-spin" /> : <Download size={16} strokeWidth={2} />}
        {isExporting ? 'Exportando...' : 'Exportar'}
      </button>

    </div>
  );
}
