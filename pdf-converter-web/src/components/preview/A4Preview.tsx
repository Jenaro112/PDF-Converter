'use client';

import { useEffect, useRef, useMemo, useDeferredValue, useCallback } from 'react';
import { useEditorStore } from '@/store/editor-store';
import { processMarkdown } from '@/lib/markdown/processor';
import { extractMermaidBlocks, renderMermaidDiagrams } from '@/lib/mermaid/renderer';
import { THEMES, type ThemeKey } from '@/lib/themes';
import { generateCoverHtml } from '@/lib/covers';
import { paginateDocument } from '@/lib/pagination/paginator';
import '@/styles/preview.css';
import '@/styles/covers.css';

/**
 * A4Preview — Renders the processed Markdown as discrete A4-sized page cards (.preview-page).
 * Uses DOM-based height measurement to automatically break pages into distinct A4 cards.
 */
export function A4Preview() {
  const markdown = useEditorStore((s) => s.markdown);
  const theme = useEditorStore((s) => s.theme);
  const coverConfig = useEditorStore((s) => s.coverConfig);
  const showCover = useEditorStore((s) => s.showCover);

  const containerRef = useRef<HTMLDivElement>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const savedScrollRef = useRef<number>(0);

  const deferredMarkdown = useDeferredValue(markdown);
  const deferredTheme = useDeferredValue(theme);
  const deferredCoverConfig = useDeferredValue(coverConfig);
  const deferredShowCover = useDeferredValue(showCover);

  // Generate cover HTML if enabled
  const coverHtml = useMemo(() => {
    if (!deferredShowCover) return '';
    return generateCoverHtml(deferredCoverConfig);
  }, [deferredShowCover, deferredCoverConfig]);

  // Process markdown to HTML
  const bodyHtml = useMemo(() => {
    if (!deferredMarkdown.trim()) {
      return '<p style="color: var(--muted-color); padding: 10mm; opacity: 0.6; font-style: italic;">Escribí Markdown en el editor para ver la vista previa aquí…</p>';
    }
    const withMermaidPlaceholders = extractMermaidBlocks(deferredMarkdown);
    return processMarkdown(withMermaidPlaceholders, deferredTheme as ThemeKey, Boolean(coverHtml));
  }, [deferredMarkdown, deferredTheme, coverHtml]);

  // Generate CSS variables for the current theme
  const themeStyles = useMemo(() => {
    const t = THEMES[deferredTheme as ThemeKey] || THEMES.minimal;
    const vars: Record<string, string> = {};
    for (const [key, value] of Object.entries(t)) {
      if (key === 'name' || key === 'pygmentsStyle') continue;
      const cssKey = `--${key.replace(/([A-Z])/g, '-$1').toLowerCase()}`;
      vars[cssKey] = value;
    }
    return vars;
  }, [deferredTheme]);

  // Save scroll position before re-render
  const saveScroll = useCallback(() => {
    if (scrollRef.current) {
      savedScrollRef.current = scrollRef.current.scrollTop;
    }
  }, []);

  // Perform pagination, render Mermaid & KaTeX
  useEffect(() => {
    if (containerRef.current) {
      // Step 1: Paginate HTML into separate A4 page cards
      paginateDocument(containerRef.current, coverHtml, bodyHtml);

      // Step 2: Render Mermaid diagrams inside the paginated cards
      renderMermaidDiagrams(containerRef.current, deferredTheme as ThemeKey);

      // Step 3: Render KaTeX math formulas
      if (typeof window !== 'undefined') {
        import('katex').then((katex) => {
          if (!containerRef.current) return;

          const displayMaths = containerRef.current.querySelectorAll('.math-display');
          displayMaths.forEach((el) => {
            const tex = el.textContent?.replace(/^\$\$/, '').replace(/\$\$$/, '').trim();
            if (tex) {
              try {
                el.innerHTML = katex.default.renderToString(tex, {
                  displayMode: true,
                  throwOnError: false,
                  output: 'html',
                });
              } catch { /* ignore KaTeX render errors */ }
            }
          });

          const inlineMaths = containerRef.current.querySelectorAll('.math-inline');
          inlineMaths.forEach((el) => {
            const tex = el.textContent?.replace(/^\$/, '').replace(/\$$/, '').trim();
            if (tex) {
              try {
                el.innerHTML = katex.default.renderToString(tex, {
                  displayMode: false,
                  throwOnError: false,
                  output: 'html',
                });
              } catch { /* ignore KaTeX render errors */ }
            }
          });
        });
      }
    }

    if (scrollRef.current && savedScrollRef.current > 0) {
      scrollRef.current.scrollTop = savedScrollRef.current;
    }
  }, [bodyHtml, coverHtml, deferredTheme]);

  // Save scroll on markdown edit
  useEffect(() => {
    saveScroll();
  }, [markdown, saveScroll]);

  return (
    <div
      className="preview-scroll-container"
      ref={scrollRef}
      style={themeStyles as React.CSSProperties}
    >
      <div className="preview-container" ref={containerRef} />
    </div>
  );
}
