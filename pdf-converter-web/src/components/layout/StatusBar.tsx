'use client';

import React from 'react';
import { useEditorStore } from '@/store/editor-store';
import { THEMES, THEME_CHOICES, type ThemeKey } from '@/lib/themes';
import '@/styles/statusbar.css';

export function StatusBar() {
  const markdown = useEditorStore((s) => s.markdown);
  const theme = useEditorStore((s) => s.theme);
  const fileName = useEditorStore((s) => s.fileName);

  const themeInfo = THEME_CHOICES.find((t) => t.key === theme);
  const wordCount = markdown.trim() === '' ? 0 : markdown.trim().split(/\s+/).length;
  const charCount = markdown.length;
  const lineCount = markdown.split('\n').length;

  return (
    <div className="status-bar">
      <div className="status-left">
        <span className="status-item file-indicator">📄 {fileName}</span>
      </div>
      <div className="status-right">
        <span className="status-item">Ln {lineCount}</span>
        <span className="status-item">{wordCount} palabras</span>
        <span className="status-item">{charCount} caracteres</span>
        <span className="status-item theme-indicator">
          {themeInfo?.emoji} {themeInfo?.label || theme}
        </span>
      </div>
    </div>
  );
}
