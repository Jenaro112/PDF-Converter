import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { ThemeKey } from '@/lib/themes/document-themes';

export interface CoverData {
  showCover: boolean;
  title: string;
  subtitle: string;
  materia: string;
  coverStyle: 'barra_azul' | 'blanca_simple' | 'fcyt_uader';
  integrantes: string[];
  profesores: string[];
  /** Abreviatura del trabajo — aparece en el encabezado (ej: "TI") */
  sigla?: string;
  /** Fecha que se muestra en la portada (ej: "13/06/2026") */
  fecha?: string;
  showHeader?: boolean;
  showFooter?: boolean;
}

export interface PageConfigData {
  numbering: 'Ninguno' | '1' | '- 1 -' | 'Página 1 de N';
  headerLeft: string;
  headerCenter: string;
  headerRight: string;
  footerLeft: string;
  footerCenter: string;
  footerRight: string;
}

export type FormatType =
  | 'bold'
  | 'italic'
  | 'highlight'
  | 'strikethrough'
  | 'code-inline'
  | 'latex-inline';

interface EditorState {
  documentText: string;
  fileName: string | null;
  isDirty: boolean;
  contentVersion: number;

  isSidebarOpen: boolean;
  isPreviewExpanded: boolean;
  isSettingsOpen: boolean;

  activeTheme: ThemeKey;

  coverConfig: CoverData | null;
  pageConfig: PageConfigData | null;

  zoomLevel: number;
  renderedHTML: string;

  cursorLine: number;
  cursorCol: number;
  wordCount: number;

  setText: (text: string) => void;
  loadContent: (text: string, name: string | null) => void;
  setFileName: (name: string | null) => void;
  toggleSidebar: () => void;
  togglePreviewExpanded: () => void;
  toggleSettings: () => void;
  setTheme: (theme: ThemeKey) => void;
  setCover: (config: CoverData | null) => void;
  setPageConfig: (config: PageConfigData | null) => void;
  setZoom: (level: number) => void;
  setRenderedHTML: (html: string) => void;
  setCursor: (line: number, col: number) => void;
  setWordCount: (count: number) => void;
  markSaved: () => void;
  markDirty: () => void;

  formatAction: FormatType | null;
  setFormatAction: (action: FormatType | null) => void;

  snippetToInsert: string | null;
  setSnippetToInsert: (snippet: string | null) => void;

  editorScrollPercent: number;
  setEditorScrollPercent: (percent: number) => void;
}

export const useEditorStore = create<EditorState>()(
  persist(
    (set) => ({
      documentText: '# Bienvenido a PDF Converter\n\nEste es tu nuevo documento.',
      fileName: null,
      isDirty: false,
      contentVersion: 0,

      isSidebarOpen: false,
      isPreviewExpanded: false,
      isSettingsOpen: false,

      activeTheme: 'minimal',

      coverConfig: null,
      pageConfig: null,

      zoomLevel: 100,
      renderedHTML: '',

      cursorLine: 1,
      cursorCol: 1,
      wordCount: 5,

      setText: (text) =>
        set({ documentText: text, isDirty: true, wordCount: text.trim() ? text.trim().split(/\s+/).length : 0 }),

      loadContent: (text, name) =>
        set((state) => ({
          documentText: text,
          fileName: name,
          isDirty: false,
          contentVersion: state.contentVersion + 1,
          wordCount: text.trim() ? text.trim().split(/\s+/).length : 0,
        })),

      setFileName: (name) => set({ fileName: name }),
      toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),
      togglePreviewExpanded: () => set((state) => ({ isPreviewExpanded: !state.isPreviewExpanded })),
      toggleSettings: () => set((state) => ({ isSettingsOpen: !state.isSettingsOpen })),
      setTheme: (theme) => set({ activeTheme: theme }),
      setCover: (config) => set({ coverConfig: config }),
      setPageConfig: (config) => set({ pageConfig: config }),
      setZoom: (level) => set({ zoomLevel: Math.max(50, Math.min(200, level)) }),
      setRenderedHTML: (html) => set({ renderedHTML: html }),
      setCursor: (line, col) => set({ cursorLine: line, cursorCol: col }),
      setWordCount: (count) => set({ wordCount: count }),
      markSaved: () => set({ isDirty: false }),
      markDirty: () => set({ isDirty: true }),

      formatAction: null,
      setFormatAction: (action) => set({ formatAction: action }),

      snippetToInsert: null,
      setSnippetToInsert: (snippet) => set({ snippetToInsert: snippet }),

      editorScrollPercent: 0,
      setEditorScrollPercent: (percent) => set({ editorScrollPercent: percent }),
    }),
    {
      name: 'pdf-converter-storage', // key in localStorage
      partialize: (state) => ({
        documentText: state.documentText,
        fileName: state.fileName,
        activeTheme: state.activeTheme,
        coverConfig: state.coverConfig,
        pageConfig: state.pageConfig,
        contentVersion: state.contentVersion, // ensures editor updates text
      }),
    }
  )
);
