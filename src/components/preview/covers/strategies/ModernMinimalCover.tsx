import React from 'react';
import { CoverData } from '@/store/editor-store';

export function ModernMinimalCover({ config }: { config: CoverData }) {
  return (
    <div 
      className="a4-page bg-white shadow-md print:shadow-none border border-[var(--border)] print:border-none relative shrink-0 flex flex-col font-sans print:m-0 p-[25mm]"
      style={{ width: '210mm', height: '297mm', backgroundColor: '#ffffff', pageBreakAfter: 'always', breakAfter: 'page', fontFamily: 'Inter, system-ui, sans-serif' }}
    >
      <div className="flex-1 flex flex-col justify-end pb-[20mm]">
        {config.showLogo !== false && (
          <img 
            src="/LogoUADER.png" 
            alt="Logo" 
            className="absolute top-[25mm] right-[25mm] w-[45mm] h-auto object-contain select-none"
          />
        )}
        
        <h3 className="text-xl font-semibold text-blue-600 mb-6 tracking-wide">
          {config.materia}
        </h3>
        
        <h1 className="text-[5rem] font-black text-gray-900 leading-[1.05] tracking-tighter text-balance mb-8">
          {config.title}
        </h1>
        
        {config.subtitle && (
          <h2 className="text-[2rem] text-gray-500 font-light leading-snug mb-16 max-w-[85%]">
            {config.subtitle}
          </h2>
        )}
      </div>

      <div className="w-full flex justify-between items-end border-t-[3px] border-blue-600 pt-8 mt-auto pb-4">
        <div className="flex flex-col gap-8">
          <div>
            <span className="block text-xs font-bold uppercase tracking-widest text-blue-600 mb-2">Integrantes</span>
            <div className="flex flex-col gap-1">
              {config.integrantes.filter(Boolean).length > 0 ? (
                config.integrantes.filter(Boolean).map(i => <span key={i} className="text-lg font-medium text-gray-800">{i}</span>)
              ) : null}
            </div>
          </div>
          <div>
            <span className="block text-xs font-bold uppercase tracking-widest text-blue-600 mb-2">Docentes</span>
            <div className="flex flex-col gap-1">
              {config.profesores.filter(Boolean).length > 0 ? (
                config.profesores.filter(Boolean).map(p => <span key={p} className="text-lg font-medium text-gray-800">{p}</span>)
              ) : null}
            </div>
          </div>
        </div>
        
        <div className="text-right pb-1">
          <span className="text-lg font-semibold text-gray-800">
            {config.fecha || new Date().getFullYear().toString()}
          </span>
        </div>
      </div>
    </div>
  );
}
