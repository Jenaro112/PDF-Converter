'use client';
import { useState, useEffect } from 'react';
import { useMarkdownProcessor } from '@/lib/markdown/pipeline';
import { Paginator } from '@/components/preview/Paginator';
import { CoverRenderer } from '@/components/preview/covers/CoverRenderer';
import { useEditorStore } from '@/store/editor-store';
import { generateRootCSS } from '@/lib/themes/document-themes';

export default function PrintPage() {
  const [ready, setReady] = useState(false);

  useEffect(() => {
    // Exponer la función para que Puppeteer inyecte los datos
    (window as any).loadDataForPrint = (text: string, coverConfig: any, activeTheme: any) => {
      useEditorStore.setState({ documentText: text, coverConfig, activeTheme });
      setReady(true);
    };
    
    // Avisar a Puppeteer que la página cargó y está lista para recibir datos
    (window as any).isReadyToReceive = true;
    
    // Limpiar fondos grises para evitar problemas al imprimir
    document.body.style.backgroundColor = 'white';
  }, []);

  const { documentText, activeTheme } = useEditorStore();
  const content = useMarkdownProcessor(documentText);

  if (!ready) {
    return <div className="p-8 text-center text-gray-400 font-sans">Preparando documento para impresión...</div>;
  }

  return (
    <div className="bg-white min-h-screen print:block">
      {/* Inyectar variables de tema del documento */}
      <style dangerouslySetInnerHTML={{ __html: generateRootCSS(activeTheme) }} />
      
      <Paginator>{content}</Paginator>
    </div>
  );
}
