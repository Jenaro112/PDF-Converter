import React from 'react';
import { CoverData } from '@/store/editor-store';
import { Sparkles } from 'lucide-react';

export function BlancaSimpleCover({ config }: { config: CoverData }) {
  return (
    <div 
      className="a4-page bg-white shadow-md print:shadow-none border border-[var(--border)] print:border-none relative shrink-0 flex flex-col items-center justify-center text-center px-24 overflow-hidden print:m-0"
      style={{ width: '210mm', height: '297mm', backgroundColor: '#ffffff', pageBreakAfter: 'always', breakAfter: 'page' }}
    >
      <Sparkles className="text-gray-200 mb-8" size={48} strokeWidth={1} />
      <h2 className="text-sm text-gray-400 uppercase tracking-[0.3em] font-medium mb-6">{config.materia}</h2>
      <h1 className="text-[4.5rem] font-black text-gray-900 tracking-tighter leading-[1.05] text-balance mb-8">
        {config.title}
      </h1>
      <p className="text-xl text-gray-500 font-light italic max-w-lg">
        {config.subtitle}
      </p>
      
      {(config.integrantes.length > 0 || config.profesores.length > 0) && (
        <div className="absolute bottom-24 flex gap-16 text-left">
          {config.integrantes.length > 0 && (
            <div>
              <h3 className="text-[10px] uppercase text-gray-400 font-bold mb-2 tracking-widest">Integrantes</h3>
              {config.integrantes.map(i => <p key={i} className="text-sm font-medium text-gray-800">{i}</p>)}
            </div>
          )}
          {config.profesores.length > 0 && (
            <div>
              <h3 className="text-[10px] uppercase text-gray-400 font-bold mb-2 tracking-widest">Profesores</h3>
              {config.profesores.map(p => <p key={p} className="text-sm font-medium text-gray-800">{p}</p>)}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
