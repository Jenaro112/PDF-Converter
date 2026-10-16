'use client';

import React, { useEffect, useRef, useState } from 'react';
import { CoverRenderer } from './covers/CoverRenderer';
import { useEditorStore } from '@/store/editor-store';

function resolveTemplate(
  template: any,
  vars: {
    pageNumber: number;
    totalPages: number;
    title: string;
    sigla: string;
    materia: string;
    fecha: string;
  }
): string {
  if (template === undefined || template === null) return '';
  let res = String(template)
    .replace(/\{pagina\}|\{page\}/gi, String(vars.pageNumber))
    .replace(/\{total\}|\{totalpages\}|\{n\}/gi, String(vars.totalPages))
    .replace(/\{titulo\}|\{title\}/gi, vars.title)
    .replace(/\{sigla\}/gi, vars.sigla)
    .replace(/\{materia\}/gi, vars.materia)
    .replace(/\{fecha\}|\{date\}/gi, vars.fecha);

  res = res.replace(/^\s*[-–—]\s*/, '').replace(/\s*[-–—]\s*$/, '').trim();
  return res;
}

function getNumberingString(
  format: string | undefined,
  pageNumber: number,
  totalPages: number
): string {
  switch (format) {
    case 'x_de_y':
      return `${pageNumber} / ${totalPages}`;
    case 'pagina_x':
      return `Página ${pageNumber}`;
    case 'guiones':
      return `- ${pageNumber} -`;
    case 'solo_numero':
      return `${pageNumber}`;
    case 'ninguno':
      return '';
    case 'pagina_x_de_y':
    default:
      return `Página ${pageNumber} de ${totalPages}`;
  }
}

