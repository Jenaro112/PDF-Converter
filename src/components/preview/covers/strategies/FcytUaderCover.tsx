import React from 'react';
import type { CoverData } from '@/store/editor-store';

export function FcytUaderCover({ config }: { config: CoverData }) {
  const today = new Date().toLocaleDateString('es-AR', {
    day: '2-digit', month: '2-digit', year: 'numeric',
  });
  const fecha = config.fecha || today;

  return (
    <div
      className="a4-page bg-white shadow-md print:shadow-none border border-[var(--border)] print:border-none shrink-0 print:m-0 flex flex-col"
      style={{
        width: '210mm',
        height: '297mm',
        backgroundColor: '#ffffff',
        fontFamily: 'Arial, Helvetica, sans-serif',
        pageBreakAfter: 'always',
        breakAfter: 'page',
      }}
    >
      {/* ── Logo header ───────────────────────────────────────────── */}
      <div style={{ padding: '22mm 22mm 0' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          {/* Logo UADER */}
          <img
            src="/LogoUADER.png"
            alt="Logo UADER"
            style={{ height: '60px', width: 'auto', objectFit: 'contain' }}
          />

          {/* Separador vertical */}
          <div style={{ width: '1px', height: '60px', backgroundColor: '#aaa', flexShrink: 0 }} />

          {/* Texto FCyT */}
          <div style={{ lineHeight: 1.25 }}>
            <div style={{ fontSize: '34px', fontWeight: 700, color: '#333', letterSpacing: '-0.5px' }}>FCyT</div>
            <div style={{ fontSize: '13px', color: '#555' }}>Sede Concepción</div>
            <div style={{ fontSize: '13px', color: '#555' }}>del Uruguay</div>
          </div>
        </div>
      </div>

      {/* ── Bloques de datos centrados ────────────────────────────── */}
      <div
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          textAlign: 'center',
          padding: '0 30mm',
          gap: '26px',
        }}
      >
        {/* Título / tipo de trabajo */}
        <div>
          <div style={{ fontWeight: 700, fontSize: '13px', color: '#1a1a1a', textTransform: 'uppercase', letterSpacing: '0.03em' }}>
            {config.title}
          </div>
          {config.subtitle && (
            <div style={{ fontSize: '12px', color: '#333', marginTop: '6px' }}>{config.subtitle}</div>
          )}
        </div>

        {/* Integrantes */}
        {config.integrantes.filter(Boolean).length > 0 && (
          <div>
            <div style={{ fontWeight: 700, fontSize: '13px', color: '#1a1a1a', textTransform: 'uppercase', letterSpacing: '0.03em' }}>
              Integrantes del Equipo
            </div>
            <div style={{ marginTop: '6px', display: 'flex', flexDirection: 'column', gap: '3px' }}>
              {config.integrantes.filter(Boolean).map((name) => (
                <div key={name} style={{ fontSize: '12px', color: '#333' }}>{name}</div>
              ))}
            </div>
          </div>
        )}

        {/* Cátedra */}
        {config.materia && (
          <div>
            <div style={{ fontWeight: 700, fontSize: '13px', color: '#1a1a1a', textTransform: 'uppercase', letterSpacing: '0.03em' }}>
              Cátedra
            </div>
            <div style={{ fontSize: '12px', color: '#333', marginTop: '6px' }}>{config.materia}</div>
          </div>
        )}

        {/* Equipo Docente */}
        {config.profesores.filter(Boolean).length > 0 && (
          <div>
            <div style={{ fontWeight: 700, fontSize: '13px', color: '#1a1a1a', textTransform: 'uppercase', letterSpacing: '0.03em' }}>
              Equipo Docente
            </div>
            <div style={{ marginTop: '6px', display: 'flex', flexDirection: 'column', gap: '3px' }}>
              {config.profesores.filter(Boolean).map((name) => (
                <div key={name} style={{ fontSize: '12px', color: '#333' }}>{name}</div>
              ))}
            </div>
          </div>
        )}

        {/* Fecha */}
        <div>
          <div style={{ fontWeight: 700, fontSize: '13px', color: '#1a1a1a', textTransform: 'uppercase', letterSpacing: '0.03em' }}>
            Fecha
          </div>
          <div style={{ fontSize: '12px', color: '#333', marginTop: '6px' }}>{fecha}</div>
        </div>
      </div>

      {/* ── Línea al pie ──────────────────────────────────────────── */}
      <div style={{ padding: '0 22mm 14mm' }}>
        <div style={{ height: '1px', backgroundColor: '#ccc' }} />
      </div>
    </div>
  );
}
