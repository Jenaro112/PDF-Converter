'use client';

import React, { useEffect, useState } from 'react';
import { createPortal } from 'react-dom';
import { useEditorStore } from '@/store/editor-store';
import { useMarkdownProcessor } from '@/lib/markdown/pipeline';
import { generateRootCSS } from '@/lib/themes/document-themes';
import { Paginator } from './Paginator';
import { ZoomIn, ZoomOut, Maximize2, Minimize2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

function PreviewControls({
  zoomLevel, setZoom, isPreviewExpanded, togglePreviewExpanded
}: {
  zoomLevel: number;
  setZoom: (z: number) => void;
  isPreviewExpanded: boolean;
  togglePreviewExpanded: () => void;
}) {
  return (
    <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex items-center gap-4 bg-[var(--bg-surface)]/90 backdrop-blur-md px-5 py-2.5 rounded-full shadow-lg border border-[var(--border)] z-[60] text-[13px] font-medium text-[var(--text-main)] transition-all hover:shadow-xl">
      <button 
        onClick={(e) => { e.stopPropagation(); setZoom(zoomLevel - 10); }} 
        className="p-1 hover:text-[var(--accent)] hover:bg-[var(--bg-sidebar)] rounded transition-colors"
        title="Alejar"
      >
        <ZoomOut size={16} strokeWidth={2.5}/>
      </button>
      
      <span className="w-10 text-center select-none">{zoomLevel}%</span>
      
      <button 
        onClick={(e) => { e.stopPropagation(); setZoom(zoomLevel + 10); }} 
        className="p-1 hover:text-[var(--accent)] hover:bg-[var(--bg-sidebar)] rounded transition-colors"
        title="Acercar"
      >
        <ZoomIn size={16} strokeWidth={2.5}/>
      </button>
      
      <div className="w-px h-5 bg-[var(--border)] mx-1" />
      
      <button 
        onClick={(e) => { e.stopPropagation(); togglePreviewExpanded(); }} 
        className="flex items-center gap-2 p-1 pl-2 pr-3 hover:text-[var(--accent)] hover:bg-[var(--bg-sidebar)] rounded transition-colors"
        title={isPreviewExpanded ? "Salir de enfoque" : "Enfocar vista previa"}
      >
        {isPreviewExpanded ? <Minimize2 size={16} strokeWidth={2.5}/> : <Maximize2 size={16} strokeWidth={2.5}/>}
        <span>{isPreviewExpanded ? 'Salir' : 'Enfocar'}</span>
      </button>
    </div>
  );
}

export function Preview() {
  const { documentText, zoomLevel, setZoom, isPreviewExpanded, togglePreviewExpanded, activeTheme } = useEditorStore();
  const previewRef = React.useRef<HTMLDivElement>(null);
  const [mounted, setMounted] = useState(false);
  
  const content = useMarkdownProcessor(documentText);

  useEffect(() => {
    setMounted(true);
  }, []);

  // Sync scroll
  useEffect(() => {
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

  const innerContent = (
    <div className="h-full w-full flex justify-center py-12 px-8">
      <motion.div 
        layout
        className="transition-transform duration-300 ease-out origin-top"
        style={{ transform: `scale(${zoomLevel / 100})` }}
      >
        <Paginator>
          {content}
        </Paginator>
      </motion.div>
    </div>
  );

  return (
    <>
      <style dangerouslySetInnerHTML={{ __html: generateRootCSS(activeTheme) }} />

      {/* INLINE PREVIEW (when not expanded) */}
      <AnimatePresence>
        {!isPreviewExpanded && (
          <motion.div 
            layoutId="preview-card"
            className="relative w-full h-full bg-[var(--bg-preview)] shadow-inner flex flex-col overflow-hidden"
            transition={{ type: "spring", bounce: 0, duration: 0.5 }}
          >
            <div ref={previewRef} className="flex-1 overflow-auto">
              {innerContent}
            </div>
            <PreviewControls 
              zoomLevel={zoomLevel} 
              setZoom={setZoom} 
              isPreviewExpanded={false} 
              togglePreviewExpanded={togglePreviewExpanded} 
            />
          </motion.div>
        )}
      </AnimatePresence>

      {/* EXPANDED PREVIEW (Portal) */}
      {mounted && createPortal(
        <AnimatePresence>
          {isPreviewExpanded && (
            <div className="fixed inset-0 z-50 flex items-center justify-center p-4 md:p-10 pointer-events-none">
              
              {/* Backdrop */}
              <motion.div 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.4 }}
                className="absolute inset-0 bg-[var(--bg-base)]/80 backdrop-blur-md pointer-events-auto"
                onClick={togglePreviewExpanded}
              />

              {/* Card */}
              <motion.div 
                layoutId="preview-card"
                className="relative w-full h-full max-w-6xl bg-[var(--bg-preview)] rounded-2xl shadow-2xl overflow-hidden border border-[var(--border)] pointer-events-auto flex flex-col"
                transition={{ type: "spring", bounce: 0, duration: 0.5 }}
              >
                <div ref={previewRef} className="flex-1 overflow-auto">
                  {innerContent}
                </div>
                <PreviewControls 
                  zoomLevel={zoomLevel} 
                  setZoom={setZoom} 
                  isPreviewExpanded={true} 
                  togglePreviewExpanded={togglePreviewExpanded} 
                />
              </motion.div>
            </div>
          )}
        </AnimatePresence>,
        document.body
      )}
    </>
  );
}
