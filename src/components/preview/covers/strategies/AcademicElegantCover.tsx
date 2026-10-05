import React from 'react';
import { CoverData } from '@/store/editor-store';

export function AcademicElegantCover({ config }: { config: CoverData }) {
  return (
    <div 
      className="a4-page bg-white shadow-md print:shadow-none border border-[var(--border)] print:border-none relative shrink-0 flex flex-col items-center justify-between p-[35mm] font-serif print:m-0"
      style={{ width: '210mm', height: '297mm', backgroundColor: '#ffffff', pageBreakAfter: 'always', breakAfter: 'page', fontFamily: '"Times New Roman", Times, serif' }}
    >
      <div className="w-full flex flex-col items-center text-center">
        {config.showLogo !== false && (
          <img 
            src="/LogoUADER.png" 
            alt="Logo" 
            className="w-[50mm] h-auto object-contain select-none mb-10 opacity-90"
            style={{ filter: 'grayscale(100%) contrast(1.2)' }}
          />
        )}
        <h3 className="text-xl font-bold uppercase tracking-widest text-gray-800 mb-2">
          {config.materia}
        </h3>
        <div className="w-16 h-[2px] bg-gray-800 mt-2 mb-16" />
      </div>

      <div className="w-full flex flex-col items-center text-center">
        <h1 className="text-[3.5rem] font-bold text-gray-900 leading-[1.2] mb-6">
          {config.title}
        </h1>
        {config.subtitle && (
          <h2 className="text-[1.8rem] text-gray-600 font-normal italic">
            {config.subtitle}
          </h2>
        )}
      </div>

      {(config.integrantes.filter(Boolean).length > 0 || config.profesores.filter(Boolean).length > 0) && (
        <div className="w-full grid grid-cols-2 gap-8 text-center border-t border-b border-gray-300 py-10">
          {config.integrantes.filter(Boolean).length > 0 && (
            <div>
              <h4 className="text-sm font-bold uppercase tracking-[0.2em] text-gray-500 mb-4">Presentado por</h4>
              <div className="flex flex-col gap-2">
                {config.integrantes.filter(Boolean).map(i => <span key={i} className="text-xl text-gray-900">{i}</span>)}
              </div>
            </div>
          )}
          {config.profesores.filter(Boolean).length > 0 && (
            <div>
              <h4 className="text-sm font-bold uppercase tracking-[0.2em] text-gray-500 mb-4">Docentes / Tutor</h4>
              <div className="flex flex-col gap-2">
                {config.profesores.filter(Boolean).map(p => <span key={p} className="text-xl text-gray-900">{p}</span>)}
              </div>
            </div>
          )}
        </div>
      )}
      
      <div className="w-full text-center mt-12">
        <span className="text-lg text-gray-600">
          {config.fecha || new Date().getFullYear().toString()}
        </span>
      </div>
    </div>
  );
}
