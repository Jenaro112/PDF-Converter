'use client';

import { useEditorStore } from '@/store/editor-store';
import type { FormatType } from '@/store/editor-store';
import {
  Bold, Italic, Highlighter, Strikethrough, Code, Sigma,
  Table, Pi, Workflow, Code2, Scissors, Minus
} from 'lucide-react';
import { MagneticButton } from '@/components/ui/MagneticButton';

function Divider() {
  return <div className="w-px h-4 bg-[var(--border)] mx-1 shrink-0 opacity-60" />;
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
    <MagneticButton onClick={onClick} title={title} active={active}>
      {children}
    </MagneticButton>
  );
}

export function Toolbar() {
  const {
    setSnippetToInsert,
    setFormatAction,
  } = useEditorStore();

  const fmt = (type: FormatType) => setFormatAction(type);

  const block = (type: 'table' | 'math' | 'mermaid' | 'code' | 'hr' | 'pagebreak') => {
    const snippets = {
      table:   '\n| Columna 1 | Columna 2 | Columna 3 |\n| :--- | :---: | ---: |\n| Texto | Centrado | Derecha |\n',
      math:    '\n$$\nE = mc^2\n$$\n',
      mermaid: '\n```mermaid\ngraph TD\n    A[Inicio] --> B{Decisión}\n    B -- Sí --> C[Opción 1]\n    B -- No --> D[Opción 2]\n```\n',
      code:    '\n```javascript\n// Tu código aquí\n\n```\n',
      hr:      '\n\n---\n\n',
      pagebreak: '\n\n\\newpage\n\n',
    };
    setSnippetToInsert(snippets[type]);
  };

  return (
    <div className="h-12 flex items-center px-4 bg-[var(--bg-surface)] border-b border-[var(--border)] shrink-0">
      
      {/* Formato inline */}
      <div className="flex items-center gap-0.5">
        <TBtn onClick={() => fmt('bold')}          title="Negrita"><Bold          size={16} strokeWidth={2.5} /></TBtn>
        <TBtn onClick={() => fmt('italic')}        title="Cursiva"><Italic        size={16} strokeWidth={2}   /></TBtn>
        <TBtn onClick={() => fmt('highlight')}     title="Resaltado"><Highlighter size={16} strokeWidth={2}   /></TBtn>
        <TBtn onClick={() => fmt('strikethrough')} title="Tachado"><Strikethrough size={16} strokeWidth={2}   /></TBtn>
        <TBtn onClick={() => fmt('code-inline')}   title="Código inline"><Code   size={16} strokeWidth={2}   /></TBtn>
        <TBtn onClick={() => fmt('latex-inline')}  title="LaTeX inline"><Sigma   size={16} strokeWidth={2}   /></TBtn>
      </div>

      <Divider />

      {/* Bloques */}
      <div className="flex items-center gap-0.5">
        <TBtn onClick={() => block('table')}   title="Insertar tabla"><Table    size={16} strokeWidth={2} /></TBtn>
        <TBtn onClick={() => block('math')}    title="Insertar ecuación $$"><Pi size={16} strokeWidth={2} /></TBtn>
        <TBtn onClick={() => block('code')}    title="Insertar bloque de código"><Code2    size={16} strokeWidth={2} /></TBtn>
        <TBtn onClick={() => block('mermaid')} title="Insertar diagrama Mermaid"><Workflow size={16} strokeWidth={2} /></TBtn>
        <TBtn onClick={() => block('hr')}      title="Línea divisoria (---)"><Minus size={16} strokeWidth={2} /></TBtn>
        <TBtn onClick={() => block('pagebreak')} title="Salto de página (\newpage)"><Scissors size={16} strokeWidth={2} /></TBtn>
      </div>

    </div>
  );
}
