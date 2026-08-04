import MarkdownIt from 'markdown-it';
import { ThemeKey } from '../themes';
import { protectLatex, restoreLatex } from './katex-plugin';
import { processHighlights } from './highlight-plugin';
import { processPagebreaks, cleanRedundantPagebreaks } from './pagebreak-plugin';

const md = new MarkdownIt({ html: true });

function cleanPandocAttributes(text: string): string {
    // Images with attributes: ![alt](src){...} → ![alt](src)
    let cleaned = text.replace(/(!\[[^\]]*\]\([^)]*\))\s*\{[^}]*\}/g, '$1');
    // Spans with class: [text]{.underline} → text
    cleaned = cleaned.replace(/\[([^\]]*)\]\{[^}]*\}/g, '$1');
    // Headers with attributes: # Title {#id .class} → # Title
    cleaned = cleaned.replace(/^(#{1,6}\s+.*?)\s*\{[^}]*\}\s*$/gm, '$1');
    // Standalone attributes on their own line: {width="5in"}
    cleaned = cleaned.replace(/^\s*\{[^}]*\}\s*$/gm, '');
    return cleaned;
}

export function processMarkdown(markdown: string, themeKey: ThemeKey, hasCover: boolean = false): string {
    // Clean pandoc specific attrs
    let processed = cleanPandocAttributes(markdown);

    // Process pagebreaks and highlights
    processed = processPagebreaks(processed);
    processed = processHighlights(processed);

    // Protect LaTeX blocks
    const { text: latexProtected, displayMaths, inlineMaths } = protectLatex(processed);
    
    // Parse markdown to HTML
    let html = md.render(latexProtected);

    // Restore LaTeX blocks
    html = restoreLatex(html, displayMaths, inlineMaths);

    // Clean redundant pagebreaks
    html = cleanRedundantPagebreaks(html, hasCover);

    return html;
}

