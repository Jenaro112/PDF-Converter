import React from 'react';
import { CoverData } from '@/store/editor-store';

export function GeometricCorporateCover({ config }: { config: CoverData }) {
  return (
    <div 
      className="a4-page bg-white shadow-md print:shadow-none border border-[var(--border)] print:border-none relative shrink-0 flex overflow-hidden font-sans print:m-0"
      style={{ width: '210mm', height: '297mm', backgroundColor: '#ffffff', pageBreakAfter: 'always', breakAfter: 'page', fontFamily: 'Arial, Helvetica, sans-serif' }}
    >
      {/* Columna lateral decorativa */}
      <div className="w-[45mm] h-full bg-[#f4f7fa] border-r border-blue-100 flex flex-col justify-between py-[25mm] items-center shrink-0">
        <div className="w-full flex justify-center">
          {config.showLogo !== false && (
            <img 
              src="/LogoUADER.png" 
              alt="Logo" 
              className="w-[30mm] h-auto object-contain select-none opacity-90"
            />
          )}
        </div>
        
        <div className="text-center w-full px-2">
           <div className="w-px h-[50mm] bg-blue-300 mx-auto mb-8" />
           <span className="block text-blue-800 font-mono text-sm rotate-180" style={{ writingMode: 'vertical-rl' }}>
              {config.fecha || new Date().getFullYear().toString()}
           </span>
        </div>
      </div>
      
      {/* Contenido principal */}
      <div className="flex-1 p-[25mm] flex flex-col h-full bg-white relative">
        <div className="w-12 h-2 bg-blue-600 mb-8" />
        
        <h3 className="text-sm font-bold text-blue-600 uppercase tracking-widest mb-2">
          {config.materia}
        </h3>
        
        <h1 className="text-[3.5rem] font-bold text-gray-900 leading-[1.1] mb-6 tracking-tight max-w-[90%]">
          {config.title}
        </h1>
        
        {config.subtitle && (
          <p className="text-[1.5rem] text-gray-500 font-medium leading-relaxed max-w-[85%] border-l-4 border-blue-200 pl-6 my-4">
            {config.subtitle}
          </p>
        )}
        
        { (config.integrantes.filter(Boolean).length > 0 || config.profesores.filter(Boolean).length > 0) && (
          <div className="mt-auto pt-16">
            <div className="grid grid-cols-2 gap-px bg-blue-100 border border-blue-100 rounded-sm overflow-hidden">
              {config.integrantes.filter(Boolean).length > 0 && (
                <div className="bg-white p-6">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-blue-600 mb-4 border-b border-blue-50 pb-2">Integrantes</h4>
                  <div className="flex flex-col gap-1.5">
                    {config.integrantes.filter(Boolean).map(i => <span key={i} className="text-lg text-gray-800 font-medium">{i}</span>)}
                  </div>
                </div>
              )}
              {config.profesores.filter(Boolean).length > 0 && (
                <div className="bg-white p-6">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-blue-600 mb-4 border-b border-blue-50 pb-2">Docentes</h4>
                  <div className="flex flex-col gap-1.5">
                    {config.profesores.filter(Boolean).map(p => <span key={p} className="text-lg text-gray-800 font-medium">{p}</span>)}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
