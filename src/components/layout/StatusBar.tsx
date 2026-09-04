'use client';

import { useEditorStore } from '@/store/editor-store';

export function StatusBar() {
  const { isDirty, cursorLine, cursorCol, wordCount, fileName } = useEditorStore();

  return (
    <div className="h-8 flex items-center justify-between px-5 text-[11px] uppercase tracking-wider select-none bg-[var(--toolbar-bg)] border-t border-[var(--border)] text-[var(--text-muted)]">
      {/* Left side */}
      <div className="flex items-center gap-6">
        <span className="font-semibold" style={{ color: isDirty ? 'var(--accent)' : 'var(--secondary)' }}>
          ● {isDirty ? 'Sin guardar' : 'Guardado'}
        </span>
        <span>Ln {cursorLine}, Col {cursorCol}</span>
        <span>{wordCount} palabras</span>
      </div>

      {/* Right side */}
      <div className="flex items-center gap-6">
        <span>UTF-8</span>
        <span>{fileName ? 'Markdown' : 'Nuevo Documento'}</span>
      </div>
    </div>
  );
}
