'use client';

import { useEffect, useRef, useState, useCallback } from 'react';
import { useEditorStore } from '@/store/editor-store';
import {
  File, FilePlus, Clock, Check, X, Pencil, Loader2, FolderOpen,
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface DocFile {
  name: string;
  size: number;
  modified: string;
}

export function FileSidebar() {
  const { isSidebarOpen, fileName, setText, setFileName, loadContent, activeTheme, coverConfig } = useEditorStore();

  const [docs, setDocs]           = useState<DocFile[]>([]);
  const [loading, setLoading]     = useState(false);
  const [renamingFile, setRenamingFile] = useState<string | null>(null);
  const [renameValue, setRenameValue]   = useState('');
  const [creatingNew, setCreatingNew]   = useState(false);
  const [newFileName, setNewFileName]   = useState('');
  const renameInputRef = useRef<HTMLInputElement>(null);
  const newInputRef    = useRef<HTMLInputElement>(null);

  const fetchDocs = useCallback(async () => {
    setLoading(true);
    try {
      const res  = await fetch('/api/docs');
      const data = await res.json();
      setDocs(data.files ?? []);
    } catch {
      setDocs([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (isSidebarOpen) fetchDocs();
  }, [isSidebarOpen, fetchDocs]);

  useEffect(() => {
    if (!isSidebarOpen) return;
    const interval = setInterval(fetchDocs, 3000);
    return () => clearInterval(interval);
  }, [isSidebarOpen, fetchDocs]);

  useEffect(() => {
    if (renamingFile && renameInputRef.current) renameInputRef.current.select();
  }, [renamingFile]);

  useEffect(() => {
    if (creatingNew && newInputRef.current) newInputRef.current.select();
  }, [creatingNew]);

  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setRenamingFile(null);
        setCreatingNew(false);
      }
    };
    document.addEventListener('keydown', handleKey);
    return () => document.removeEventListener('keydown', handleKey);
  }, []);

  const loadDoc = async (name: string) => {
    try {
      const res  = await fetch(`/api/docs/load?file=${encodeURIComponent(name)}`);
      const data = await res.json();
      if (data.content !== undefined) {
        loadContent(data.content, name);
      }
    } catch {
      alert('No se pudo cargar el archivo.');
    }
  };

  const commitRename = async (oldName: string) => {
    const trimmed = renameValue.trim();
    if (!trimmed || trimmed === oldName.replace(/\.md$/, '')) {
      setRenamingFile(null);
      return;
    }
    try {
      const res  = await fetch('/api/docs/rename', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ oldName, newName: trimmed }),
      });
      const data = await res.json();
      if (data.success) {
        if (fileName === oldName) setFileName(data.name);
        await fetchDocs();
      }
    } catch {
      alert('No se pudo renombrar.');
    } finally {
      setRenamingFile(null);
    }
  };

  const commitNewFile = async () => {
    const trimmed = newFileName.trim();
    if (!trimmed) { setCreatingNew(false); return; }
    const initialContent = '# ' + trimmed.replace(/\.md$/, '') + '\n\n';
    try {
      const res  = await fetch('/api/docs/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          fileName: trimmed,
          content: initialContent,
          activeTheme,
          coverConfig,
        }),
      });
      const data = await res.json();
      if (data.success) {
        loadContent(initialContent, data.name);
        await fetchDocs();
      }
    } catch {
      alert('No se pudo crear el archivo.');
    } finally {
      setCreatingNew(false);
      setNewFileName('');
    }
  };

  const formatDate = (iso: string) => {
    const d = new Date(iso);
    return d.toLocaleDateString('es-AR', {
      day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit',
    });
  };

  return (
    <div className="h-full flex flex-col bg-[var(--bg-sidebar)] border-r border-[var(--border)] overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-5 py-3 shrink-0 border-b border-[var(--border)]">
        <div className="flex items-center gap-2">
          <FolderOpen size={16} className="text-[var(--accent)]" />
          <span className="text-xs font-bold text-[var(--text-muted)] uppercase tracking-wider">
            Explorador
          </span>
        </div>
      </div>

      {/* New file button */}
      <div className="px-4 pt-3 pb-2 shrink-0">
        {creatingNew ? (
          <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-[var(--bg-surface)] border border-[var(--accent)]/40 shadow-sm">
            <File size={14} className="text-[var(--accent)] shrink-0" />
            <input
              ref={newInputRef}
              value={newFileName}
              onChange={(e) => setNewFileName(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') commitNewFile();
                if (e.key === 'Escape') { setCreatingNew(false); setNewFileName(''); }
              }}
              placeholder="nombre-archivo"
              className="flex-1 bg-transparent text-sm text-[var(--text-main)] outline-none placeholder:text-[var(--text-muted)]"
              autoFocus
            />
            <button onClick={commitNewFile} className="text-[var(--accent)] hover:opacity-70">
              <Check size={14} />
            </button>
            <button onClick={() => { setCreatingNew(false); setNewFileName(''); }} className="text-[var(--text-muted)] hover:opacity-70">
              <X size={14} />
            </button>
          </div>
        ) : (
          <button
            onClick={() => { setCreatingNew(true); setNewFileName(''); }}
            className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-[var(--text-muted)] hover:text-[var(--text-main)] hover:bg-[var(--bg-surface)] hover:shadow-sm border border-transparent hover:border-[var(--border)] transition-all"
          >
            <FilePlus size={15} />
            Nuevo archivo
          </button>
        )}
      </div>

      {/* File list */}
      <div className="flex-1 overflow-y-auto py-2">
        {loading ? (
          <div className="flex items-center justify-center gap-2 py-10 text-[var(--text-muted)]">
            <Loader2 size={16} className="animate-spin" />
            <span className="text-sm">Cargando...</span>
          </div>
        ) : docs.length === 0 ? (
          <div className="px-5 py-10 text-center text-[var(--text-muted)] text-sm">
            No hay archivos.
          </div>
        ) : (
          <div className="px-2 space-y-1">
            {docs.map((doc) => (
              <div
                key={doc.name}
                className={`group flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors cursor-pointer border ${
                  fileName === doc.name
                    ? 'bg-[var(--bg-surface)] border-[var(--border)] shadow-sm'
                    : 'border-transparent hover:bg-[var(--bg-surface)] hover:border-[var(--border)]/50'
                }`}
              >
                {renamingFile === doc.name ? (
                  /* Inline rename */
                  <div className="flex items-center gap-2 flex-1 min-w-0">
                    <File size={14} className="text-[var(--accent)] shrink-0" />
                    <input
                      ref={renameInputRef}
                      value={renameValue}
                      onChange={(e) => setRenameValue(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter') commitRename(doc.name);
                        if (e.key === 'Escape') setRenamingFile(null);
                      }}
                      onBlur={() => commitRename(doc.name)}
                      className="flex-1 bg-transparent text-sm text-[var(--text-main)] outline-none border-b border-[var(--accent)]/60 pb-0.5 min-w-0"
                      onClick={(e) => e.stopPropagation()}
                    />
                    <button
                      onClick={(e) => { e.stopPropagation(); commitRename(doc.name); }}
                      className="text-[var(--accent)] hover:opacity-70 shrink-0"
                    >
                      <Check size={13} />
                    </button>
                    <button
                      onClick={(e) => { e.stopPropagation(); setRenamingFile(null); }}
                      className="text-[var(--text-muted)] hover:opacity-70 shrink-0"
                    >
                      <X size={13} />
                    </button>
                  </div>
                ) : (
                  /* Normal row */
                  <>
                    <div className="flex items-start gap-3 flex-1 min-w-0" onClick={() => loadDoc(doc.name)}>
                      <File
                        size={14}
                        className={`mt-0.5 shrink-0 ${fileName === doc.name ? 'text-[var(--accent)]' : 'text-[var(--text-muted)]'}`}
                      />
                      <div className="min-w-0 flex-1">
                        <div className={`text-sm font-medium truncate ${fileName === doc.name ? 'text-[var(--text-main)]' : 'text-[var(--text-main)]'}`}>
                          {doc.name}
                        </div>
                        <div className="flex items-center gap-1 text-[11px] text-[var(--text-muted)] mt-0.5">
                          <span>{formatDate(doc.modified)}</span>
                        </div>
                      </div>
                    </div>

                    {/* Rename button — visible on hover */}
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        setRenamingFile(doc.name);
                        setRenameValue(doc.name.replace(/\.md$/, ''));
                      }}
                      className="shrink-0 p-1.5 rounded opacity-0 group-hover:opacity-100 transition-opacity text-[var(--text-muted)] hover:text-[var(--accent)] hover:bg-[var(--accent)]/10"
                      title="Renombrar"
                    >
                      <Pencil size={12} />
                    </button>
                  </>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
