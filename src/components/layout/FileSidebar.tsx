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
  const { isSidebarOpen, fileName, setText, setFileName, loadContent, activeTheme, coverConfig, setCover, setTheme } = useEditorStore();

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
    const onFocus = () => fetchDocs();
    window.addEventListener('focus', onFocus);
    return () => window.removeEventListener('focus', onFocus);
  }, [isSidebarOpen, fetchDocs]);

  useEffect(() => {
    if (creatingNew && newInputRef.current) {
      newInputRef.current.focus();
    }
  }, [creatingNew]);

  useEffect(() => {
    if (renamingFile && renameInputRef.current) {
      renameInputRef.current.select();
    }
  }, [renamingFile]);

  const loadDoc = async (name: string) => {
    if (!name || fileName === name) return;
    try {
      const safeName = name.endsWith('.md') ? name : `${name}.md`;
      const res  = await fetch(`/api/docs/load?file=${encodeURIComponent(safeName)}`);
      if (!res.ok) {
        alert('Error cargando documento');
        return;
      }
      const data = await res.json();
      if (data.content !== undefined) {
        loadContent(data.content, safeName);
        if (data.frontmatter?.coverConfig) {
          setCover(data.frontmatter.coverConfig);
        }
        if (data.frontmatter?.activeTheme) {
          setTheme(data.frontmatter.activeTheme);
        }
      }
    } catch {
      alert('Error cargando documento');
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
    <div className="h-full flex flex-col bg-white border-none overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-5 py-4 shrink-0 border-b border-[#E5E5E5] bg-white">
        <div className="flex items-center gap-2">
          <FolderOpen size={16} className="text-[#4F46E5]" />
          <span className="text-xs font-bold text-[#A3A3A3] uppercase tracking-wider" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
            Explorador
          </span>
        </div>
      </div>

      {/* New file button */}
      <div className="px-4 pt-4 pb-2 shrink-0">
        {creatingNew ? (
          <div className="flex items-center gap-2 px-3 py-2 rounded-xl bg-white border-2 border-[#4F46E5] shadow-sm">
            <File size={14} className="text-[#4F46E5] shrink-0" />
            <input
              ref={newInputRef}
              value={newFileName}
              onChange={(e) => setNewFileName(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') commitNewFile();
                if (e.key === 'Escape') { setCreatingNew(false); setNewFileName(''); }
              }}
              placeholder="nombre-archivo"
              className="flex-1 bg-transparent text-sm text-[#171717] outline-none placeholder:text-[#A3A3A3]"
              autoFocus
            />
            <button onClick={commitNewFile} className="text-[#4F46E5] hover:opacity-70">
              <Check size={14} />
            </button>
            <button onClick={() => { setCreatingNew(false); setNewFileName(''); }} className="text-[#A3A3A3] hover:opacity-70">
              <X size={14} />
            </button>
          </div>
        ) : (
          <button
            onClick={() => { setCreatingNew(true); setNewFileName(''); }}
            className="w-full flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm text-[#4F46E5] font-medium bg-[#EEF2FF] hover:bg-[#4F46E5] hover:text-white hover:shadow-md transition-all duration-300"
          >
            <FilePlus size={16} />
            Nuevo Documento
          </button>
        )}
      </div>

      {/* File list */}
      <div className="flex-1 overflow-y-auto py-2">
        {loading ? (
          <div className="flex items-center justify-center gap-2 py-10 text-[#A3A3A3]">
            <Loader2 size={16} className="animate-spin" />
            <span className="text-sm font-medium">Cargando...</span>
          </div>
        ) : docs.length === 0 ? (
          <div className="px-5 py-10 text-center text-[#A3A3A3] text-sm font-medium">
            No hay archivos.
          </div>
        ) : (
          <div className="px-3 space-y-1">
            {docs.map((doc) => (
              <div
                key={doc.name}
                className={`group flex items-center gap-3 px-3 py-3 rounded-xl transition-all duration-200 cursor-pointer border border-transparent ${
                  fileName === doc.name
                    ? 'bg-[#F3F4F6] shadow-sm'
                    : 'hover:bg-[#FAFAFA]'
                }`}
              >
                {renamingFile === doc.name ? (
                  /* Inline rename */
                  <div className="flex items-center gap-2 flex-1 min-w-0">
                    <File size={14} className="text-[#4F46E5] shrink-0" />
                    <input
                      ref={renameInputRef}
                      value={renameValue}
                      onChange={(e) => setRenameValue(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter') commitRename(doc.name);
                        if (e.key === 'Escape') setRenamingFile(null);
                      }}
                      onBlur={() => commitRename(doc.name)}
                      className="flex-1 bg-transparent text-sm text-[#171717] font-medium outline-none border-b-2 border-[#4F46E5] pb-0.5 min-w-0"
                      onClick={(e) => e.stopPropagation()}
                    />
                    <button
                      onClick={(e) => { e.stopPropagation(); commitRename(doc.name); }}
                      className="text-[#4F46E5] hover:opacity-70 shrink-0"
                    >
                      <Check size={14} />
                    </button>
                    <button
                      onClick={(e) => { e.stopPropagation(); setRenamingFile(null); }}
                      className="text-[#A3A3A3] hover:opacity-70 shrink-0"
                    >
                      <X size={14} />
                    </button>
                  </div>
                ) : (
                  /* Normal row */
                  <>
                    <div className="flex items-start gap-3 flex-1 min-w-0" onClick={() => loadDoc(doc.name)}>
                      <File
                        size={16}
                        className={`mt-0.5 shrink-0 transition-colors ${fileName === doc.name ? 'text-[#4F46E5]' : 'text-[#A3A3A3] group-hover:text-[#4F46E5]'}`}
                      />
                      <div className="min-w-0 flex-1">
                        <div className={`text-sm font-semibold truncate ${fileName === doc.name ? 'text-[#111827]' : 'text-[#4B5563]'}`}>
                          {doc.name.replace(/\.md$/, '')}
                        </div>
                        <div className="flex items-center gap-1 text-[11px] text-[#A3A3A3] font-medium mt-0.5">
                          <span>{formatDate(doc.modified)}</span>
                        </div>
                      </div>
                    </div>

                    {/* Rename button - visible on hover */}
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        setRenamingFile(doc.name);
                        setRenameValue(doc.name.replace(/\.md$/, ''));
                      }}
                      className="shrink-0 p-1.5 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity text-[#A3A3A3] hover:text-[#4F46E5] hover:bg-[#EEF2FF]"
                      title="Renombrar"
                    >
                      <Pencil size={14} />
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
