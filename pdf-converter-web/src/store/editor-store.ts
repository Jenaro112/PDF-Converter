import { create } from 'zustand';
import { ThemeKey } from '../lib/themes';
import { CoverConfig } from '../lib/covers';

interface EditorState {
    markdown: string;
    theme: ThemeKey;
    fileName: string;
    coverConfig: CoverConfig | null;
    showCover: boolean;
    images: Record<string, string>;
    setMarkdown: (md: string) => void;
    setTheme: (theme: ThemeKey) => void;
    setFileName: (name: string) => void;
    setCoverConfig: (config: CoverConfig | null) => void;
    setShowCover: (show: boolean) => void;
    addImage: (name: string, dataUri: string) => void;
}

const DEFAULT_MARKDOWN = `# Bienvenido a PDF Converter Web

Este es un editor de **Markdown** con vista previa en tiempo real y exportación a PDF de alta calidad.

## Características

- ✏️ Editor con resaltado de sintaxis
- 👀 Vista previa paginada A4
- 🎨 6 temas profesionales
- 📐 Fórmulas matemáticas con KaTeX
- 📊 Diagramas Mermaid
- 📄 Exportación a PDF

## Ejemplo de Código

\`\`\`python
def fibonacci(n: int) -> list[int]:
    """Genera la secuencia de Fibonacci."""
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[-1] + fib[-2])
    return fib
\`\`\`

## Fórmulas Matemáticas

Inline: $E = mc^2$

En bloque:

$$\\sum_{i=1}^{n} i = \\frac{n(n+1)}{2}$$

## Tabla Comparativa

| Tema | Fuente | Estilo |
|------|--------|--------|
| Minimalista | Space Grotesk | Limpio y moderno |
| Académico | Literata | Tradicional serif |
| Institucional | Inter | Corporativo |
`;

export const useEditorStore = create<EditorState>((set) => ({
    markdown: DEFAULT_MARKDOWN,
    theme: 'minimal',
    fileName: 'Untitled',
    coverConfig: null,
    showCover: false,
    images: {},
    setMarkdown: (md) => set({ markdown: md }),
    setTheme: (theme) => set({ theme }),
    setFileName: (fileName) => set({ fileName }),
    setCoverConfig: (coverConfig) => set({ coverConfig }),
    setShowCover: (showCover) => set({ showCover }),
    addImage: (name, dataUri) => set((state) => ({ images: { ...state.images, [name]: dataUri } })),
}));