export function Paginator({ children }: { children: React.ReactNode }) {
  const measureRef = useRef<HTMLDivElement>(null);
  const [pages, setPages] = useState<string[]>([]);
  const coverConfig = useEditorStore((s) => s.coverConfig);

  const hasCover  = !!(coverConfig?.showCover);
  const sigla     = coverConfig?.sigla != null ? String(coverConfig.sigla).trim() : '';
  const docTitle  = coverConfig?.title != null ? String(coverConfig.title).trim() : '';
  const materia   = coverConfig?.materia != null ? String(coverConfig.materia).trim() : '';
  const fecha     = coverConfig?.fecha != null ? String(coverConfig.fecha).trim() : '';

  useEffect(() => {
    let isCancelled = false;

    const paginate = () => {
      if (isCancelled || !measureRef.current) return;
      
      const renderHeader = coverConfig?.showHeader !== false;
      const renderFooter = coverConfig?.showFooter !== false;
      
      const topMargin = renderHeader ? 24 : 16;
      const bottomMargin = renderFooter ? 24 : 16;
      const availableHeight = 297 - topMargin - bottomMargin;

      const ruler = document.createElement('div');
      ruler.style.height = `${availableHeight}mm`;
      ruler.style.position = 'absolute';
      ruler.style.visibility = 'hidden';
      document.body.appendChild(ruler);
      // Margen de seguridad de 6px para evitar cortes por redondeo subpíxel
      const MAX_HEIGHT = ruler.getBoundingClientRect().height - 6;
      document.body.removeChild(ruler);

      const elements = Array.from(measureRef.current.children);
      const newPages: string[] = [];
      let currentPageHtml = '';
      let currentHeight   = 0;

      interface PageItem {
        el: Element;
        html: string;
        height: number;
      }
      let currentPageElements: PageItem[] = [];

      const isHeading = (el: Element) => /^H[1-6]$/i.test(el.tagName);

      // Evita cadenas de encabezados o encabezados con breve texto introductorio huérfanos al pie de página
      const getTrailingOrphanChain = (): { orphanHtml: string; orphanHeight: number; count: number } | null => {
        const len = currentPageElements.length;
        if (len === 0) return null;

        let idx = len - 1;
        let count = 0;
        let hasHeading = false;

        // Recorrer hacia atrás acumulando encabezados y sus párrafos introductorios asociados
        while (idx >= 0) {
          const item = currentPageElements[idx];
          if (isHeading(item.el)) {
            hasHeading = true;
            idx--;
            count++;
          } else if (item.el.tagName === 'P' && item.height < 140) {
            // Incluir párrafo corto si está precedido inmediatamente por un encabezado o si ya hay un encabezado posterior
            if (idx > 0 && isHeading(currentPageElements[idx - 1].el)) {
              idx--;
              count++;
            } else if (hasHeading) {
              idx--;
              count++;
            } else if (count === 0) {
              idx--;
              count++;
            } else {
              break;
            }
          } else {
            break;
          }
        }

        // Si no encontramos ningún encabezado, o si toda la página son solo estos elementos
        if (!hasHeading || count >= len) {
          return null;
        }

        const orphanItems = currentPageElements.slice(len - count);
        const orphanHtml = orphanItems.map(item => item.html).join('');
        const orphanHeight = orphanItems.reduce((acc, item) => acc + item.height, 0);

        return { orphanHtml, orphanHeight, count };
      };

      elements.forEach(el => {
        const isPageBreak = el.classList.contains('page-break');
        if (isPageBreak) {
          if (currentPageHtml.trim() !== '') newPages.push(currentPageHtml);
          currentPageHtml = '';
          currentHeight   = 0;
          currentPageElements = [];
          return;
        }
        const rect        = el.getBoundingClientRect();
        const style       = window.getComputedStyle(el);
        const marginTop   = parseFloat(style.marginTop)    || 0;
        const marginBottom= parseFloat(style.marginBottom) || 0;
        const elHeight    = rect.height + marginTop + marginBottom;

        // 1. Prevención preventiva de encabezados huérfanos antes de agregarlos si están al borde inferior
        if (isHeading(el) && currentHeight > 0 && currentHeight + elHeight + 60 > MAX_HEIGHT) {
          const orphan = getTrailingOrphanChain();
          if (orphan) {
            currentPageElements = currentPageElements.slice(0, currentPageElements.length - orphan.count);
            const remainingHtml = currentPageElements.map(item => item.html).join('');
            if (remainingHtml.trim() !== '') {
              newPages.push(remainingHtml);
            }
            currentPageHtml = orphan.orphanHtml + el.outerHTML;
            currentHeight = orphan.orphanHeight + elHeight;
            currentPageElements = [
              { el: document.createElement('div'), html: orphan.orphanHtml, height: orphan.orphanHeight },
              { el, html: el.outerHTML, height: elHeight }
            ];
          } else {
            newPages.push(currentPageHtml);
            currentPageHtml = el.outerHTML;
            currentHeight   = elHeight;
            currentPageElements = [{ el, html: el.outerHTML, height: elHeight }];
          }
          return;
        }

        // 2. División inteligente de listas (UL / OL) que desbordan la página
        if ((el.tagName === 'UL' || el.tagName === 'OL') && currentHeight + elHeight > MAX_HEIGHT && el.children.length > 0) {
          const lis = Array.from(el.children);
          const listTag = el.tagName.toLowerCase();
          const listClasses = el.className ? ` class="${el.className}"` : '';
          const listStyle = el.getAttribute('style') ? ` style="${el.getAttribute('style')}"` : '';

          const firstLi = lis[0] as HTMLElement;
          const firstLiStyle = window.getComputedStyle(firstLi);
          const firstLiHeight = firstLi.getBoundingClientRect().height + 
            (parseFloat(firstLiStyle.marginTop) || 0) + 
            (parseFloat(firstLiStyle.marginBottom) || 0);

          // Si no cabe ni el primer ítem, revisar si hay título/intro previo que deba acompañarlo
          if (currentHeight + firstLiHeight > MAX_HEIGHT && currentHeight > 0) {
            const orphan = getTrailingOrphanChain();
            if (orphan) {
              currentPageElements = currentPageElements.slice(0, currentPageElements.length - orphan.count);
              const remainingHtml = currentPageElements.map(item => item.html).join('');
              if (remainingHtml.trim() !== '') {
                newPages.push(remainingHtml);
              }
              currentPageHtml = orphan.orphanHtml;
              currentHeight = orphan.orphanHeight;
              currentPageElements = [
                { el: document.createElement('div'), html: orphan.orphanHtml, height: orphan.orphanHeight }
              ];
            } else {
              newPages.push(currentPageHtml);
              currentPageHtml = '';
              currentHeight = 0;
              currentPageElements = [];
            }
          }

          let currentListHtml = `<${listTag}${listClasses}${listStyle}>`;
          let hasItemsInCurrentList = false;

          lis.forEach((li, liIndex) => {
            const liEl = li as HTMLElement;
            const lStyle = window.getComputedStyle(liEl);
            const liHeight = liEl.getBoundingClientRect().height + 
              (parseFloat(lStyle.marginTop) || 0) + 
              (parseFloat(lStyle.marginBottom) || 0);

            if (currentHeight + liHeight > MAX_HEIGHT && currentHeight > 0) {
              if (hasItemsInCurrentList) {
                currentListHtml += `</${listTag}>`;
                currentPageHtml += currentListHtml;
              }
              newPages.push(currentPageHtml);
              currentPageHtml = '';
              currentHeight = 0;
              currentPageElements = [];
              const startAttr = listTag === 'ol' ? ` start="${liIndex + 1}"` : '';
              currentListHtml = `<${listTag}${listClasses}${listStyle}${startAttr}>`;
              hasItemsInCurrentList = false;
            }

            currentListHtml += li.outerHTML;
            currentHeight += liHeight;
            hasItemsInCurrentList = true;
          });

          if (hasItemsInCurrentList) {
            currentListHtml += `</${listTag}>`;
            currentPageHtml += currentListHtml;
            currentPageElements.push({ el, html: currentListHtml, height: currentHeight });
          }
          return;
        }

        // 3. Manejo de TABLAS: se mantienen enteras si caben, o se dividen fila a fila con repetición de thead
        if (el.tagName === 'TABLE') {
          // Si cabe directamente en la página actual
          if (currentHeight + elHeight <= MAX_HEIGHT) {
            currentPageHtml += el.outerHTML;
            currentHeight += elHeight;
            currentPageElements.push({ el, html: el.outerHTML, height: elHeight });
            return;
          }

          // Si no cabe en la página actual pero hay contenido previo
          if (currentHeight > 0) {
            const orphan = getTrailingOrphanChain();
            if (orphan) {
              currentPageElements = currentPageElements.slice(0, currentPageElements.length - orphan.count);
              const remainingHtml = currentPageElements.map(item => item.html).join('');
              if (remainingHtml.trim() !== '') {
                newPages.push(remainingHtml);
              }
              currentPageHtml = orphan.orphanHtml;
              currentHeight = orphan.orphanHeight;
              currentPageElements = [
                { el: document.createElement('div'), html: orphan.orphanHtml, height: orphan.orphanHeight }
              ];
            } else {
              newPages.push(currentPageHtml);
              currentPageHtml = '';
              currentHeight = 0;
              currentPageElements = [];
            }
          }

          // Si ahora cabe entera en el espacio disponible (en la página nueva con/sin orphan)
          if (currentHeight + elHeight <= MAX_HEIGHT) {
            currentPageHtml += el.outerHTML;
            currentHeight += elHeight;
            currentPageElements.push({ el, html: el.outerHTML, height: elHeight });
            return;
          }

          // Si la tabla excede el espacio restante: división inteligente de filas con repetición de thead
          const thead = el.querySelector('thead');
          const theadHtml = thead ? thead.outerHTML : '';
          const theadHeight = thead ? (thead.getBoundingClientRect().height || 40) : 0;
          const tableClasses = el.className ? ` class="${el.className}"` : '';
          const tableStyle = el.getAttribute('style') ? ` style="${el.getAttribute('style')}"` : '';
          const tableOpenTag = `<table${tableClasses}${tableStyle}>`;

          const rows = Array.from(el.querySelectorAll('tbody > tr'));
          if (rows.length === 0) {
            newPages.push(currentPageHtml);
            currentPageHtml = el.outerHTML;
            currentHeight = elHeight;
            currentPageElements = [{ el, html: el.outerHTML, height: elHeight }];
            return;
          }

          let currentTableHtml = `${tableOpenTag}${theadHtml}<tbody>`;
          let hasRowsInCurrentTable = false;
          currentHeight += theadHeight;

          rows.forEach((tr) => {
            const trEl = tr as HTMLElement;
            const trHeight = trEl.getBoundingClientRect().height || 40;

            if (currentHeight + trHeight > MAX_HEIGHT && currentHeight > theadHeight) {
              if (hasRowsInCurrentTable) {
                currentTableHtml += `</tbody></table>`;
                currentPageHtml += currentTableHtml;
              }
              newPages.push(currentPageHtml);
              currentPageHtml = '';
              currentHeight = theadHeight;
              currentPageElements = [];
              currentTableHtml = `${tableOpenTag}${theadHtml}<tbody>`;
              hasRowsInCurrentTable = false;
            }

            currentTableHtml += tr.outerHTML;
            currentHeight += trHeight;
            hasRowsInCurrentTable = true;
          });

          if (hasRowsInCurrentTable) {
            currentTableHtml += `</tbody></table>`;
            currentPageHtml += currentTableHtml;
            currentPageElements.push({ el, html: currentTableHtml, height: currentHeight });
          }
          return;
        }

        // 4. Elementos estándar (párrafos, pre/código, imágenes, blockquotes, etc.)
        if (currentHeight + elHeight > MAX_HEIGHT && currentHeight > 0) {
          const orphan = getTrailingOrphanChain();
          if (orphan) {
            currentPageElements = currentPageElements.slice(0, currentPageElements.length - orphan.count);
            const remainingHtml = currentPageElements.map(item => item.html).join('');
            if (remainingHtml.trim() !== '') {
              newPages.push(remainingHtml);
            }
            currentPageHtml = orphan.orphanHtml + el.outerHTML;
            currentHeight = orphan.orphanHeight + elHeight;
            currentPageElements = [
              { el: document.createElement('div'), html: orphan.orphanHtml, height: orphan.orphanHeight },
              { el, html: el.outerHTML, height: elHeight }
            ];
          } else {
            newPages.push(currentPageHtml);
            currentPageHtml = el.outerHTML;
            currentHeight = elHeight;
            currentPageElements = [{ el, html: el.outerHTML, height: elHeight }];
          }
        } else {
          currentPageHtml += el.outerHTML;
          currentHeight += elHeight;
          currentPageElements.push({ el, html: el.outerHTML, height: elHeight });
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
    };

    paginate();

    // Re-ejecutar cuando las imágenes terminen de cargar para medir alturas reales
    if (measureRef.current) {
      const imgs = Array.from(measureRef.current.querySelectorAll('img'));
      imgs.forEach(img => {
        if (!img.complete) {
          img.addEventListener('load', () => paginate(), { once: true });
          img.addEventListener('error', () => paginate(), { once: true });
        }
      });
    }

    if (typeof document !== 'undefined' && document.fonts) {
      document.fonts.ready.then(() => {
        if (!isCancelled) paginate();
      });
    }

    return () => {
      isCancelled = true;
    };
  }, [children, coverConfig]);

  return (
    <div className="flex flex-col items-center gap-12 print:block print:gap-0 w-full" id="paginator-root">
      {/* Contenedor de medición (oculto) */}
      <div
        className="measurement-container"
        style={{
          position: 'absolute',
          visibility: 'hidden',
          pointerEvents: 'none',
          width: '210mm',
          paddingLeft: '20mm',
          paddingRight: '20mm',
          boxSizing: 'border-box',
          zIndex: -1000
        }}
      >
        <div
          className="preview-content"
          ref={measureRef}
          style={{
            width: '170mm',
            boxSizing: 'border-box',
            fontFamily: "var(--font-family-content, 'Inter', sans-serif)",
            color: "var(--text-color, #2d2d2d)",
            lineHeight: '1.6',
            fontSize: '11pt',
            textAlign: 'justify',
          }}
        >
          {children}
        </div>
      </div>

      {/* Portada */}
      <CoverRenderer />

      {/* Pginas A4 */}
      {pages.map((pageHtml, index) => {
        const pageNumber = index + 1; // Content pages start at 1
        const totalContentPages = pages.length;
        const renderHeader = coverConfig?.showHeader !== false;
        const renderFooter = coverConfig?.showFooter !== false;

        const vars = {
          pageNumber,
          totalPages: totalContentPages,
          title: docTitle,
          sigla,
          materia,
          fecha,
        };

        // Header configuration
        const headerShowLine = coverConfig?.headerShowLine !== false;
        const rawHeaderLeft = coverConfig?.headerLeft !== undefined && String(coverConfig.headerLeft).trim() !== ''
          ? coverConfig.headerLeft
          : (sigla && docTitle ? '{sigla} - {title}' : (docTitle || sigla || ''));
        const headerLeftText = resolveTemplate(rawHeaderLeft, vars);
        const headerCenterText = resolveTemplate(coverConfig?.headerCenter, vars);
        const headerRightText = resolveTemplate(coverConfig?.headerRight != null && String(coverConfig.headerRight).trim() !== '' ? coverConfig.headerRight : (fecha ? '{fecha}' : ''), vars);

        // Footer configuration
        const footerShowLine = coverConfig?.footerShowLine !== false;
        const rawFooterLeft = coverConfig?.footerLeft !== undefined && String(coverConfig.footerLeft).trim() !== ''
          ? coverConfig.footerLeft
          : (materia || (sigla && docTitle ? '{sigla} - {title}' : ''));
        const footerLeftText = resolveTemplate(rawFooterLeft, vars);
        const footerCenterText = resolveTemplate(coverConfig?.footerCenter, vars);
        
        let footerRightText = '';
        if (coverConfig?.footerRight !== undefined && String(coverConfig.footerRight).trim() !== '') {
          footerRightText = resolveTemplate(coverConfig.footerRight, vars);
        } else {
          footerRightText = getNumberingString(coverConfig?.footerNumbering, pageNumber, totalContentPages);
        }

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
                  top: '12mm',
                  left: '20mm',
                  right: '20mm',
                }}
              >
                {/* Texto */}
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'baseline',
                  fontSize: '8.5pt',
                  color: '#4B5563',
                  fontFamily: "'Space Grotesk', system-ui, sans-serif",
                  marginBottom: '2mm'
                }}>
                  <div style={{ textAlign: 'left', flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {headerLeftText}
                  </div>
                  {headerCenterText && (
                    <div style={{ textAlign: 'center', flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {headerCenterText}
                    </div>
                  )}
                  <div style={{ textAlign: 'right', flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {headerRightText}
                  </div>
                </div>
                {/* Línea abajo del texto */}
                {headerShowLine && <div style={{ height: '1px', backgroundColor: '#E5E7EB' }} />}
              </div>
            )}

            {/* Contenido */}
            <div
              className="preview-content"
              style={{
                position: 'absolute',
                top:    renderHeader ? '24mm' : '16mm',
                left:   '20mm',
                right:  '20mm',
                bottom: renderFooter ? '24mm' : '16mm',
                overflow: 'hidden',
                fontFamily: "var(--font-family-content, 'Inter', sans-serif)",
                color: "var(--text-color, #2d2d2d)",
                lineHeight: '1.6',
                fontSize: '11pt',
                textAlign: 'justify',
              }}
              dangerouslySetInnerHTML={{ __html: pageHtml }}
            />

            {/* Footer */}
            {renderFooter && (
              <div
                style={{
                  position: 'absolute',
                  bottom: '12mm',
                  left: '20mm',
                  right: '20mm',
                }}
              >
                {/* Línea arriba del texto */}
                {footerShowLine && <div style={{ height: '1px', backgroundColor: '#E5E7EB', marginBottom: '2mm' }} />}
                {/* Texto */}
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'baseline',
                  fontSize: '8.5pt',
                  color: '#4B5563',
                  fontFamily: "'Space Grotesk', system-ui, sans-serif",
                }}>
                  <div style={{ textAlign: 'left', flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {footerLeftText}
                  </div>
                  {footerCenterText && (
                    <div style={{ textAlign: 'center', flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {footerCenterText}
                    </div>
                  )}
                  <div style={{ textAlign: 'right', flex: 1, fontWeight: 600, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {footerRightText}
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
