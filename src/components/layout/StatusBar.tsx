'use client';

import { useRef } from 'react';
import { useEditorStore } from '@/store/editor-store';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';

gsap.registerPlugin(useGSAP);

export function StatusBar() {
  const { isDirty, cursorLine, cursorCol, wordCount, fileName } = useEditorStore();
  const statusRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    if (!statusRef.current) return;
    const tl = gsap.timeline();
    tl.fromTo(statusRef.current,
      { y: 5, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.3, ease: 'power2.out' }
    );
  }, [isDirty]);

  return (
    <div className="h-10 flex items-center justify-between px-6 text-[11px] uppercase tracking-wider select-none bg-white border-t border-[#E5E5E5] text-[#A3A3A3] font-semibold" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
      {/* Left side */}
      <div className="flex items-center gap-8">
        <div className="relative flex items-center" style={{ width: 100 }}>
          <div ref={statusRef} className="absolute left-0">
            {isDirty ? (
              <span className="text-[#4F46E5] flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-[#4F46E5] animate-pulse" />
                Sin guardar
              </span>
            ) : (
              <span className="text-[#10B981] flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-[#10B981]" />
                Guardado
              </span>
            )}
          </div>
        </div>
        <span className="hover:text-[#171717] transition-colors cursor-default">Ln {cursorLine}, Col {cursorCol}</span>
        <span className="hover:text-[#171717] transition-colors cursor-default">{wordCount} palabras</span>
      </div>

      {/* Right side */}
      <div className="flex items-center gap-8">
        <span className="hover:text-[#171717] transition-colors cursor-default">UTF-8</span>
        <span className="hover:text-[#171717] transition-colors cursor-default">{fileName ? 'Markdown' : 'Nuevo Documento'}</span>
      </div>
    </div>
  );
}
