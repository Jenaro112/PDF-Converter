'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { useEditorStore } from '@/store/editor-store';
import {
  Save, Settings, Download, Loader2, FolderOpen, Home
} from 'lucide-react';
import { ExportService } from '@/lib/services/ExportService';
import { MagneticButton } from '@/components/ui/MagneticButton';

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
    <div className="h-16 flex items-center px-6 bg-white/80 backdrop-blur-xl border-b border-[#E5E5E5] z-20 shrink-0">
      
      {/* Home / Logo */}
      <div className="flex items-center gap-3 mr-6 shrink-0">
        <button 
          onClick={() => setViewMode('dashboard')}
          className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#4F46E5] to-[#4338CA] text-white flex items-center justify-center shadow-md hover:shadow-lg hover:-translate-y-0.5 transition-all duration-300"
          title="Volver a Inicio"
        >
          <Home size={20} />
        </button>
        <span className="font-semibold text-lg tracking-tight text-[#171717] hidden sm:block" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
          PDF Converter
        </span>
      </div>

      {/* Inline Document Rename */}
      <div className="flex-1 flex items-center">
        {viewMode === 'editor' && fileName && (
          <div className="relative flex items-center max-w-sm">
            {isRenaming ? (
              <div className="flex items-center bg-white border-2 border-[#4F46E5] rounded-lg shadow-sm overflow-hidden px-3 py-1.5 transition-all">
                <input 
                  ref={renameInputRef}
                  value={renameValue}
                  onChange={(e) => setRenameValue(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') commitRename();
                    if (e.key === 'Escape') setIsRenaming(false);
                  }}
                  onBlur={commitRename}
                  className="bg-transparent text-sm text-[#171717] outline-none w-48 font-medium"
                />
              </div>
            ) : (
              <button 
                onClick={() => {
                  setRenameValue(fileName.replace(/\.md$/, ''));
                  setIsRenaming(true);
                }}
                className="text-sm font-medium text-[#737373] hover:text-[#171717] hover:bg-[#FAFAFA] px-3 py-1.5 rounded-lg transition-colors truncate max-w-[250px]"
                title="Renombrar documento"
              >
                {fileName.replace(/\.md$/, '')}
              </button>
            )}
          </div>
        )}
      </div>

      {/* File & Save Buttons */}
      <div className="flex items-center gap-2 mr-6">
        {viewMode === 'editor' && (
          <>
            <MagneticButton onClick={toggleSidebar} title="Explorador de archivos">
              <FolderOpen size={20} strokeWidth={2} className="text-[#737373] hover:text-[#171717] transition-colors" />
            </MagneticButton>
            <MagneticButton onClick={saveNow} title="Guardar (Ctrl+S)" active={savedFlash}>
              <Save
                size={20}
                strokeWidth={savedFlash ? 2.5 : 2}
                className={`transition-colors ${isDirty && !savedFlash ? 'text-[#4F46E5]' : 'text-[#737373] hover:text-[#171717]'}`}
              />
            </MagneticButton>
          </>
        )}
      </div>

      <div className="w-px h-6 bg-[#E5E5E5] mr-6" />

      {/* Settings & Export */}
      <div className="flex items-center gap-4">
        {viewMode === 'editor' && (
          <MagneticButton onClick={toggleSettings} title="Configuracin de Portada">
            <Settings size={20} strokeWidth={2} className="text-[#737373] hover:text-[#171717] transition-colors" />
          </MagneticButton>
        )}

        <button
          onClick={viewMode === 'editor' ? handleExport : () => setViewMode('editor')}
          disabled={isExporting || (!fileName && viewMode === 'editor')}
          className="group relative flex items-center gap-2 px-5 py-2 rounded-xl bg-[#4F46E5] text-white hover:bg-[#4338CA] hover:shadow-md hover:-translate-y-0.5 disabled:opacity-50 disabled:hover:translate-y-0 disabled:hover:shadow-none transition-all text-sm font-semibold overflow-hidden shrink-0"
        >
          <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300 ease-out" />
          {isExporting ? <Loader2 size={16} className="animate-spin relative z-10" /> : (viewMode === 'editor' ? <Download size={16} strokeWidth={2.5} className="relative z-10" /> : null)}
          <span className="relative z-10">{isExporting ? 'Exportando...' : (viewMode === 'editor' ? 'Exportar PDF' : 'Volver al Editor')}</span>
        </button>
      </div>
    </div>
  );
}
