import { type ThemeKey, MERMAID_THEME_CONFIG } from '../themes';
import { applyMermaidFlexboxFix } from './flexbox-fix';

/**
 * Renders mermaid diagram placeholders inside a container element.
 * Called client-side after the HTML is mounted in the DOM.
 */
export async function renderMermaidDiagrams(
  containerElement: HTMLElement,
  themeKey: ThemeKey
): Promise<void> {
  const placeholders = containerElement.querySelectorAll('.mermaid-placeholder');
  if (placeholders.length === 0) return;

  // Dynamic import to avoid SSR issues
  const mermaid = (await import('mermaid')).default;
  const config = MERMAID_THEME_CONFIG[themeKey];

  mermaid.initialize({
    startOnLoad: false,
    theme: 'base',
    themeVariables: config.themeVariables,
  });

  for (let i = 0; i < placeholders.length; i++) {
    const el = placeholders[i] as HTMLElement;
    const codeBase64 = el.getAttribute('data-mermaid');
    if (!codeBase64) continue;

    try {
      const code = atob(codeBase64);
      const id = `mermaid-${Date.now()}-${i}`;
      const { svg } = await mermaid.render(id, code);
      const fixedSvg = applyMermaidFlexboxFix(svg);

      const wrapper = document.createElement('div');
      wrapper.className = 'mermaid-diagram';
      wrapper.innerHTML = fixedSvg;

      el.replaceWith(wrapper);
    } catch (error) {
      console.error('Failed to render mermaid diagram:', error);
      el.innerHTML = `<div class="mermaid-fallback-box">
        <div class="mermaid-fallback-header">📊 Error al renderizar diagrama</div>
        <pre class="mermaid-fallback-code"><code>${el.textContent || ''}</code></pre>
      </div>`;
    }
  }
}

/**
 * Extracts ```mermaid ... ``` blocks from markdown and replaces them
 * with placeholder divs. The mermaid code is base64-encoded in a
 * data attribute for later client-side rendering.
 *
 * Works on both server and client (uses Buffer on Node, btoa on browser).
 */
export function extractMermaidBlocks(markdown: string): string {
  const mermaidRegex = /```mermaid\s*\n([\s\S]*?)```/g;
  return markdown.replace(mermaidRegex, (_, code: string) => {
    const trimmedCode = code.trim();
    // Use Buffer for Node.js (SSR) or btoa for browser
    const base64Code =
      typeof Buffer !== 'undefined'
        ? Buffer.from(trimmedCode, 'utf-8').toString('base64')
        : btoa(unescape(encodeURIComponent(trimmedCode)));
    return `<div data-mermaid="${base64Code}" class="mermaid-placeholder">Cargando diagrama…</div>`;
  });
}
