import React from 'react';
import { CoverData } from '@/store/editor-store';

export function BarraAzulCover({ config }: { config: CoverData }) {
  return (
    <div 
      className="a4-page bg-white shadow-md print:shadow-none border border-[var(--border)] print:border-none relative shrink-0 flex overflow-hidden font-sans print:m-0"
      style={{ width: '210mm', height: '297mm', backgroundColor: '#ffffff', pageBreakAfter: 'always', breakAfter: 'page' }}
    >
      {/* Barra Azul Izquierda */}
      <div className="w-[55mm] h-full bg-[#265e8a] flex flex-col pt-[70mm] px-[8mm] shadow-[4px_0_24px_rgba(0,0,0,0.08)] z-10">
        <img 
          src="/LogoUADER.png" 
          alt="Logo UADER FCyT" 
          className="w-full h-auto object-contain select-none opacity-95"
        />
      </div>
      
      {/* Contenido Principal */}
      <div className="flex-1 py-[60mm] px-[25mm] flex flex-col h-full" style={{ fontFamily: 'Arial, Helvetica, sans-serif' }}>
        
        <h2 className="text-[13px] font-bold text-gray-400 uppercase tracking-[0.3em] mb-4">
          {config.materia}
        </h2>

        <div className="w-full">
          <h1 className="text-[4rem] font-black text-gray-900 leading-[1.1] mb-6 tracking-tight text-balance">
            {config.title}
          </h1>
          <p className="text-[1.5rem] text-gray-500 font-normal text-balance">
            {config.subtitle}
          </p>
        </div>
        
        {(config.integrantes.filter(Boolean).length > 0 || config.profesores.filter(Boolean).length > 0) && (
          <div className="mt-auto grid grid-cols-2 gap-12 w-full border-t border-gray-100 pt-10">
              {config.integrantes.filter(Boolean).length > 0 && (
                <div>
                  <span className="block text-[11px] font-bold uppercase tracking-[0.25em] text-gray-400 mb-4">Integrantes</span>
                  <div className="flex flex-col gap-1.5">
                    {config.integrantes.filter(Boolean).map(i => <span key={i} className="text-[16px] text-gray-800 font-medium">{i}</span>)}
                  </div>
                </div>
              )}

              {config.profesores.filter(Boolean).length > 0 && (
                <div>
                  <span className="block text-[11px] font-bold uppercase tracking-[0.25em] text-gray-400 mb-4">Docentes</span>
                  <div className="flex flex-col gap-1.5">
                    {config.profesores.filter(Boolean).map(p => <span key={p} className="text-[16px] text-gray-800 font-medium">{p}</span>)}
                  </div>
                </div>
              )}
          </div>
        )}
      </div>
    </div>
  );
}
