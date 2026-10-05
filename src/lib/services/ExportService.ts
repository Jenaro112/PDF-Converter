import type { CoverData } from '@/store/editor-store';
import type { ThemeKey } from '@/lib/themes/document-themes';

export interface ExportPayload {
  documentText: string;
  activeTheme: ThemeKey;
  coverConfig: CoverData | null;
  fileName?: string | null;
}

export class ExportService {
  /**
   * Facade pattern para ocultar la complejidad de la exportación a PDF.
   * Maneja la petición de red, el parseo del Blob y la descarga forzada en el cliente.
   */
  static async exportToPDF(payload: ExportPayload): Promise<void> {
    try {
      const res = await fetch('/api/export-pdf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        throw new Error(`Error del servidor: ${res.statusText}`);
      }

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      
      const safeName = payload.fileName ? payload.fileName.replace(/\.md$/, '') : 'documento';
      a.download = `${safeName}.pdf`;
      
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('ExportService Error:', error);
      throw error;
    }
  }
}
