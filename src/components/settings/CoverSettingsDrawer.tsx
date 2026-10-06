'use client';
import React, { useRef, useEffect } from 'react';
import { useEditorStore } from '@/store/editor-store';
import { X, Book, Users, GraduationCap } from 'lucide-react';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';

gsap.registerPlugin(useGSAP);

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div>
      <label className="block text-xs text-[#737373] mb-1.5 font-semibold" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>{label}</label>
      {children}
    </div>
  );
}

const inputCls =
  'w-full border border-[#E5E5E5] rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-[#4F46E5] focus:ring-4 focus:ring-[#4F46E5]/10 transition-all bg-[#FAFAFA] font-medium text-[#171717]';

function StyleCard({
  selected, onClick, label, preview
}: {
  selected: boolean;
  onClick: () => void;
  label: string;
  preview: React.ReactNode;
}) {
  return (
    <div
      onClick={onClick}
      className={`cursor-pointer rounded-xl border-2 transition-all overflow-hidden bg-white ${
        selected ? 'border-[#4F46E5] shadow-md scale-[1.02]' : 'border-[#E5E5E5] hover:border-[#A3A3A3] opacity-70 hover:opacity-100'
      }`}
    >
      <div className="h-24 w-full bg-[#FAFAFA] border-b border-[#E5E5E5] relative">
        {preview}
      </div>
      <div className="p-3 text-center text-xs font-semibold text-[#171717] bg-white">
        {label}
      </div>
    </div>
  );
}

