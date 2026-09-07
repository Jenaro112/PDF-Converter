'use client';

import React from 'react';
import { useEditorStore } from '@/store/editor-store';
import { useMarkdownProcessor } from '@/lib/markdown/pipeline';
import { generateRootCSS } from '@/lib/themes/document-themes';
import 'katex/dist/katex.min.css';
import { Paginator } from './Paginator';
import { ZoomIn, ZoomOut, Maximize2, Minimize2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export function Preview() {
  const { documentText, zoomLevel, setZoom, isPreviewExpanded, togglePreviewExpanded, activeTheme } = useEditorStore();
  const previewRef = React.useRef<HTMLDivElement>(null);
  
  // hook que convierte el texto en componentes React
  const content = useMarkdownProcessor(documentText);

  // Sincronización del scroll: nos suscribimos al store sin re-renderizar todo el componente
  React.useEffect(() => {
    const unsub = useEditorStore.subscribe((state, prevState) => {
      if (state.editorScrollPercent !== prevState.editorScrollPercent) {
        if (previewRef.current) {
          const maxScroll = previewRef.current.scrollHeight - previewRef.current.clientHeight;
          if (maxScroll > 0) {
            previewRef.current.scrollTop = maxScroll * state.editorScrollPercent;
          }
        }
      }
    });
    return unsub;
  }, []);

  return (
    <>
      <style dangerouslySetInnerHTML={{ __html: generateRootCSS(activeTheme) }} />
      {/* Background Overlay cuando está expandido */}
      <AnimatePresence>
        {isPreviewExpanded && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.4 }}
            className="fixed inset-0 bg-black/20 backdrop-blur-sm z-40"
            onClick={togglePreviewExpanded}
          />
        )}
      </AnimatePresence>

      <motion.div 
        ref={previewRef}
        layout
        transition={{ type: "spring", bounce: 0.15, duration: 0.6 }}
        className={`preview-container bg-[var(--bg-preview)] flex flex-col items-center overflow-auto shadow-2xl ${
          isPreviewExpanded 
            ? 'fixed inset-4 md:inset-10 z-50 py-12 px-8 rounded-2xl' 
            : 'relative w-full h-full py-12 px-8'
        }`}
      >
        
        {/* Contenedor con Zoom (Transform) */}
        <motion.div 
          layout
          className="transition-transform duration-300 ease-out origin-top"
          style={{ transform: `scale(${zoomLevel / 100})` }}
        >
          <Paginator>
            {content}
          </Paginator>
        </motion.div>

      {/* Controles Flotantes Inferiores */}
      <div className="fixed bottom-8 left-1/2 -translate-x-1/2 flex items-center gap-4 bg-white/90 backdrop-blur-md px-5 py-2.5 rounded-full shadow-lg border border-[var(--border)] z-[60] text-[13px] font-medium text-[var(--text-main)] transition-all hover:shadow-xl">
        <button 
          onClick={() => setZoom(zoomLevel - 10)} 
          className="p-1 hover:text-[var(--accent)] hover:bg-[var(--bg-sidebar)] rounded transition-colors"
          title="Alejar"
        >
          <ZoomOut size={16} strokeWidth={2.5}/>
        </button>
        
        <span className="w-10 text-center select-none">{zoomLevel}%</span>
        
        <button 
          onClick={() => setZoom(zoomLevel + 10)} 
          className="p-1 hover:text-[var(--accent)] hover:bg-[var(--bg-sidebar)] rounded transition-colors"
          title="Acercar"
        >
          <ZoomIn size={16} strokeWidth={2.5}/>
        </button>
        
        <div className="w-px h-5 bg-[#e6e2dd] mx-1" />
        
        <button 
          onClick={togglePreviewExpanded} 
          className="flex items-center gap-2 p-1 pl-2 pr-3 hover:text-[var(--accent)] hover:bg-[var(--bg-sidebar)] rounded transition-colors"
          title={isPreviewExpanded ? "Salir de enfoque" : "Enfocar vista previa"}
        >
          {isPreviewExpanded ? <Minimize2 size={16} strokeWidth={2.5}/> : <Maximize2 size={16} strokeWidth={2.5}/>}
          <span>{isPreviewExpanded ? 'Salir' : 'Enfocar'}</span>
        </button>
      </div>
      
    </motion.div>
    </>
  );
}
