'use client';
import React from 'react';
import { useEditorStore } from '@/store/editor-store';
import { X, Book, Users, GraduationCap } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

// ─── Tiny helper ─────────────────────────────────────────────────────────────
function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div>
      <label className="block text-xs text-gray-500 mb-1.5 font-medium">{label}</label>
      {children}
    </div>
  );
}

const inputCls =
  'w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[var(--accent)] focus:ring-1 focus:ring-[var(--accent)]/30 transition-all bg-white';

// ─── Cover style cards ────────────────────────────────────────────────────────
function StyleCard({
  label, selected, onClick, preview,
}: {
  label: string;
  selected: boolean;
  onClick: () => void;
  preview: React.ReactNode;
}) {
  return (
    <button
      onClick={onClick}
      className={`border-2 rounded-xl text-left overflow-hidden transition-all ${
        selected ? 'border-[var(--accent)] ring-2 ring-[var(--accent)]/20' : 'border-gray-200 hover:border-gray-300'
      }`}
    >
      <div className="h-24 bg-gray-50 flex items-center justify-center overflow-hidden">{preview}</div>
      <div className="p-3 bg-white border-t border-gray-100">
        <p className="text-sm font-semibold text-gray-800">{label}</p>
      </div>
    </button>
  );
}

// ─── Main component ───────────────────────────────────────────────────────────
export function CoverSettingsDrawer() {
  const { isSettingsOpen, toggleSettings, coverConfig, setCover } = useEditorStore();

  if (!isSettingsOpen) return null;

  const today = new Date().toLocaleDateString('es-AR', {
    day: '2-digit', month: '2-digit', year: 'numeric',
  });

  const config = coverConfig || {
    showCover:  false,
    title:      'Trabajo Integrador Final',
    subtitle:   'Análisis de Sistemas',
    materia:    'Taller de Integración',
    coverStyle: 'fcyt_uader' as const,
    integrantes: [''],
    profesores:  [''],
    sigla:       'TI',
    fecha:       today,
  };

  const up = (field: keyof typeof config, value: unknown) =>
    setCover({ ...config, [field]: value } as typeof config);

  const updateArr = (field: 'integrantes' | 'profesores', i: number, val: string) => {
    const a = [...config[field]]; a[i] = val; up(field, a);
  };
  const addArr = (field: 'integrantes' | 'profesores') => up(field, [...config[field], '']);
  const delArr = (field: 'integrantes' | 'profesores', i: number) => {
    const a = config[field].filter((_, idx) => idx !== i);
    up(field, a.length > 0 ? a : ['']);
  };

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, x: 400 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: 400 }}
        transition={{ type: 'spring', bounce: 0, duration: 0.4 }}
        className="fixed top-0 right-0 bottom-0 w-[450px] bg-white shadow-2xl border-l border-gray-200 z-[100] flex flex-col overflow-hidden"
      >
        {/* Header */}
        <div className="h-16 border-b border-gray-100 flex items-center justify-between px-6 shrink-0 bg-gray-50/50">
          <h2 className="font-bold text-gray-800 text-lg flex items-center gap-2">
            <Book size={18} className="text-[var(--accent)]" />
            Configuración de Portada
          </h2>
          <button onClick={toggleSettings} className="p-2 hover:bg-gray-100 rounded-full transition-colors text-gray-500">
            <X size={20} />
          </button>
        </div>

        {/* Scrollable body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-8">

          {/* Toggle */}
          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-xl border border-gray-100">
            <div>
              <p className="font-semibold text-gray-800 text-sm">Incluir página de portada</p>
              <p className="text-xs text-gray-500 mt-0.5">Se agregará como la primera hoja del PDF.</p>
            </div>
            <button
              onClick={() => up('showCover', !config.showCover)}
              className={`w-12 h-6 rounded-full transition-colors relative ${config.showCover ? 'bg-[var(--accent)]' : 'bg-gray-300'}`}
            >
              <div className={`w-5 h-5 bg-white rounded-full absolute top-0.5 transition-transform ${config.showCover ? 'translate-x-6' : 'translate-x-0.5'}`} />
            </button>
          </div>

          <div className={`space-y-8 transition-opacity duration-300 ${!config.showCover ? 'opacity-40 pointer-events-none' : ''}`}>

            {/* Estilo */}
            <div className="space-y-3">
              <label className="text-xs font-bold text-gray-500 uppercase tracking-wider">Estilo de Portada</label>
              <div className="grid grid-cols-3 gap-3">

                {/* FCyT UADER */}
                <StyleCard
                  label="FCyT UADER"
                  selected={config.coverStyle === 'fcyt_uader'}
                  onClick={() => up('coverStyle', 'fcyt_uader')}
                  preview={
                    <div className="w-full h-full flex flex-col p-2 bg-white">
                      <div className="flex items-center gap-1.5 mb-2">
                        <img src="/LogoUADER.png" alt="" className="h-7 w-auto object-contain" />
                        <div className="w-px h-7 bg-gray-300" />
                        <div>
                          <div className="text-[8px] font-bold text-gray-700 leading-tight">FCyT</div>
                          <div className="text-[6px] text-gray-500 leading-tight">Sede Concepción</div>
                        </div>
                      </div>
                      <div className="flex-1 flex flex-col items-center justify-center gap-1 text-center">
                        <div className="text-[6px] font-bold text-gray-800 uppercase">Trabajo Final</div>
                        <div className="text-[5px] text-gray-500">Materia</div>
                        <div className="text-[5px] font-bold text-gray-800 uppercase">Integrantes</div>
                        <div className="text-[5px] text-gray-500">Juan García</div>
                      </div>
                      <div className="h-px bg-gray-300 mt-2" />
                    </div>
                  }
                />

                {/* Clásica Azul */}
                <StyleCard
                  label="Clásica Azul"
                  selected={config.coverStyle === 'barra_azul'}
                  onClick={() => up('coverStyle', 'barra_azul')}
                  preview={
                    <div className="w-full h-full flex bg-gray-50">
                      <div className="w-1/4 h-full bg-[#265e8a] flex flex-col items-center py-2">
                        <div className="w-4 h-4 bg-white/30 rounded-full" />
                      </div>
                      <div className="flex-1 p-2 flex flex-col justify-center">
                        <div className="w-8 h-1 bg-gray-300 rounded mb-2" />
                        <div className="w-16 h-2 bg-gray-800 rounded mb-1" />
                        <div className="w-12 h-1 bg-gray-400 rounded" />
                      </div>
                    </div>
                  }
                />

                {/* Blanca Simple */}
                <StyleCard
                  label="Blanca Simple"
                  selected={config.coverStyle === 'blanca_simple'}
                  onClick={() => up('coverStyle', 'blanca_simple')}
                  preview={
                    <div className="w-full h-full bg-white flex flex-col items-center justify-center p-3 gap-1">
                      <div className="w-4 h-4 bg-gray-200 rounded-full" />
                      <div className="w-10 h-1 bg-gray-300 rounded" />
                      <div className="w-20 h-2 bg-gray-800 rounded" />
                      <div className="w-14 h-1 bg-gray-400 rounded" />
                    </div>
                  }
                />
              </div>
            </div>

            {/* Datos del documento */}
            <div className="space-y-4">
              <label className="text-xs font-bold text-gray-500 uppercase tracking-wider">Datos del Documento</label>

              <Field label="Título principal (ej: Trabajo Integrador Final)">
                <input type="text" value={config.title} onChange={(e) => up('title', e.target.value)} className={inputCls} placeholder="Trabajo Integrador Final" />
              </Field>

              <Field label="Subtítulo / Descripción (ej: Análisis de Sistemas)">
                <input type="text" value={config.subtitle} onChange={(e) => up('subtitle', e.target.value)} className={inputCls} placeholder="Análisis de Sistemas" />
              </Field>

              <Field label="Cátedra / Materia">
                <input type="text" value={config.materia} onChange={(e) => up('materia', e.target.value)} className={inputCls} placeholder="Taller de Integración" />
              </Field>

              <div className="grid grid-cols-2 gap-3">
                <Field label="Sigla (encabezado)">
                  <input
                    type="text"
                    value={config.sigla ?? ''}
                    onChange={(e) => up('sigla', e.target.value)}
                    className={inputCls}
                    placeholder="TI"
                    maxLength={8}
                  />
                </Field>
                <Field label="Fecha">
                  <input
                    type="text"
                    value={config.fecha ?? today}
                    onChange={(e) => up('fecha', e.target.value)}
                    className={inputCls}
                    placeholder={today}
                  />
                </Field>
              </div>
            </div>

            {/* Integrantes */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <label className="text-xs font-bold text-gray-500 uppercase tracking-wider flex items-center gap-1.5">
                  <Users size={13} /> Integrantes
                </label>
                <button onClick={() => addArr('integrantes')} className="text-xs font-medium text-[var(--accent)] hover:underline">+ Agregar</button>
              </div>
              <div className="space-y-2">
                {config.integrantes.map((v, i) => (
                  <div key={i} className="flex items-center gap-2">
                    <input type="text" value={v} onChange={(e) => updateArr('integrantes', i, e.target.value)} className={inputCls} placeholder="Nombre del integrante" />
                    <button onClick={() => delArr('integrantes', i)} className="text-gray-400 hover:text-red-500 p-1 shrink-0"><X size={15} /></button>
                  </div>
                ))}
              </div>
            </div>

            {/* Profesores */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <label className="text-xs font-bold text-gray-500 uppercase tracking-wider flex items-center gap-1.5">
                  <GraduationCap size={13} /> Equipo Docente
                </label>
                <button onClick={() => addArr('profesores')} className="text-xs font-medium text-[var(--accent)] hover:underline">+ Agregar</button>
              </div>
              <div className="space-y-2">
                {config.profesores.map((v, i) => (
                  <div key={i} className="flex items-center gap-2">
                    <input type="text" value={v} onChange={(e) => updateArr('profesores', i, e.target.value)} className={inputCls} placeholder="Nombre del docente" />
                    <button onClick={() => delArr('profesores', i)} className="text-gray-400 hover:text-red-500 p-1 shrink-0"><X size={15} /></button>
                  </div>
                ))}
              </div>
            </div>

          </div>
        </div>
      </motion.div>
    </AnimatePresence>
  );
}