export function CoverSettingsDrawer() {
  const { isSettingsOpen, toggleSettings, coverConfig, setCover } = useEditorStore();
  const config = coverConfig;
  const drawerRef = useRef<HTMLDivElement>(null);
  const backdropRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    if (isSettingsOpen) {
      gsap.to(backdropRef.current, { opacity: 1, duration: 0.3, ease: 'power2.out', display: 'block' });
      gsap.to(drawerRef.current, { x: 0, duration: 0.4, ease: 'power3.out' });
    } else {
      gsap.to(drawerRef.current, { x: '100%', duration: 0.3, ease: 'power3.in' });
      gsap.to(backdropRef.current, { opacity: 0, duration: 0.3, ease: 'power2.in', display: 'none' });
    }
  }, [isSettingsOpen]);

  if (!config) return null;

  const up = (k: keyof typeof config, v: any) => setCover({ ...config, [k]: v });

  const addArr = (k: 'integrantes' | 'profesores') => {
    up(k, [...config[k], '']);
  };

  const updateArr = (k: 'integrantes' | 'profesores', i: number, v: string) => {
    const arr = [...config[k]];
    arr[i] = v;
    up(k, arr);
  };

  const delArr = (k: 'integrantes' | 'profesores', i: number) => {
    const arr = [...config[k]];
    arr.splice(i, 1);
    up(k, arr);
  };

  const today = new Date().toLocaleDateString('es-AR');

  return (
    <>
      <div 
        ref={backdropRef}
        className="fixed inset-0 bg-[#171717]/20 backdrop-blur-sm z-[90] hidden opacity-0"
        onClick={toggleSettings}
      />
      <div
        ref={drawerRef}
        className="fixed top-0 right-0 h-full w-[400px] max-w-[90vw] bg-white border-l border-[#E5E5E5] shadow-2xl z-[100] flex flex-col translate-x-full"
      >
        <div className="flex items-center justify-between px-6 py-5 border-b border-[#E5E5E5] bg-white/80 backdrop-blur-md">
          <div className="flex items-center gap-3 text-[#171717]">
            <div className="p-2 bg-[#EEF2FF] rounded-lg text-[#4F46E5]">
              <Book size={20} />
            </div>
            <h2 className="font-bold text-lg tracking-tight" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>Configuracin del Documento</h2>
          </div>
          <button
            onClick={toggleSettings}
            className="p-2 rounded-xl hover:bg-[#F3F4F6] text-[#A3A3A3] hover:text-[#171717] transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-6 custom-scroll">
          <div className="space-y-10">
            {/* Activar Portada */}
            <div className="flex items-center justify-between bg-[#FAFAFA] p-4 rounded-2xl border border-[#E5E5E5]">
              <div>
                <span className="text-sm font-bold text-[#171717] block" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>Generar Portada</span>
                <span className="text-xs text-[#737373] mt-1 block">Aade una pgina de ttulo al exportar</span>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  className="sr-only peer"
                  checked={config.showCover}
                  onChange={(e) => up('showCover', e.target.checked)}
                />
                <div className="w-11 h-6 bg-[#E5E5E5] peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#4F46E5]"></div>
              </label>
            </div>

            {/* Estilo de Portada */}
            <div className="space-y-4">
              <label className="text-xs font-bold text-[#A3A3A3] uppercase tracking-wider" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>Estilo Visual</label>
              <div className="grid grid-cols-2 gap-4">
                <StyleCard
                  label="Elegante Acadmica"
                  selected={config.coverStyle === 'academic_elegant'}
                  onClick={() => up('coverStyle', 'academic_elegant')}
                  preview={
                    <div className="w-full h-full flex flex-col items-center justify-center p-2 bg-white">
                      <div className="w-4 h-4 rounded-full border border-gray-800 mb-2" />
                      <div className="w-16 h-2 bg-gray-800 mb-1" />
                      <div className="w-12 h-1 bg-gray-200 mb-3" />
                      <div className="w-8 h-px bg-gray-400 mb-2" />
                      <div className="w-10 h-1 bg-gray-400" />
                    </div>
                  }
                />
                <StyleCard
                  label="Minimalista Moderna"
                  selected={config.coverStyle === 'modern_minimal'}
                  onClick={() => up('coverStyle', 'modern_minimal')}
                  preview={
                    <div className="w-full h-full bg-white flex flex-col items-start justify-end p-3">
                      <div className="w-6 h-6 bg-[#F3F4F6] rounded-lg absolute top-2 right-2" />
                      <div className="w-20 h-3 bg-[#171717] mb-1" />
                      <div className="w-14 h-1 bg-[#A3A3A3] mb-4" />
                      <div className="w-10 h-1 bg-[#D4D4D8]" />
                    </div>
                  }
                />
                <StyleCard
                  label="Tcnica / Geomtrica"
                  selected={config.coverStyle === 'geometric_corporate'}
                  onClick={() => up('coverStyle', 'geometric_corporate')}
                  preview={
                    <div className="w-full h-full bg-white flex relative overflow-hidden">
                      <div className="w-3 h-full bg-[#4F46E5]/10 absolute left-0 top-0" />
                      <div className="ml-4 p-2 flex flex-col justify-center w-full">
                        <div className="w-16 h-2 bg-[#171717] mb-1" />
                        <div className="w-12 h-1 bg-[#4F46E5] mb-3" />
                        <div className="w-full h-8 bg-[#F3F4F6] mt-2 flex flex-col gap-1 p-1">
                          <div className="w-8 h-1 bg-[#D4D4D8]" />
                          <div className="w-12 h-1 bg-[#A3A3A3]" />
                        </div>
                      </div>
                    </div>
                  }
                />
                <StyleCard
                  label="FCyT Clsica"
                  selected={config.coverStyle === 'fcyt_uader'}
                  onClick={() => up('coverStyle', 'fcyt_uader')}
                  preview={
                    <div className="w-full h-full flex flex-col p-2 bg-white">
                      <div className="flex items-center gap-1 mb-2">
                        <div className="w-4 h-4 bg-[#EEF2FF] rounded" />
                        <div className="w-px h-4 bg-[#E5E5E5]" />
                        <div className="w-8 h-2 bg-[#A3A3A3]" />
                      </div>
                      <div className="flex-1 flex flex-col items-center justify-center gap-1">
                        <div className="w-14 h-1.5 bg-[#171717]" />
                        <div className="w-10 h-1 bg-[#A3A3A3]" />
                      </div>
                    </div>
                  }
                />
                <StyleCard
                  label="Blanca Simple"
                  selected={config.coverStyle === 'blanca_simple'}
                  onClick={() => up('coverStyle', 'blanca_simple')}
                  preview={
                    <div className="w-full h-full flex flex-col items-center justify-center p-2 bg-white">
                      <div className="w-20 h-2 bg-[#171717] mb-2" />
                      <div className="w-12 h-1 bg-[#737373] mb-4" />
                      <div className="w-16 h-1 bg-[#D4D4D8]" />
                    </div>
                  }
                />
                <StyleCard
                  label="Barra Azul"
                  selected={config.coverStyle === 'barra_azul'}
                  onClick={() => up('coverStyle', 'barra_azul')}
                  preview={
                    <div className="w-full h-full flex flex-col items-center justify-center p-2 bg-white relative">
                      <div className="absolute top-0 left-0 w-full h-2 bg-[#4F46E5]" />
                      <div className="w-16 h-2 bg-[#171717] mb-2 mt-2" />
                      <div className="w-10 h-1 bg-[#737373]" />
                    </div>
                  }
                />
              </div>
            </div>

            {/* Datos del documento */}
            <div className="space-y-5">
              <label className="text-xs font-bold text-[#A3A3A3] uppercase tracking-wider" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>Datos del Documento</label>
              <Field label="Ttulo principal">
                <input type="text" value={config.title} onChange={(e) => up('title', e.target.value)} className={inputCls} placeholder="Trabajo Integrador Final" />
              </Field>
              <Field label="Subttulo / Descripcin">
                <input type="text" value={config.subtitle} onChange={(e) => up('subtitle', e.target.value)} className={inputCls} placeholder="Anlisis de Sistemas" />
              </Field>
              <Field label="Ctedra / Materia">
                <input type="text" value={config.materia} onChange={(e) => up('materia', e.target.value)} className={inputCls} placeholder="Taller de Integracin" />
              </Field>
              <div className="grid grid-cols-2 gap-4">
                <Field label="Sigla (encabezado)">
                  <input type="text" value={config.sigla ?? ''} onChange={(e) => up('sigla', e.target.value)} className={inputCls} placeholder="TI" maxLength={8} />
                </Field>
                <Field label="Fecha">
                  <input type="text" value={config.fecha ?? today} onChange={(e) => up('fecha', e.target.value)} className={inputCls} placeholder={today} />
                </Field>
              </div>
            </div>

            {/* Integrantes */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <label className="text-xs font-bold text-[#A3A3A3] uppercase tracking-wider flex items-center gap-2" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
                  <Users size={14} /> Integrantes
                </label>
                <button onClick={() => addArr('integrantes')} className="text-xs font-bold text-[#4F46E5] hover:text-[#4338CA] transition-colors">+ Agregar</button>
              </div>
              <div className="space-y-3">
                {config.integrantes.map((v, i) => (
                  <div key={i} className="flex items-center gap-2">
                    <input type="text" value={v} onChange={(e) => updateArr('integrantes', i, e.target.value)} className={inputCls} placeholder="Nombre del integrante" />
                    <button onClick={() => delArr('integrantes', i)} className="text-[#A3A3A3] hover:text-[#EF4444] p-2 bg-[#FAFAFA] rounded-xl transition-colors"><X size={16} /></button>
                  </div>
                ))}
              </div>
            </div>

            {/* Profesores */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <label className="text-xs font-bold text-[#A3A3A3] uppercase tracking-wider flex items-center gap-2" style={{ fontFamily: "'Space Grotesk', sans-serif" }}>
                  <GraduationCap size={14} /> Equipo Docente
                </label>
                <button onClick={() => addArr('profesores')} className="text-xs font-bold text-[#4F46E5] hover:text-[#4338CA] transition-colors">+ Agregar</button>
              </div>
              <div className="space-y-3">
                {config.profesores.map((v, i) => (
                  <div key={i} className="flex items-center gap-2">
                    <input type="text" value={v} onChange={(e) => updateArr('profesores', i, e.target.value)} className={inputCls} placeholder="Nombre del docente" />
                    <button onClick={() => delArr('profesores', i)} className="text-[#A3A3A3] hover:text-[#EF4444] p-2 bg-[#FAFAFA] rounded-xl transition-colors"><X size={16} /></button>
                  </div>
                ))}
              </div>
            </div>

          </div>
        </div>
      </div>
    </>
  );
}
