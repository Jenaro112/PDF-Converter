'use client';
import React, { useEffect, useState, useId } from 'react';

export function Mermaid({ chart }: { chart: string }) {
  const [svgHtml, setSvgHtml] = useState<string>('');
  const [error, setError] = useState<string | null>(null);
  const reactId = useId().replace(/[^a-zA-Z0-9]/g, '');

  // Debouncear el chart: solo se re-renderiza cuando el usuario hace una pausa
  const [debouncedChart, setDebouncedChart] = useState(chart);
  useEffect(() => {
    const timer = setTimeout(() => setDebouncedChart(chart), 250);
    return () => clearTimeout(timer);
  }, [chart]);

  useEffect(() => {
    let isCancelled = false;

    async function renderMermaid() {
      if (!debouncedChart || !debouncedChart.trim()) {
        setSvgHtml('');
        return;
      }

      try {
        const mermaid = (await import('mermaid')).default;
        mermaid.initialize({
          startOnLoad: false,
          theme: 'base',
          flowchart: {
            useMaxWidth: true,
            htmlLabels: true,
            curve: 'basis',
            nodeSpacing: 30,
            rankSpacing: 35,
            padding: 12,
          },
          themeVariables: {
            fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
            fontSize: '13px',
            darkMode: false,
            background: '#ffffff',
            mainBkg: '#ffffff',
            primaryColor: '#f8fafc',
            primaryTextColor: '#0f172a',
            primaryBorderColor: '#94a3b8',
            lineColor: '#64748b',
            secondaryColor: '#f1f5f9',
            secondaryTextColor: '#0f172a',
            secondaryBorderColor: '#cbd5e1',
            edgeLabelBackground: '#ffffff',
            nodeBorder: '#cbd5e1',
            nodeTextColor: '#0f172a',
          },
        });

        // ID único para cada render de Mermaid
        const currentId = `mermaid_${reactId}_${Date.now()}`;
        const cleanChart = debouncedChart.trim();
        const { svg } = await mermaid.render(currentId, cleanChart);

        if (!isCancelled) {
          setSvgHtml(svg);
          setError(null);
          if (typeof window !== 'undefined') {
            window.dispatchEvent(new CustomEvent('mermaid-rendered'));
          }
        }
      } catch (err: any) {
        if (!isCancelled) {
          console.warn('Mermaid rendering notice:', err?.message || err);
          setError(err?.message || 'Error renderizando diagrama');
        }
      }
    }

    renderMermaid();

    return () => {
      isCancelled = true;
    };
  }, [debouncedChart, reactId]);

  if (error && !svgHtml) {
    return (
      <div className="my-4 rounded-xl border border-red-200 bg-red-50 p-4 text-xs text-red-700">
        <strong>Error en diagrama Mermaid:</strong> {error}
      </div>
    );
  }

  if (!svgHtml) {
    return (
      <div className="mermaid-container my-6 rounded-2xl border border-gray-100 bg-gray-50/50 p-6 flex justify-center items-center text-xs text-gray-400">
        Cargando diagrama...
      </div>
    );
  }

  return (
    <div className="mermaid-container my-6 rounded-2xl border border-gray-200 bg-white shadow-sm w-full overflow-hidden p-4 flex justify-center items-center">
      <div
        className="mermaid-svg-wrapper w-full flex justify-center items-center"
        dangerouslySetInnerHTML={{ __html: svgHtml }}
      />
    </div>
  );
}
