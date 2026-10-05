'use client';
import React from 'react';
import { useEditorStore } from '@/store/editor-store';
import { X, Book, Users, GraduationCap } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

// ─── Tiny helper ─────────────────────────────────────────────────────────────
function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div>
      <label className="block text-xs text-[var(--text-muted)] mb-1.5 font-medium">{label}</label>
      {children}
    </div>
  );
}

const inputCls =
  'w-full border border-[var(--border)] rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[var(--accent)] focus:ring-1 focus:ring-[var(--accent)]/30 transition-all bg-[var(--bg-surface)]';

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
        selected ? 'border-[var(--accent)] ring-2 ring-[var(--accent)]/20' : 'border-[var(--border)] hover:border-[var(--border)]'
      }`}
    >
      <div className="h-24 bg-[var(--bg-sidebar)] flex items-center justify-center overflow-hidden">{preview}</div>
      <div className="p-3 bg-[var(--bg-surface)] border-t border-[var(--border)]">
        <p className="text-sm font-semibold text-[var(--text-main)]">{label}</p>
      </div>
    </button>
  );
}

// ─── Main component ───────────────────────────────────────────────────────────
export function CoverSettingsDrawer() {
  const { isSettingsOpen, toggleSettings, coverConfig, setCover } = useEditorStore();

  const today = new Date().toLocaleDateString('es-AR', {
    day: '2-digit', month: '2-digit', year: 'numeric',
  });

  const config = coverConfig || {
    showCover:  false,
    title:      '',
    subtitle:   '',
    materia:    '',
    coverStyle: 'academic_elegant' as const,
    showLogo:   true,
    integrantes: [''],
    profesores:  [''],
    sigla:       '',
    fecha:       today,
    showHeader:  true,
    showFooter:  true,
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
      {isSettingsOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.3 }}
            onClick={toggleSettings}
            className="fixed inset-0 z-[90] pointer-events-auto"
            style={{ background: 'rgba(30,20,15,0.18)', backdropFilter: 'blur(1px)' }}
          />

          <motion.div
            initial={{ opacity: 0, x: 400 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 400 }}
            transition={{ duration: 0.5, ease: [0.32, 0.72, 0, 1] }}
            className="fixed top-0 right-0 bottom-0 w-[450px] bg-[var(--bg-surface)] shadow-2xl border-l border-[var(--border)] z-[100] flex flex-col overflow-hidden"
          >
            {/* Header */}
            <div className="h-16 border-b border-[var(--border)] flex items-center justify-between px-6 shrink-0 bg-[var(--bg-sidebar)]/50 backdrop-blur-md">
              <h2 className="font-bold text-[var(--text-main)] text-lg flex items-center gap-2 tracking-tight">
                <Book size={18} className="text-[var(--accent)]" />
                Configuración de Portada
              </h2>
              <button onClick={toggleSettings} className="p-2 hover:bg-gray-200 rounded-full transition-colors text-[var(--text-muted)] hover:text-[var(--text-main)] outline-none">
                <X size={20} />
              </button>
            </div>

            {/* Scrollable body */}
            <div className="flex-1 overflow-y-auto p-6 space-y-8">

              {/* Toggles */}
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-[var(--bg-sidebar)] rounded-xl border border-[var(--border)] shadow-sm">
                  <div>
                    <p className="font-semibold text-[var(--text-main)] text-sm">Incluir página de portada</p>
                    <p className="text-xs text-[var(--text-muted)] mt-0.5">Se agregará como la primera hoja del PDF.</p>
                  </div>
                  <button
                    onClick={() => up('showCover', !config.showCover)}
                    className={`w-12 h-6 rounded-full transition-colors relative shadow-inner ${config.showCover ? 'bg-[var(--accent)]' : 'bg-gray-300'}`}
                  >
                    <motion.div 
                      layout
                      transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                      className={`w-5 h-5 bg-[var(--bg-surface)] rounded-full absolute top-0.5 shadow-sm ${config.showCover ? 'left-6' : 'left-0.5'}`} 
                    />
                  </button>
                </div>

                <div className="flex items-center justify-between p-4 bg-[var(--bg-sidebar)] rounded-xl border border-[var(--border)] shadow-sm">
                  <div>
                    <p className="font-semibold text-[var(--text-main)] text-sm">Mostrar logo de la Facultad</p>
                    <p className="text-xs text-[var(--text-muted)] mt-0.5">Aplica a las portadas que lo soporten.</p>
                  </div>
                  <button
                    onClick={() => up('showLogo', config.showLogo === false ? true : false)}
                    className={`w-12 h-6 rounded-full transition-colors relative shadow-inner ${config.showLogo !== false ? 'bg-[var(--accent)]' : 'bg-gray-300'}`}
                  >
                    <motion.div 
                      layout
                      transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                      className={`w-5 h-5 bg-[var(--bg-surface)] rounded-full absolute top-0.5 shadow-sm ${config.showLogo !== false ? 'left-6' : 'left-0.5'}`} 
                    />
                  </button>
                </div>
              </div>

              <div className="space-y-4">
                <label className="text-xs font-bold text-[var(--text-muted)] uppercase tracking-wider">Opciones de Página</label>
                <div className="flex items-center justify-between p-4 bg-[var(--bg-sidebar)] rounded-xl border border-[var(--border)] shadow-sm">
                  <div>
                    <p className="font-semibold text-[var(--text-main)] text-sm">Encabezado</p>
                    <p className="text-xs text-[var(--text-muted)] mt-0.5">Muestra la sigla en la parte superior.</p>
                  </div>
                  <button
                    onClick={() => up('showHeader', config.showHeader === false ? true : false)}
                    className={`w-12 h-6 rounded-full transition-colors relative shadow-inner ${config.showHeader !== false ? 'bg-[var(--accent)]' : 'bg-gray-300'}`}
                  >
                    <motion.div 
                      layout
                      transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                      className={`w-5 h-5 bg-[var(--bg-surface)] rounded-full absolute top-0.5 shadow-sm ${config.showHeader !== false ? 'left-6' : 'left-0.5'}`} 
                    />
                  </button>
                </div>

                <div className="flex items-center justify-between p-4 bg-[var(--bg-sidebar)] rounded-xl border border-[var(--border)] shadow-sm">
                  <div>
                    <p className="font-semibold text-[var(--text-main)] text-sm">Pie de Página</p>
                    <p className="text-xs text-[var(--text-muted)] mt-0.5">Muestra el número de página en la parte inferior.</p>
                  </div>
                  <button
                    onClick={() => up('showFooter', config.showFooter === false ? true : false)}
                    className={`w-12 h-6 rounded-full transition-colors relative shadow-inner ${config.showFooter !== false ? 'bg-[var(--accent)]' : 'bg-gray-300'}`}
                  >
                    <motion.div 
                      layout
                      transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                      className={`w-5 h-5 bg-[var(--bg-surface)] rounded-full absolute top-0.5 shadow-sm ${config.showFooter !== false ? 'left-6' : 'left-0.5'}`} 
                    />
                  </button>
                </div>
              </div>

              <div className={`space-y-8 transition-opacity duration-300 ${!config.showCover ? 'opacity-40 pointer-events-none' : ''}`}>

                {/* Estilo */}
                <div className="space-y-3">
                  <label className="text-xs font-bold text-[var(--text-muted)] uppercase tracking-wider">Estilo de Portada</label>
                  <div className="grid grid-cols-2 gap-3">

                    {/* Academic Elegant */}
                    <StyleCard
                      label="Académica Elegante"
                      selected={config.coverStyle === 'academic_elegant'}
                      onClick={() => up('coverStyle', 'academic_elegant')}
                      preview={
                        <div className="w-full h-full bg-[#fdfbf7] flex flex-col items-center justify-center p-2 text-center border border-[var(--border)]">
                          <div className="w-4 h-4 rounded-full border border-gray-800 mb-2" />
                          <div className="w-16 h-2 bg-gray-800 mb-1" />
                          <div className="w-12 h-1 bg-[var(--bg-sidebar)]0 mb-3" />
                          <div className="w-8 h-px bg-gray-400 mb-2" />
                          <div className="w-10 h-1 bg-gray-400" />
                        </div>
                      }
                    />

                    {/* Modern Minimal */}
                    <StyleCard
                      label="Minimalista Moderna"
                      selected={config.coverStyle === 'modern_minimal'}
                      onClick={() => up('coverStyle', 'modern_minimal')}
                      preview={
                        <div className="w-full h-full bg-[var(--bg-surface)] flex flex-col items-start justify-end p-3 border border-[var(--border)]">
                          <div className="w-6 h-6 bg-gray-100 rounded-lg absolute top-2 right-2" />
                          <div className="w-20 h-3 bg-gray-900 mb-1" />
                          <div className="w-14 h-1 bg-gray-400 mb-4" />
                          <div className="w-10 h-1 bg-gray-300" />
                        </div>
                      }
                    />

                    {/* Geometric Corporate */}
                    <StyleCard
                      label="Técnica / Geométrica"
                      selected={config.coverStyle === 'geometric_corporate'}
                      onClick={() => up('coverStyle', 'geometric_corporate')}
                      preview={
                        <div className="w-full h-full bg-[var(--bg-surface)] flex border border-[var(--border)] relative overflow-hidden">
                          <div className="w-3 h-full bg-blue-900/10 absolute left-0 top-0" />
                          <div className="ml-4 p-2 flex flex-col justify-center w-full">
                            <div className="w-16 h-2 bg-gray-800 mb-1" />
                            <div className="w-12 h-1 bg-[var(--bg-sidebar)]0 mb-3" />
                            <div className="w-full h-8 bg-[var(--bg-sidebar)] mt-2 flex flex-col gap-1 p-1">
                              <div className="w-8 h-1 bg-gray-300" />
                              <div className="w-12 h-1 bg-gray-400" />
                            </div>
                          </div>
                        </div>
                      }
                    />

                    {/* FCyT UADER */}
                    <StyleCard
                      label="FCyT Clásica"
                      selected={config.coverStyle === 'fcyt_uader'}
                      onClick={() => up('coverStyle', 'fcyt_uader')}
                      preview={
                        <div className="w-full h-full flex flex-col p-2 bg-[var(--bg-surface)] border border-[var(--border)]">
                          <div className="flex items-center gap-1 mb-2">
                            <div className="w-4 h-4 bg-blue-100 rounded" />
                            <div className="w-px h-4 bg-gray-300" />
                            <div className="w-8 h-2 bg-gray-400" />
                          </div>
                          <div className="flex-1 flex flex-col items-center justify-center gap-1">
                            <div className="w-14 h-1.5 bg-gray-800" />
                            <div className="w-10 h-1 bg-gray-400" />
                          </div>
                        </div>
                      }
                    />

                  </div>
                </div>

                {/* Datos del documento */}
                <div className="space-y-4">
                  <label className="text-xs font-bold text-[var(--text-muted)] uppercase tracking-wider">Datos del Documento</label>

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
                    <label className="text-xs font-bold text-[var(--text-muted)] uppercase tracking-wider flex items-center gap-1.5">
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
                    <label className="text-xs font-bold text-[var(--text-muted)] uppercase tracking-wider flex items-center gap-1.5">
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
        </>
      )}
    </AnimatePresence>
  );
}
