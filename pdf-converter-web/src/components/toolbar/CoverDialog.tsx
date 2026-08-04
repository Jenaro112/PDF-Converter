'use client';

import React, { useState } from 'react';
import { useEditorStore } from '@/store/editor-store';
import { type CoverConfig, type CoverStyle } from '@/lib/covers';
import '@/styles/cover-dialog.css';

interface CoverDialogProps {
  isOpen: boolean;
  onClose: () => void;
}

export function CoverDialog({ isOpen, onClose }: CoverDialogProps) {
  const coverConfig = useEditorStore((s) => s.coverConfig);
  const showCover = useEditorStore((s) => s.showCover);
  const setCoverConfig = useEditorStore((s) => s.setCoverConfig);
  const setShowCover = useEditorStore((s) => s.setShowCover);

  const [enabled, setEnabled] = useState<boolean>(showCover);
  const [title, setTitle] = useState<string>(coverConfig?.title || 'Informe Técnico');
  const [subtitle, setSubtitle] = useState<string>(coverConfig?.subtitle || 'Arquitectura y Gestión de Memoria');
  const [materia, setMateria] = useState<string>(coverConfig?.materia || 'Sistemas Operativos');
  const [integrantes, setIntegrantes] = useState<string>(coverConfig?.integrantes || 'Juan Pérez, María Gómez');
  const [profesores, setProfesores] = useState<string>(coverConfig?.profesores || 'Prof. Dr. Carlos Rodríguez');
  const [showLogo, setShowLogo] = useState<boolean>(coverConfig?.showLogo ?? true);
  const [logoPosition, setLogoPosition] = useState<'left' | 'center' | 'right'>(
    coverConfig?.logoPosition || 'center'
  );
  const [coverStyle, setCoverStyle] = useState<CoverStyle>(
    coverConfig?.coverStyle || 'classic'
  );

  if (!isOpen) return null;

  const handleSave = () => {
    const config: CoverConfig = {
      title,
      subtitle,
      materia,
      integrantes,
      profesores,
      showLogo,
      logoPosition,
      coverStyle,
    };
    setCoverConfig(config);
    setShowCover(enabled);
    onClose();
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="modal-title">
            <span>📖</span> Configuración de Portada
          </h2>
          <button className="modal-close-btn" onClick={onClose} title="Cerrar">
            ✕
          </button>
        </div>

        <div className="modal-body">
          {/* Enable Switch */}
          <label className="toggle-row">
            <div>
              <div style={{ fontWeight: 700, fontSize: '0.95rem' }}>Habilitar Portada</div>
              <div style={{ fontSize: '0.8rem', color: '#94a3b8' }}>
                Genera una página de carátula al inicio del documento
              </div>
            </div>
            <div className="switch">
              <input
                type="checkbox"
                checked={enabled}
                onChange={(e) => setEnabled(e.target.checked)}
              />
              <span className="slider" />
            </div>
          </label>

          {/* Cover Style Selector */}
          <div className="modal-section">
            <div className="modal-section-title">Estilo de Carátula</div>
            <div className="style-grid">
              <button
                type="button"
                className={`style-card ${coverStyle === 'classic' ? 'active' : ''}`}
                onClick={() => setCoverStyle('classic')}
              >
                <span className="style-card-icon">📜</span>
                <span>Clásica Centrada</span>
              </button>

              <button
                type="button"
                className={`style-card ${coverStyle === 'sidebar' ? 'active' : ''}`}
                onClick={() => setCoverStyle('sidebar')}
              >
                <span className="style-card-icon">📰</span>
                <span>Franja Lateral</span>
              </button>

              <button
                type="button"
                className={`style-card ${coverStyle === 'minimal' ? 'active' : ''}`}
                onClick={() => setCoverStyle('minimal')}
              >
                <span className="style-card-icon">✒️</span>
                <span>Minimalista</span>
              </button>

              <button
                type="button"
                className={`style-card ${coverStyle === 'technical' ? 'active' : ''}`}
                onClick={() => setCoverStyle('technical')}
              >
                <span className="style-card-icon">📐</span>
                <span>Ficha Técnica</span>
              </button>
            </div>
          </div>

          {/* Form Fields */}
          <div className="modal-section">
            <div className="modal-section-title">Información del Documento</div>

            <div className="form-group">
              <label>Título Principal</label>
              <input
                type="text"
                className="form-input"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="ej. Informe de Proyecto"
              />
            </div>

            <div className="form-group">
              <label>Subtítulo / Descripción Corta</label>
              <input
                type="text"
                className="form-input"
                value={subtitle}
                onChange={(e) => setSubtitle(e.target.value)}
                placeholder="ej. Análisis de Resultados"
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Materia / Asignatura</label>
                <input
                  type="text"
                  className="form-input"
                  value={materia}
                  onChange={(e) => setMateria(e.target.value)}
                  placeholder="ej. Sistemas Operativos"
                />
              </div>

              <div className="form-group">
                <label>Profesores / Docentes</label>
                <input
                  type="text"
                  className="form-input"
                  value={profesores}
                  onChange={(e) => setProfesores(e.target.value)}
                  placeholder="ej. Prof. Carlos Rodríguez"
                />
              </div>
            </div>

            <div className="form-group">
              <label>Integrantes / Autores</label>
              <input
                type="text"
                className="form-input"
                value={integrantes}
                onChange={(e) => setIntegrantes(e.target.value)}
                placeholder="ej. Juan Pérez, María Gómez"
              />
            </div>
          </div>

          {/* Logo Options */}
          <div className="modal-section">
            <div className="modal-section-title">Logo Institucional</div>
            <div className="form-row">
              <label className="toggle-row" style={{ margin: 0 }}>
                <span style={{ fontSize: '0.88rem', fontWeight: 600 }}>Mostrar Logo</span>
                <div className="switch">
                  <input
                    type="checkbox"
                    checked={showLogo}
                    onChange={(e) => setShowLogo(e.target.checked)}
                  />
                  <span className="slider" />
                </div>
              </label>

              <div className="form-group">
                <label>Posición del Logo</label>
                <select
                  className="form-input"
                  value={logoPosition}
                  onChange={(e) => setLogoPosition(e.target.value as any)}
                >
                  <option value="left">Izquierda</option>
                  <option value="center">Centro</option>
                  <option value="right">Derecha</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <div className="modal-footer">
          <button className="btn-secondary" onClick={onClose}>
            Cancelar
          </button>
          <button className="btn-primary" onClick={handleSave}>
            Guardar Portada
          </button>
        </div>
      </div>
    </div>
  );
}
