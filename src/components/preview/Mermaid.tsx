'use client';
import React, { useRef, useEffect, useState } from 'react';

// Genera un HTML autónomo que carga Mermaid desde CDN en un iframe aislado
function buildMermaidHTML(chart: string): string {
  // Escapar caracteres especiales para evitar romper el HTML
  const escaped = chart
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');

  return `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body { 
    background: transparent; 
    display: flex; 
    justify-content: center; 
    align-items: flex-start;
    min-height: 100%;
  }
  .mermaid { 
    max-width: 100%; 
    display: flex; 
    justify-content: center;
  }
  .mermaid svg { max-width: 100%; height: auto; }
</style>
</head>
<body>
<div class="mermaid">${escaped}</div>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({ 
    startOnLoad: true, 
    theme: 'base',
    themeVariables: {
      fontFamily: 'Inter, sans-serif',
      primaryColor: '#faf8f5',
      primaryTextColor: '#4a4543',
      primaryBorderColor: '#e6e2dd',
      lineColor: '#8c827a',
    }
  });

  function notifyHeight() {
    const h = document.documentElement.scrollHeight;
    window.parent.postMessage({ type: 'mermaid-height', height: h }, '*');
  }

  // Esperar a que Mermaid inserte el SVG en el DOM y luego medir
  const observer = new MutationObserver(function() {
    const svg = document.querySelector('.mermaid svg');
    if (svg) {
      observer.disconnect();
      // Esperar un frame más para que el layout esté completo
      requestAnimationFrame(function() {
        requestAnimationFrame(notifyHeight);
      });
      // También usar ResizeObserver por si el SVG cambia de tamaño
      const ro = new ResizeObserver(notifyHeight);
      ro.observe(svg);
    }
  });
  observer.observe(document.body, { childList: true, subtree: true });

  // Fallback: notificar cada segundo por si el observer no dispara
  setTimeout(notifyHeight, 800);
  setTimeout(notifyHeight, 2000);
</script>
</body>
</html>`;
}

export function Mermaid({ chart }: { chart: string }) {
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const [height, setHeight] = useState(400);

  // Debouncear el chart: el iframe solo se recarga cuando el usuario para de tipear 800ms
  const [debouncedChart, setDebouncedChart] = useState(chart);
  useEffect(() => {
    const timer = setTimeout(() => setDebouncedChart(chart), 800);
    return () => clearTimeout(timer);
  }, [chart]);

  const srcDoc = buildMermaidHTML(debouncedChart);

  // Escuchar mensajes del iframe para ajustar la altura dinámicamente
  useEffect(() => {
    function handleMessage(e: MessageEvent) {
      if (e.data?.type === 'mermaid-height' && typeof e.data.height === 'number') {
        const newHeight = Math.max(e.data.height + 32, 120);
        setHeight(newHeight);
      }
    }
    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, []);

  return (
    <div className="my-6 rounded-xl border border-[var(--border)] bg-[#fdfbf8] shadow-sm w-full overflow-hidden">
      <iframe
        ref={iframeRef}
        srcDoc={srcDoc}
        sandbox="allow-scripts"
        style={{ width: '100%', height: `${height}px`, border: 'none', display: 'block' }}
        title="Diagrama Mermaid"
      />
    </div>
  );
}
