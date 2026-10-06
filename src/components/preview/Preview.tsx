'use client';

import React, { useEffect, useState, useRef } from 'react';
import { createPortal } from 'react-dom';
import { useEditorStore } from '@/store/editor-store';
import { useMarkdownProcessor } from '@/lib/markdown/pipeline';
import { generateRootCSS } from '@/lib/themes/document-themes';
import { Paginator } from './Paginator';
import { ZoomIn, ZoomOut, Maximize2, Minimize2 } from 'lucide-react';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';

gsap.registerPlugin(useGSAP);

function PreviewControls({
  zoomLevel, setZoom, isPreviewExpanded, togglePreviewExpanded
}: {
  zoomLevel: number;
  setZoom: (z: number) => void;
  isPreviewExpanded: boolean;
  togglePreviewExpanded: () => void;
}) {
  return (
    <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex items-center gap-4 bg-white/90 backdrop-blur-xl px-6 py-3 rounded-2xl shadow-xl border border-[#E5E5E5] z-[60] text-[13px] font-semibold text-[#171717] transition-all hover:shadow-2xl">
      <button 
        onClick={(e) => { e.stopPropagation(); setZoom(zoomLevel - 10); }} 
        className="p-1.5 text-[#A3A3A3] hover:text-[#4F46E5] hover:bg-[#EEF2FF] rounded-lg transition-colors"
        title="Alejar"
      >
        <ZoomOut size={18} strokeWidth={2.5}/>
      </button>
      
      <span className="w-12 text-center select-none font-medium text-sm" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>{zoomLevel}%</span>
      
      <button 
        onClick={(e) => { e.stopPropagation(); setZoom(zoomLevel + 10); }} 
        className="p-1.5 text-[#A3A3A3] hover:text-[#4F46E5] hover:bg-[#EEF2FF] rounded-lg transition-colors"
        title="Acercar"
      >
        <ZoomIn size={18} strokeWidth={2.5}/>
      </button>
      
      <div className="w-px h-6 bg-[#E5E5E5] mx-2" />
      
      <button 
        onClick={(e) => { e.stopPropagation(); togglePreviewExpanded(); }} 
        className="flex items-center gap-2 p-1.5 pl-3 pr-4 text-[#A3A3A3] hover:text-[#4F46E5] hover:bg-[#EEF2FF] rounded-lg transition-colors"
        title={isPreviewExpanded ? "Salir de enfoque" : "Enfocar vista previa"}
      >
        {isPreviewExpanded ? <Minimize2 size={18} strokeWidth={2.5}/> : <Maximize2 size={18} strokeWidth={2.5}/>}
        <span>{isPreviewExpanded ? 'Salir' : 'Enfocar'}</span>
      </button>
    </div>
  );
}

export function Preview() {
  const { documentText, zoomLevel, setZoom, isPreviewExpanded, togglePreviewExpanded, activeTheme } = useEditorStore();
  const previewRef = useRef<HTMLDivElement>(null);
  const portalPreviewRef = useRef<HTMLDivElement>(null);
  const [mounted, setMounted] = useState(false);
  
  const content = useMarkdownProcessor(documentText);

  useEffect(() => {
    setMounted(true);
  }, []);

  // Sync scroll
  useEffect(() => {
    const unsub = useEditorStore.subscribe((state, prevState) => {
      if (state.editorScrollPercent !== prevState.editorScrollPercent) {
        const refs = [previewRef.current, portalPreviewRef.current];
        refs.forEach(ref => {
          if (ref) {
            const maxScroll = ref.scrollHeight - ref.clientHeight;
            if (maxScroll > 0) {
              ref.scrollTop = maxScroll * state.editorScrollPercent;
            }
          }
        });
      }
    });
    return unsub;
  }, []);

  const innerContent = (
    <div className="h-full w-full flex justify-center py-12 px-8">
      <div 
        className="transition-transform duration-300 ease-out origin-top"
        style={{ transform: `scale(${zoomLevel / 100})` }}
      >
        <Paginator>
          {content}
        </Paginator>
      </div>
    </div>
  );

  return (
    <>
      <style dangerouslySetInnerHTML={{ __html: generateRootCSS(activeTheme) }} />

      {/* INLINE PREVIEW */}
      <div 
        className="relative w-full h-full bg-[#FAFAFA] flex flex-col overflow-hidden"
        style={{ opacity: isPreviewExpanded ? 0 : 1, pointerEvents: isPreviewExpanded ? 'none' : 'auto' }}
      >
        <div ref={previewRef} className="flex-1 overflow-auto custom-scroll">
          {innerContent}
        </div>
        {!isPreviewExpanded && (
          <PreviewControls 
            zoomLevel={zoomLevel} 
            setZoom={setZoom} 
            isPreviewExpanded={false} 
            togglePreviewExpanded={togglePreviewExpanded} 
          />
        )}
      </div>

      {/* EXPANDED PREVIEW (Portal) */}
      {mounted && isPreviewExpanded && createPortal(
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 md:p-10">
          {/* Backdrop */}
          <div 
            className="absolute inset-0 bg-[#FAFAFA]/90 backdrop-blur-xl animate-in fade-in duration-300"
            onClick={togglePreviewExpanded}
          />

          {/* Card */}
          <div 
            className="relative w-full h-full max-w-6xl bg-white rounded-3xl shadow-2xl overflow-hidden border border-[#E5E5E5] flex flex-col animate-in zoom-in-95 duration-300"
          >
            <div ref={portalPreviewRef} className="flex-1 overflow-auto custom-scroll">
              {innerContent}
            </div>
            <PreviewControls 
              zoomLevel={zoomLevel} 
              setZoom={setZoom} 
              isPreviewExpanded={true} 
              togglePreviewExpanded={togglePreviewExpanded} 
            />
          </div>
        </div>,
        document.body
      )}
    </>
  );
}
