'use client';

import { useEffect, useRef, useState, useCallback } from 'react';
import { useEditorStore } from '@/store/editor-store';
import {
  File, FilePlus, Clock, Check, X, Pencil, Loader2, FolderOpen,
} from 'lucide-react';

interface DocFile {
  name: string;
  size: number;
  modified: string;
}

export function FileSidebar() {
  const { isSidebarOpen, toggleSidebar, fileName, setText, setFileName, markSaved, loadContent, documentText, activeTheme, coverConfig } = useEditorStore();

  const [docs, setDocs]           = useState<DocFile[]>([]);
  const [loading, setLoading]     = useState(false);
  const [renamingFile, setRenamingFile] = useState<string | null>(null); // current name being renamed
  const [renameValue, setRenameValue]   = useState('');
  const [creatingNew, setCreatingNew]   = useState(false);
  const [newFileName, setNewFileName]   = useState('');
  const renameInputRef = useRef<HTMLInputElement>(null);
  const newInputRef    = useRef<HTMLInputElement>(null);
  const sidebarRef     = useRef<HTMLDivElement>(null);

  // Fetch files whenever sidebar opens
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

  // Focus rename input when it opens
  useEffect(() => {
    if (renamingFile && renameInputRef.current) renameInputRef.current.select();
  }, [renamingFile]);

  useEffect(() => {
    if (creatingNew && newInputRef.current) newInputRef.current.select();
  }, [creatingNew]);

  // Close on Escape or outside click
  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setRenamingFile(null);
        setCreatingNew(false);
        if (isSidebarOpen) toggleSidebar();
      }
    };
    const handleClick = (e: MouseEvent) => {
      if (sidebarRef.current && !sidebarRef.current.contains(e.target as Node)) {
        if (isSidebarOpen) toggleSidebar();
      }
    };
    document.addEventListener('keydown', handleKey);
    document.addEventListener('mousedown', handleClick);
    return () => {
      document.removeEventListener('keydown', handleKey);
      document.removeEventListener('mousedown', handleClick);
    };
  }, [isSidebarOpen, toggleSidebar]);

  // Load a file into the editor
  const loadDoc = async (name: string) => {
    try {
      const res  = await fetch(`/api/docs/load?file=${encodeURIComponent(name)}`);
      const data = await res.json();
      if (data.content !== undefined) {
        loadContent(data.content, name);
        toggleSidebar();
      }
    } catch {
      alert('No se pudo cargar el archivo.');
    }
  };

  // Rename an existing file
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

  // Create a new blank file via dedicated API
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
    <>
      {/* Backdrop */}
      <div
        className={`fixed inset-0 z-30 transition-opacity duration-300 ${
          isSidebarOpen ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'
        }`}
        style={{ background: 'rgba(30,20,15,0.18)', backdropFilter: 'blur(1px)' }}
      />

      {/* Sidebar panel */}
      <div
        ref={sidebarRef}
        className={`fixed left-0 top-0 bottom-0 z-40 flex flex-col transition-transform duration-300 ease-in-out ${
          isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
        style={{
          width: '280px',
          background: 'rgba(253, 251, 248, 0.72)',
          backdropFilter: 'blur(20px) saturate(180%)',
          WebkitBackdropFilter: 'blur(20px) saturate(180%)',
          borderRight: '1px solid rgba(230, 226, 221, 0.6)',
          boxShadow: '4px 0 32px rgba(80,50,30,0.10)',
        }}
      >
        {/* Header */}
        <div
          className="flex items-center justify-between px-5 py-4 shrink-0"
          style={{ borderBottom: '1px solid rgba(230,226,221,0.6)' }}
        >
          <div className="flex items-center gap-2">
            <FolderOpen size={16} className="text-[var(--accent)]" />
            <span className="text-xs font-bold text-[var(--text-muted)] uppercase tracking-wider">
              docs /
            </span>
          </div>
          <button
            onClick={toggleSidebar}
            className="p-1 rounded hover:bg-[var(--bg-preview)] text-[var(--text-muted)] transition-colors"
          >
            <X size={15} />
          </button>
        </div>

        {/* New file button */}
        <div className="px-4 pt-3 pb-2 shrink-0">
          {creatingNew ? (
            <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-[var(--bg-preview)] border border-[var(--accent)]/40">
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
              className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-[var(--text-muted)] hover:text-[var(--accent)] hover:bg-[var(--bg-preview)] transition-colors"
            >
              <FilePlus size={15} />
              Nuevo archivo
            </button>
          )}
        </div>

        {/* Divider */}
        <div style={{ height: '1px', background: 'rgba(230,226,221,0.5)', margin: '0 16px' }} />

        {/* File list */}
        <div className="flex-1 overflow-y-auto py-2">
          {loading ? (
            <div className="flex items-center justify-center gap-2 py-10 text-[var(--text-muted)]">
              <Loader2 size={16} className="animate-spin" />
              <span className="text-sm">Cargando...</span>
            </div>
          ) : docs.length === 0 ? (
            <div className="px-5 py-10 text-center text-[var(--text-muted)] text-sm">
              No hay archivos en docs/
            </div>
          ) : (
            docs.map((doc) => (
              <div
                key={doc.name}
                className={`group flex items-center gap-3 mx-2 px-3 py-2.5 rounded-lg transition-colors cursor-pointer ${
                  fileName === doc.name
                    ? 'bg-[var(--accent)]/10 text-[var(--accent)]'
                    : 'hover:bg-[var(--bg-preview)] text-[var(--text-main)]'
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
                        <div className="text-sm font-medium truncate">{doc.name}</div>
                        <div className="flex items-center gap-1 text-xs text-[var(--text-muted)] mt-0.5">
                          <Clock size={10} />
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
                      className="shrink-0 p-1 rounded opacity-0 group-hover:opacity-100 transition-opacity text-[var(--text-muted)] hover:text-[var(--accent)] hover:bg-[var(--accent)]/10"
                      title="Renombrar"
                    >
                      <Pencil size={12} />
                    </button>
                  </>
                )}
              </div>
            ))
          )}
        </div>

        {/* Footer hint */}
        <div
          className="px-5 py-3 shrink-0"
          style={{ borderTop: '1px solid rgba(230,226,221,0.5)' }}
        >
          <p className="text-xs text-[var(--text-muted)] text-center">
            Ctrl+S para guardar · Esc para cerrar
          </p>
        </div>
      </div>
    </>
  );
}
