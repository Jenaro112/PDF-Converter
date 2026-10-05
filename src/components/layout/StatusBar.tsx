'use client';

import { useEditorStore } from '@/store/editor-store';
import { motion, AnimatePresence } from 'framer-motion';

export function StatusBar() {
  const { isDirty, cursorLine, cursorCol, wordCount, fileName } = useEditorStore();

  return (
    <div className="h-9 flex items-center justify-between px-6 text-[11px] uppercase tracking-widest select-none bg-[var(--toolbar-bg)] border-t border-[var(--border)] text-[var(--text-muted)] font-medium">
      {/* Left side */}
      <div className="flex items-center gap-8">
        <div className="relative flex items-center" style={{ width: 100 }}>
          <AnimatePresence mode="wait">
            {isDirty ? (
              <motion.span
                key="unsaved"
                initial={{ opacity: 0, y: 5 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -5 }}
                transition={{ duration: 0.15 }}
                className="font-semibold text-[var(--accent)] absolute left-0"
              >
                ● Sin guardar
              </motion.span>
            ) : (
              <motion.span
                key="saved"
                initial={{ opacity: 0, y: 5 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -5 }}
                transition={{ duration: 0.15 }}
                className="font-semibold text-[var(--secondary)] absolute left-0"
              >
                ● Guardado
              </motion.span>
            )}
          </AnimatePresence>
        </div>
        <span>Ln {cursorLine}, Col {cursorCol}</span>
        <span>{wordCount} palabras</span>
      </div>

      {/* Right side */}
      <div className="flex items-center gap-8">
        <span>UTF-8</span>
        <span>{fileName ? 'Markdown' : 'Nuevo Documento'}</span>
      </div>
    </div>
  );
}
