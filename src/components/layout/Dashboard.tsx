'use client';

import { useEffect, useState, useCallback } from 'react';
import { useEditorStore } from '@/store/editor-store';
import { FileText, Plus, Clock, File, Search, Pencil, Trash2 } from 'lucide-react';
import { motion } from 'framer-motion';

interface DocFile {
  name: string;
  size: number;
  modified: string;
}

export function Dashboard() {
  const { loadBlankContent, loadContent, activeTheme, coverConfig } = useEditorStore();
  const [docs, setDocs] = useState<DocFile[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  const fetchDocs = useCallback(async () => {
    try {
      const res = await fetch('/api/docs');
      const data = await res.json();
      setDocs(data.files ?? []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDocs();
  }, [fetchDocs]);

  const createBlank = () => {
    const name = `Documento-${Math.floor(Math.random() * 10000)}`;
    loadBlankContent(name);
  };

  const openDoc = async (name: string) => {
    try {
      const res = await fetch(`/api/docs/load?file=${encodeURIComponent(name)}`);
      const data = await res.json();
      if (data.content !== undefined) {
        loadContent(data.content, name);
      }
    } catch {
      alert('Error al cargar documento');
    }
  };

  const renameDoc = async (oldName: string) => {
    const newName = window.prompt('Nuevo nombre para el documento:', oldName.replace(/\.md$/, ''));
    if (!newName || newName.trim() === '' || newName === oldName.replace(/\.md$/, '')) return;

    try {
      const res = await fetch('/api/docs/rename', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ oldName, newName: newName.trim() }),
      });
      if (res.ok) {
        fetchDocs();
      } else {
        alert('No se pudo renombrar el documento.');
      }
    } catch {
      alert('Error al renombrar.');
    }
  };

  const deleteDoc = async (name: string) => {
    if (!window.confirm(`¿Estás seguro de que quieres eliminar "${name}"?`)) return;

    try {
      const res = await fetch('/api/docs/delete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fileName: name }),
      });
      if (res.ok) {
        fetchDocs();
      } else {
        alert('No se pudo eliminar el documento.');
      }
    } catch {
      alert('Error al eliminar.');
    }
  };

  const filteredDocs = docs.filter(d => d.name.toLowerCase().includes(search.toLowerCase()));

  return (
    <div className="w-full h-full bg-[var(--bg-base)] overflow-y-auto flex flex-col font-sans">
      {/* Top Banner */}
      <div className="w-full h-[35vh] min-h-[300px] relative bg-gradient-to-br from-gray-900 to-gray-800 flex flex-col items-center justify-center p-8 overflow-hidden shrink-0">
        <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10" />
        <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-t from-gray-900/80 to-transparent" />
        
        <div className="relative z-10 w-full max-w-5xl flex flex-col gap-6 mt-10">
          <h1 className="text-4xl md:text-5xl font-bold text-white tracking-tight">
            ¿Qué vas a crear hoy?
          </h1>
          <div className="relative w-full max-w-2xl">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
            <input 
              type="text" 
              placeholder="Buscar documentos..." 
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-white/10 backdrop-blur-md border border-white/20 text-white placeholder:text-gray-400 rounded-2xl py-4 pl-12 pr-6 outline-none focus:bg-white/20 transition-all shadow-xl"
            />
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="flex-1 w-full max-w-7xl mx-auto px-6 md:px-12 py-12 flex flex-col gap-10">
        
        <div>
          <h2 className="text-lg font-semibold text-[var(--text-main)] mb-6 flex items-center gap-2">
            <Plus size={18} className="text-blue-500" />
            Crear Nuevo
          </h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
            <button 
              onClick={createBlank}
              className="group aspect-[3/4] bg-[var(--bg-surface)] border border-[var(--border)] rounded-xl shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 flex flex-col items-center justify-center gap-4 cursor-pointer"
            >
              <div className="w-16 h-16 rounded-full bg-blue-50 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                <Plus size={28} className="text-blue-500" />
              </div>
              <span className="font-medium text-[var(--text-main)]">Documento en Blanco</span>
            </button>
          </div>
        </div>

        <div>
          <h2 className="text-lg font-semibold text-[var(--text-main)] mb-6 flex items-center gap-2">
            <Clock size={18} className="text-[var(--text-muted)]" />
            Documentos Recientes
          </h2>
          
          {loading ? (
            <div className="w-full flex justify-center py-20">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500" />
            </div>
          ) : filteredDocs.length === 0 ? (
            <div className="text-center py-20 text-gray-400">
              {search ? "No se encontraron documentos." : "No tienes documentos recientes."}
            </div>
          ) : (
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
              {filteredDocs.map((doc, i) => (
                <motion.div 
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.05 }}
                  key={doc.name}
                  className="group flex flex-col text-left aspect-[3/4] bg-[var(--bg-surface)] border border-[var(--border)] rounded-xl shadow-sm hover:shadow-lg hover:border-blue-200 hover:-translate-y-1 transition-all duration-300 overflow-hidden relative cursor-pointer"
                  onClick={() => openDoc(doc.name)}
                >
                  <div className="flex-1 bg-gray-50 p-6 flex flex-col items-center justify-center border-b border-[var(--border)] relative overflow-hidden">
                    <FileText size={48} className="text-gray-300 group-hover:text-blue-200 transition-colors" strokeWidth={1.5} />
                    {/* Simulated document lines */}
                    <div className="absolute bottom-6 left-1/2 -translate-x-1/2 w-16 h-1 bg-gray-200 rounded-full" />
                    <div className="absolute bottom-4 left-1/2 -translate-x-1/2 w-12 h-1 bg-gray-200 rounded-full" />
                    
                    {/* Actions overlay */}
                    <div className="absolute top-2 right-2 flex flex-col gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button 
                        onClick={(e) => { e.stopPropagation(); renameDoc(doc.name); }}
                        className="p-1.5 bg-[var(--bg-surface)] text-[var(--text-muted)] hover:text-blue-500 rounded-md shadow-sm border border-[var(--border)]"
                        title="Renombrar"
                      >
                        <Pencil size={14} />
                      </button>
                      <button 
                        onClick={(e) => { e.stopPropagation(); deleteDoc(doc.name); }}
                        className="p-1.5 bg-[var(--bg-surface)] text-[var(--text-muted)] hover:text-red-500 rounded-md shadow-sm border border-[var(--border)]"
                        title="Eliminar"
                      >
                        <Trash2 size={14} />
                      </button>
                    </div>
                  </div>
                  <div className="p-4 bg-[var(--bg-surface)] flex flex-col">
                    <span className="font-medium text-[var(--text-main)] truncate" title={doc.name}>
                      {doc.name.replace(/\.md$/, '')}
                    </span>
                    <span className="text-xs text-[var(--text-muted)] mt-1 flex items-center gap-1">
                      <Clock size={10} />
                      {new Date(doc.modified).toLocaleDateString()}
                    </span>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
