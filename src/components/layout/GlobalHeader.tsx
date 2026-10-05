'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { useEditorStore } from '@/store/editor-store';
import {
  Save, Settings, Download, Loader2, FolderOpen, Home, Check
} from 'lucide-react';
import { ExportService } from '@/lib/services/ExportService';
import { MagneticButton } from '@/components/ui/MagneticButton';
import { ThemeToggle } from '@/components/ThemeToggle';

export function GlobalHeader() {
  const {
    documentText,
    fileName,
    setFileName,
    activeTheme,
    coverConfig,
    isDirty,
    markSaved,
    toggleSettings,
    toggleSidebar,
    viewMode,
    setViewMode,
  } = useEditorStore();

  const [isExporting, setIsExporting] = useState(false);
  const [savedFlash, setSavedFlash]   = useState(false);
  const [isRenaming, setIsRenaming]   = useState(false);
  const [renameValue, setRenameValue] = useState('');
  const renameInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isRenaming && renameInputRef.current) {
      renameInputRef.current.select();
    }
  }, [isRenaming]);

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
  }, [documentText, activeTheme, coverConfig, markSaved, fileName]);

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
      await ExportService.exportToPDF({ documentText, activeTheme, coverConfig, fileName });
    } catch {
      alert('Hubo un problema exportando el PDF.');
    } finally {
      setIsExporting(false);
    }
  };

  const commitRename = async () => {
    if (!fileName) return;
    const trimmed = renameValue.trim();
    if (!trimmed || trimmed === fileName.replace(/\.md$/, '')) {
      setIsRenaming(false);
      return;
    }
    try {
      const res = await fetch('/api/docs/rename', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ oldName: fileName, newName: trimmed }),
      });
      
      if (res.status === 404) {
        // File doesn't exist on disk yet (unsaved blank document). Just rename locally.
        setFileName(trimmed);
        setIsRenaming(false);
        return;
      }

      const data = await res.json();
      if (data.success) {
        setFileName(data.name);
      }
    } catch {
      alert('No se pudo renombrar el archivo.');
    } finally {
      setIsRenaming(false);
    }
  };

  return (
    <div className="h-14 flex items-center px-4 bg-[var(--toolbar-bg)] backdrop-blur-xl border-b border-[var(--border)] z-20 shrink-0">
      
      {/* Home / Logo */}
      <div className="flex items-center gap-2 mr-6 shrink-0">
        <button 
          onClick={() => setViewMode('dashboard')}
          className="w-8 h-8 rounded-md bg-gradient-to-br from-[var(--accent)] to-[var(--accent-hover)] text-white flex items-center justify-center font-serif font-bold text-sm shadow-inner hover:scale-105 transition-transform"
          title="Volver a Inicio"
        >
          <Home size={16} />
        </button>
        <span className="font-semibold text-sm tracking-tight text-[var(--text-main)] hidden sm:block">
          PDF Converter
        </span>
      </div>

      {/* Inline Document Rename */}
      <div className="flex-1 flex items-center">
        {viewMode === 'editor' && fileName && (
          <div className="relative flex items-center max-w-sm">
            {isRenaming ? (
              <div className="flex items-center bg-[var(--bg-surface)] border border-blue-400 rounded-md shadow-sm overflow-hidden px-2 py-1">
                <input 
                  ref={renameInputRef}
                  value={renameValue}
                  onChange={(e) => setRenameValue(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') commitRename();
                    if (e.key === 'Escape') setIsRenaming(false);
                  }}
                  onBlur={commitRename}
                  className="bg-transparent text-sm text-[var(--text-main)] outline-none w-48 font-medium"
                />
              </div>
            ) : (
              <button 
                onClick={() => {
                  setRenameValue(fileName.replace(/\.md$/, ''));
                  setIsRenaming(true);
                }}
                className="text-sm font-medium text-[var(--text-main)] hover:bg-[var(--bg-sidebar)] px-2 py-1 rounded-md transition-colors truncate max-w-[200px]"
                title="Renombrar documento"
              >
                {fileName.replace(/\.md$/, '')}
              </button>
            )}
          </div>
        )}
      </div>

      {/* File & Save Buttons */}
      <div className="flex items-center gap-1 mr-4">
        {viewMode === 'editor' && (
          <>
            <MagneticButton onClick={toggleSidebar} title="Explorador de archivos">
              <FolderOpen size={18} strokeWidth={2} />
            </MagneticButton>
            <MagneticButton onClick={saveNow} title="Guardar (Ctrl+S)" active={savedFlash}>
              <Save
                size={18}
                strokeWidth={savedFlash ? 2.5 : 2}
                className={isDirty && !savedFlash ? 'text-[var(--accent)]' : ''}
              />
            </MagneticButton>
          </>
        )}
      </div>

      <div className="w-px h-5 bg-[var(--border)] mr-4" />

      {/* Settings & Export */}
      <div className="flex items-center gap-3">
        <ThemeToggle />

        {viewMode === 'editor' && (
          <MagneticButton onClick={toggleSettings} title="Configuración de Portada">
            <Settings size={18} strokeWidth={2} />
          </MagneticButton>
        )}

        <button
          onClick={viewMode === 'editor' ? handleExport : () => setViewMode('editor')}
          disabled={isExporting || (!fileName && viewMode === 'editor')}
          className="group relative flex items-center gap-2 px-4 py-1.5 rounded-md bg-[var(--accent)] text-white hover:bg-[var(--accent-hover)] disabled:opacity-50 transition-all text-xs font-medium shadow-sm overflow-hidden shrink-0"
        >
          <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300 ease-out" />
          {isExporting ? <Loader2 size={14} className="animate-spin relative z-10" /> : (viewMode === 'editor' ? <Download size={14} strokeWidth={2.5} className="relative z-10" /> : null)}
          <span className="relative z-10">{isExporting ? 'Exportando...' : (viewMode === 'editor' ? 'Exportar' : 'Volver al Editor')}</span>
        </button>
      </div>
    </div>
  );
}
