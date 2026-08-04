'use client';

import React, { useState, useRef, useEffect } from 'react';
import { useEditorStore } from '@/store/editor-store';
import { THEME_CHOICES, type ThemeKey } from '@/lib/themes';

export function ThemeSelector() {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const currentTheme = useEditorStore((s) => s.theme);
  const setTheme = useEditorStore((s) => s.setTheme);

  const currentChoice = THEME_CHOICES.find((t) => t.key === currentTheme) || THEME_CHOICES[0];

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSelect = (themeKey: ThemeKey) => {
    setTheme(themeKey);
    setIsOpen(false);
  };

  return (
    <div className="theme-selector" ref={dropdownRef}>
      <button
        className="toolbar-btn theme-trigger"
        onClick={() => setIsOpen(!isOpen)}
        title="Seleccionar Tema"
      >
        <span>{currentChoice.emoji}</span>
        <span>{currentChoice.label}</span>
        <span className="dropdown-arrow">{isOpen ? '▲' : '▼'}</span>
      </button>

      {isOpen && (
        <div className="theme-dropdown">
          {THEME_CHOICES.map((choice) => (
            <button
              key={choice.key}
              className={`theme-option ${currentTheme === choice.key ? 'active' : ''}`}
              onClick={() => handleSelect(choice.key as ThemeKey)}
            >
              <span className="theme-option-emoji">{choice.emoji}</span>
              <span className="theme-option-label">{choice.label}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
