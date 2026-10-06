'use client';

import React, { useEffect, useRef, useState } from 'react';
import { CoverRenderer } from './covers/CoverRenderer';
import { useEditorStore } from '@/store/editor-store';

export function Paginator({ children }: { children: React.ReactNode }) {
  const measureRef = useRef<HTMLDivElement>(null);
  const [pages, setPages] = useState<string[]>([]);
  const coverConfig = useEditorStore((s) => s.coverConfig);

  const hasCover  = !!(coverConfig?.showCover);
  const sigla     = coverConfig?.sigla?.trim() || '';
  const docTitle  = coverConfig?.title?.trim() || '';
  const totalPages = pages.length + (hasCover ? 1 : 0);

  useEffect(() => {
    if (!measureRef.current) return;
    
    const renderHeader = coverConfig?.showHeader !== false && (sigla || docTitle);
    const renderFooter = coverConfig?.showFooter !== false;
    
    const topMargin = renderHeader ? 30 : 20;
    const bottomMargin = renderFooter ? 30 : 20;
    const availableHeight = 297 - topMargin - bottomMargin;

    const ruler = document.createElement('div');
    ruler.style.height = `${availableHeight}mm`;
    ruler.style.position = 'absolute';
    ruler.style.visibility = 'hidden';
    document.body.appendChild(ruler);
    const MAX_HEIGHT = ruler.getBoundingClientRect().height;
    document.body.removeChild(ruler);

    const elements = Array.from(measureRef.current.children);
    const newPages: string[] = [];
    let currentPageHtml = '';
    let currentHeight   = 0;

    elements.forEach(el => {
      const isPageBreak = el.classList.contains('page-break');
      if (isPageBreak) {
        newPages.push(currentPageHtml);
        currentPageHtml = '';
        currentHeight   = 0;
        return;
      }
      const rect        = el.getBoundingClientRect();
      const style       = window.getComputedStyle(el);
      const marginTop   = parseFloat(style.marginTop)    || 0;
      const marginBottom= parseFloat(style.marginBottom) || 0;
      const elHeight    = rect.height + marginTop + marginBottom;

      if (currentHeight + elHeight > MAX_HEIGHT && currentHeight > 0) {
        newPages.push(currentPageHtml);
        currentPageHtml = el.outerHTML;
        currentHeight   = elHeight;
      } else {
        currentPageHtml += el.outerHTML;
        currentHeight   += elHeight;
      }
    });

    if (currentPageHtml.trim() !== '') newPages.push(currentPageHtml);
    if (newPages.length === 0)         newPages.push('');
    setPages(newPages);

    setTimeout(() => {
      if (measureRef.current) {
        measureRef.current.parentElement?.classList.add('print-ready');
      }
    }, 100);
  }, [children]);

  return (
    <div className="flex flex-col items-center gap-12 print:block print:gap-0 w-full" id="paginator-root">
      {/* Contenedor de medición (oculto) */}
      <div
        className="measurement-container"
        style={{ position: 'absolute', visibility: 'hidden', pointerEvents: 'none', width: '210mm', padding: '20mm', zIndex: -1000 }}
      >
        <div className="preview-content" ref={measureRef}>
          {children}
        </div>
      </div>

      {/* Portada */}
      <CoverRenderer />

      {/* Pginas A4 */}
      {pages.map((pageHtml, index) => {
        const pageNumber = index + 1; // Content pages start at 1
        const totalContentPages = pages.length;
        const renderHeader = coverConfig?.showHeader !== false && (sigla || docTitle);
        const renderFooter = coverConfig?.showFooter !== false;

        return (
          <div
            key={index}
            className="a4-page bg-white shadow-md print:shadow-none border border-[#E5E5E5] print:border-none relative overflow-hidden shrink-0 print:m-0"
            style={{
              width: '210mm',
              height: '297mm',
              backgroundColor: '#ffffff',
              pageBreakAfter: index === pages.length - 1 ? 'auto' : 'always',
              breakAfter:     index === pages.length - 1 ? 'auto' : 'page',
            }}
          >
            {/* Header */}
            {renderHeader && (
              <div
                style={{
                  position: 'absolute',
                  top: '14mm',
                  left: '20mm',
                  right: '20mm',
                }}
              >
                {/* Texto */}
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'baseline',
                  fontSize: '9pt',
                  color: '#333',
                  fontFamily: 'Arial, Helvetica, sans-serif',
                  marginBottom: '3mm'
                }}>
                  <div>
                    {sigla && <strong>{sigla}</strong>}
                    {sigla && docTitle && ' - '}
                    {docTitle}
                  </div>
                </div>
                {/* Línea abajo del texto */}
                <div style={{ height: '1px', backgroundColor: '#c0c0c0' }} />
              </div>
            )}

            {/* Contenido */}
            <div
              className="preview-content"
              style={{
                position: 'absolute',
                top:    renderHeader ? '30mm' : '20mm',
                left:   '20mm',
                right:  '20mm',
                bottom: renderFooter ? '30mm' : '20mm',
                overflow: 'hidden',
                fontFamily: "'Inter', sans-serif",
                color: '#2d2d2d',
                lineHeight: '1.6',
                fontSize: '11pt',
              }}
              dangerouslySetInnerHTML={{ __html: pageHtml }}
            />

            {/* Footer */}
            {renderFooter && (
              <div
                style={{
                  position: 'absolute',
                  bottom: '14mm',
                  left: '20mm',
                  right: '20mm',
                }}
              >
                {/* Línea arriba del texto */}
                <div style={{ height: '1px', backgroundColor: '#c0c0c0', marginBottom: '3mm' }} />
                {/* Texto */}
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'baseline',
                  fontSize: '9pt',
                  color: '#333',
                  fontFamily: 'Arial, Helvetica, sans-serif',
                }}>
                  <div>
                    {sigla && <strong>{sigla}</strong>}
                    {sigla && docTitle && ' - '}
                    {docTitle}
                  </div>
                  <div>
                    <strong>Página {pageNumber} de {totalContentPages}</strong>
                  </div>
                </div>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
