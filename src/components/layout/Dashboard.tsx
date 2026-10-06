'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { Search, Plus, Clock, FileText, Pencil, Trash2 } from 'lucide-react';
import { useEditorStore } from '@/store/editor-store';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';

gsap.registerPlugin(useGSAP);

interface DocInfo {
  name: string;
  modified: number;
  size: number;
}

export function Dashboard() {
  const { loadBlankContent, loadContent } = useEditorStore();
  const [docs, setDocs] = useState<DocInfo[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  const containerRef = useRef<HTMLDivElement>(null);
  const cardsRef = useRef<HTMLDivElement>(null);

  const fetchDocs = useCallback(async () => {
    try {
      setLoading(true);
      const res = await fetch('/api/docs/list');
      const data = await res.json();
      setDocs(data.files || []);
    } catch {
      console.error('Error fetching docs');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDocs();
  }, [fetchDocs]);

  // Intro animations
  useGSAP(() => {
    gsap.fromTo('.hero-element', 
      { opacity: 0, y: 30 },
      { opacity: 1, y: 0, stagger: 0.1, duration: 0.8, ease: 'power3.out' }
    );
  }, { scope: containerRef });

  useGSAP(() => {
    if (!loading && docs.length > 0) {
      gsap.fromTo('.doc-card',
        { opacity: 0, y: 20 },
        { opacity: 1, y: 0, stagger: 0.05, duration: 0.5, ease: 'power2.out' }
      );
    }
  }, [loading, docs.length]);

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
    if (!window.confirm(`Seguro que quieres eliminar "${name}"?`)) return;

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
    <div ref={containerRef} className="w-full h-full bg-[#FAFAFA] overflow-y-auto flex flex-col font-sans">
      {/* Fresh Premium Hero */}
      <div className="w-full relative bg-white flex flex-col items-center justify-center p-12 overflow-hidden shrink-0 border-b border-[#E5E5E5]">
        {/* Abstract shapes for a fresh vibe */}
        <div className="absolute top-[-20%] left-[-10%] w-96 h-96 bg-[#4F46E5] rounded-full mix-blend-multiply filter blur-3xl opacity-5"></div>
        <div className="absolute bottom-[-20%] right-[-10%] w-96 h-96 bg-[#3B82F6] rounded-full mix-blend-multiply filter blur-3xl opacity-5"></div>
        
        <div className="relative z-10 w-full max-w-5xl flex flex-col items-center gap-8 mt-10">
          <h1 className="hero-element text-5xl md:text-6xl font-extrabold text-[#111827] tracking-tight text-center" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
            Qu vas a crear <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#4F46E5] to-[#3B82F6]">hoy?</span>
          </h1>
          <p className="hero-element text-[#737373] text-lg text-center max-w-2xl font-medium">
            Tus documentos en un solo lugar. Empieza uno nuevo o contina donde lo dejaste.
          </p>
          <div className="hero-element relative w-full max-w-2xl group">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-[#A3A3A3] group-focus-within:text-[#4F46E5] transition-colors" size={20} />
            <input 
              type="text" 
              placeholder="Buscar documentos..." 
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-white border-2 border-[#E5E5E5] text-[#171717] placeholder:text-[#A3A3A3] rounded-2xl py-4 pl-12 pr-6 outline-none focus:border-[#4F46E5] focus:ring-4 focus:ring-[#4F46E5]/10 transition-all shadow-sm"
            />
          </div>
        </div>
      </div>

      {/* Main Content Bento Grid */}
      <div className="flex-1 w-full max-w-7xl mx-auto px-6 md:px-12 py-12 flex flex-col gap-12">
        
        {/* Actions Grid */}
        <div className="hero-element">
          <h2 className="text-xl font-bold text-[#111827] mb-6 flex items-center gap-2" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
            Acciones rpidas
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
            <button 
              onClick={createBlank}
              className="group aspect-[2/1] bg-white border border-[#E5E5E5] rounded-2xl shadow-sm hover:shadow-md hover:border-[#4F46E5] transition-all duration-300 flex flex-col items-center justify-center gap-3 cursor-pointer relative overflow-hidden"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-[#4F46E5]/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div className="w-12 h-12 rounded-xl bg-[#F3F4F6] group-hover:bg-[#EEF2FF] flex items-center justify-center transition-colors duration-300">
                <Plus size={24} className="text-[#4F46E5]" />
              </div>
              <span className="font-semibold text-[#171717]">Nuevo Documento</span>
            </button>
          </div>
        </div>

        {/* Recent Docs */}
        <div className="hero-element" ref={cardsRef}>
          <h2 className="text-xl font-bold text-[#111827] mb-6 flex items-center gap-2" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
            <Clock size={20} className="text-[#4F46E5]" />
            Recientes
          </h2>
          
          {loading ? (
            <div className="w-full flex justify-center py-20">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#4F46E5]" />
            </div>
          ) : filteredDocs.length === 0 ? (
            <div className="text-center py-20 bg-white rounded-2xl border border-[#E5E5E5] border-dashed text-[#737373]">
              {search ? "No se encontraron documentos." : "Aun no tienes documentos."}
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
              {filteredDocs.map((doc, i) => (
                <div 
                  key={doc.name}
                  className="doc-card group flex flex-col text-left aspect-[4/5] bg-white border border-[#E5E5E5] rounded-2xl shadow-sm hover:shadow-xl hover:border-[#4F46E5] hover:-translate-y-1 transition-all duration-300 overflow-hidden relative cursor-pointer"
                  onClick={() => openDoc(doc.name)}
                >
                  <div className="flex-1 bg-gradient-to-br from-[#F9FAFB] to-[#F3F4F6] p-6 flex flex-col items-center justify-center border-b border-[#E5E5E5] relative overflow-hidden">
                    <FileText size={48} className="text-[#D1D5DB] group-hover:text-[#4F46E5] group-hover:scale-110 transition-all duration-300" strokeWidth={1.5} />
                    
                    {/* Actions overlay */}
                    <div className="absolute top-3 right-3 flex flex-col gap-2 opacity-0 group-hover:opacity-100 transition-opacity translate-x-2 group-hover:translate-x-0">
                      <button 
                        onClick={(e) => { e.stopPropagation(); renameDoc(doc.name); }}
                        className="p-2 bg-white text-[#737373] hover:text-[#4F46E5] rounded-lg shadow-sm border border-[#E5E5E5]"
                        title="Renombrar"
                      >
                        <Pencil size={14} />
                      </button>
                      <button 
                        onClick={(e) => { e.stopPropagation(); deleteDoc(doc.name); }}
                        className="p-2 bg-white text-[#737373] hover:text-[#EF4444] rounded-lg shadow-sm border border-[#E5E5E5]"
                        title="Eliminar"
                      >
                        <Trash2 size={14} />
                      </button>
                    </div>
                  </div>
                  <div className="p-4 bg-white flex flex-col">
                    <span className="font-semibold text-[#171717] truncate font-outfit" title={doc.name}>
                      {doc.name.replace(/\.md$/, '')}
                    </span>
                    <span className="text-xs font-medium text-[#A3A3A3] mt-1 flex items-center gap-1">
                      <Clock size={12} />
                      {new Date(doc.modified).toLocaleDateString()}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
