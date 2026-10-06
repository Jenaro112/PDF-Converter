import React from 'react';
import { CoverData } from '@/store/editor-store';

export function AcademicElegantCover({ config }: { config: CoverData }) {
  const fontStyle = { fontFamily: '"Times New Roman", Times, serif' };
  return (
    <div 
      className="a4-page bg-white shadow-md print:shadow-none border border-[#E5E5E5] print:border-none relative shrink-0 flex flex-col items-center justify-between p-[35mm] print:m-0"
      style={{ width: '210mm', height: '297mm', backgroundColor: '#ffffff', pageBreakAfter: 'always', breakAfter: 'page', ...fontStyle }}
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
        <h3 className="text-xl font-bold uppercase tracking-widest text-[#171717] mb-2" style={fontStyle}>
          {config.materia}
        </h3>
        <div className="w-16 h-[2px] bg-[#171717] mt-2 mb-16" />
      </div>

      <div className="w-full flex flex-col items-center text-center">
        <h1 className="text-[3.5rem] font-bold text-[#111827] leading-[1.2] mb-6" style={fontStyle}>
          {config.title}
        </h1>
        {config.subtitle && (
          <h2 className="text-[1.8rem] text-[#4B5563] font-normal italic" style={fontStyle}>
            {config.subtitle}
          </h2>
        )}
      </div>

      {(config.integrantes.filter(Boolean).length > 0 || config.profesores.filter(Boolean).length > 0) && (
        <div className="w-full grid grid-cols-2 gap-8 text-center border-t border-b border-[#D1D5DB] py-10">
          {config.integrantes.filter(Boolean).length > 0 && (
            <div>
              <h4 className="text-sm font-bold uppercase tracking-[0.2em] text-[#737373] mb-4" style={fontStyle}>Presentado por</h4>
              <div className="flex flex-col gap-2">
                {config.integrantes.filter(Boolean).map(i => <span key={i} className="text-xl text-[#111827]" style={fontStyle}>{i}</span>)}
              </div>
            </div>
          )}
          {config.profesores.filter(Boolean).length > 0 && (
            <div>
              <h4 className="text-sm font-bold uppercase tracking-[0.2em] text-[#737373] mb-4" style={fontStyle}>Docentes / Tutor</h4>
              <div className="flex flex-col gap-2">
                {config.profesores.filter(Boolean).map(p => <span key={p} className="text-xl text-[#111827]" style={fontStyle}>{p}</span>)}
              </div>
            </div>
          )}
        </div>
      )}
      
      <div className="w-full text-center mt-12">
        <span className="text-lg text-[#4B5563]" style={fontStyle}>
          {config.fecha || new Date().getFullYear().toString()}
        </span>
      </div>
    </div>
  );
}
