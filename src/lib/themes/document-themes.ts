export interface ThemeDefinition {
  key: string;
  name: string;
  icon: string;
  pygmentsStyle: string;
  previewBodyBg: string;
  pageBg: string;
  textColor: string;
  headingColor: string;
  accentColor: string;
  mutedColor: string;
  fontFamilyContent: string;
  fontFamilyHeadings: string;
  codeBg: string;
  codeBorder: string;
  codeColor: string;
  inlineCodeBg: string;
  inlineCodeColor: string;
  inlineCodeBorder: string;
  quoteBorder: string;
  quoteBg: string;
  tableHeaderBg: string;
  tableHeaderFg: string;
  tableBorder: string;
  tableRowEvenBg: string;
  h1BorderColor: string;
  h1BorderWidth: string;
}

export const THEMES: Record<string, ThemeDefinition> = {
  minimal: {
    key: 'minimal',
    name: '✦ Minimalista Moderno',
    icon: '✦',
    pygmentsStyle: 'monokai',
    previewBodyBg: '#e4e4e7',
    pageBg: '#ffffff',
    textColor: '#2d2d2d',
    headingColor: '#1a1a1a',
    accentColor: '#3a3a3a',
    mutedColor: '#6b6b6b',
    fontFamilyContent: "'Space Grotesk', sans-serif",
    fontFamilyHeadings: "'Space Grotesk', sans-serif",
    codeBg: '#1e1e2e',
    codeBorder: '#313244',
    codeColor: '#cdd6f4',
    inlineCodeBg: '#f3f4f6',
    inlineCodeColor: '#d63384',
    inlineCodeBorder: '#e1e4e8',
    quoteBorder: '#d4d4d8',
    quoteBg: '#f4f4f5',
    tableHeaderBg: '#27272a',
    tableHeaderFg: '#ffffff',
    tableBorder: '#e4e4e7',
    tableRowEvenBg: '#fafafa',
    h1BorderColor: '#e4e4e7',
    h1BorderWidth: '1px',
  },
  institutional: {
    key: 'institutional',
    name: '🏛 Institucional',
    icon: '🏛',
    pygmentsStyle: 'one-dark',
    previewBodyBg: '#dde3ea',
    pageBg: '#ffffff',
    textColor: '#1e293b',
    headingColor: '#1e3a5f',
    accentColor: '#c9a84c',
    mutedColor: '#64748b',
    fontFamilyContent: "'Inter', sans-serif",
    fontFamilyHeadings: "'Outfit', sans-serif",
    codeBg: '#1e293b',
    codeBorder: '#334155',
    codeColor: '#e2e8f0',
    inlineCodeBg: '#f0f4f8',
    inlineCodeColor: '#c2410c',
    inlineCodeBorder: '#cbd5e1',
    quoteBorder: '#1e3a5f',
    quoteBg: '#f0f4f8',
    tableHeaderBg: '#1e3a5f',
    tableHeaderFg: '#ffffff',
    tableBorder: '#cbd5e1',
    tableRowEvenBg: '#f8fafc',
    h1BorderColor: '#1e3a5f',
    h1BorderWidth: '3px',
  },
  blueprint: {
    key: 'blueprint',
    name: '⚙️ Técnico Claro',
    icon: '⚙️',
    pygmentsStyle: 'material',
    previewBodyBg: '#dbe2ea',
    pageBg: '#f7f9fb',
    textColor: '#1e293b',
    headingColor: '#0f172a',
    accentColor: '#2563eb',
    mutedColor: '#64748b',
    fontFamilyContent: "'IBM Plex Sans', 'Inter', sans-serif",
    fontFamilyHeadings: "'IBM Plex Sans', 'Inter', sans-serif",
    codeBg: '#0f172a',
    codeBorder: '#1e3a8a',
    codeColor: '#93c5fd',
    inlineCodeBg: '#eff6ff',
    inlineCodeColor: '#1d4ed8',
    inlineCodeBorder: '#bfdbfe',
    quoteBorder: '#2563eb',
    quoteBg: '#eff6ff',
    tableHeaderBg: '#1e40af',
    tableHeaderFg: '#ffffff',
    tableBorder: '#cbd5e1',
    tableRowEvenBg: '#f1f5f9',
    h1BorderColor: '#2563eb',
    h1BorderWidth: '2px',
  },
  nordic: {
    key: 'nordic',
    name: '❄ Nórdico Limpio',
    icon: '❄',
    pygmentsStyle: 'nord',
    previewBodyBg: '#d8dee6',
    pageBg: '#f8f9fb',
    textColor: '#2e3440',
    headingColor: '#1d2433',
    accentColor: '#4a6fa5',
    mutedColor: '#6b7b8d',
    fontFamilyContent: "'Figtree', 'Inter', sans-serif",
    fontFamilyHeadings: "'Figtree', 'Inter', sans-serif",
    codeBg: '#2e3440',
    codeBorder: '#3b4252',
    codeColor: '#d8dee9',
    inlineCodeBg: '#edf1f7',
    inlineCodeColor: '#3560a0',
    inlineCodeBorder: '#c8d1de',
    quoteBorder: '#4a6fa5',
    quoteBg: '#edf1f7',
    tableHeaderBg: '#2e3d55',
    tableHeaderFg: '#eceff4',
    tableBorder: '#c8d1de',
    tableRowEvenBg: '#f2f4f8',
    h1BorderColor: '#4a6fa5',
    h1BorderWidth: '2px',
  },
  vanguardia: {
    key: 'vanguardia',
    name: '🚀 Vanguardia Institucional',
    icon: '🚀',
    pygmentsStyle: 'one-dark',
    previewBodyBg: '#e2e6ec',
    pageBg: '#ffffff',
    textColor: '#4C4F69',
    headingColor: '#1A1B26',
    accentColor: '#7AA2F7',
    mutedColor: '#6c7086',
    fontFamilyContent: "'Satoshi', 'Inter', sans-serif",
    fontFamilyHeadings: "'Cabinet Grotesk', 'Inter', sans-serif",
    codeBg: '#1A1B26',
    codeBorder: '#2a2b3d',
    codeColor: '#c0caf5',
    inlineCodeBg: '#f0f3f8',
    inlineCodeColor: '#7AA2F7',
    inlineCodeBorder: '#dce3ed',
    quoteBorder: '#7AA2F7',
    quoteBg: '#f0f4ff',
    tableHeaderBg: '#1A1B26',
    tableHeaderFg: '#c0caf5',
    tableBorder: '#dce3ed',
    tableRowEvenBg: '#f8fafc',
    h1BorderColor: '#7AA2F7',
    h1BorderWidth: '2px',
  },
  ecosistema: {
    key: 'ecosistema',
    name: '◉ Ecosistema Moderno',
    icon: '◉',
    pygmentsStyle: 'monokai',
    previewBodyBg: '#e4e4e7',
    pageBg: '#ffffff',
    textColor: '#52525B',
    headingColor: '#09090B',
    accentColor: '#18181B',
    mutedColor: '#71717A',
    fontFamilyContent: "'Geist', 'Inter', sans-serif",
    fontFamilyHeadings: "'Manrope', 'Inter', sans-serif",
    codeBg: '#09090B',
    codeBorder: '#27272A',
    codeColor: '#d4d4d8',
    inlineCodeBg: '#f4f4f5',
    inlineCodeColor: '#18181B',
    inlineCodeBorder: '#e4e4e7',
    quoteBorder: '#18181B',
    quoteBg: '#fafafa',
    tableHeaderBg: '#09090B',
    tableHeaderFg: '#fafafa',
    tableBorder: '#e4e4e7',
    tableRowEvenBg: '#fafafa',
    h1BorderColor: '#18181B',
    h1BorderWidth: '2px',
  },
};

export const PASTEL_COLORS: Record<string, string> = {
  amarillo: '#fff3b0',
  rosa: '#f8c8dc',
  rojo: '#fca5a5',
  verde: '#bbf7d0',
  celeste: '#bae6fd',
  naranja: '#fed7aa',
  violeta: '#ddd6fe',
};

export type ThemeKey = keyof typeof THEMES;

export function getThemeChoices(): { key: ThemeKey; name: string; icon: string }[] {
  return Object.values(THEMES).map((t) => ({ key: t.key as ThemeKey, name: t.name, icon: t.icon }));
}

export function generateRootCSS(themeKey: ThemeKey): string {
  const t = THEMES[themeKey];
  if (!t) return '';
  return `:root {
    --preview-body-bg: ${t.previewBodyBg};
    --page-bg: ${t.pageBg};
    --text-color: ${t.textColor};
    --heading-color: ${t.headingColor};
    --accent-color: ${t.accentColor};
    --muted-color: ${t.mutedColor};
    --font-family-content: ${t.fontFamilyContent};
    --font-family-headings: ${t.fontFamilyHeadings};
    --code-bg: ${t.codeBg};
    --code-border: ${t.codeBorder};
    --code-color: ${t.codeColor};
    --inline-code-bg: ${t.inlineCodeBg};
    --inline-code-color: ${t.inlineCodeColor};
    --inline-code-border: ${t.inlineCodeBorder};
    --quote-border: ${t.quoteBorder};
    --quote-bg: ${t.quoteBg};
    --table-header-bg: ${t.tableHeaderBg};
    --table-header-fg: ${t.tableHeaderFg};
    --table-border: ${t.tableBorder};
    --table-row-even-bg: ${t.tableRowEvenBg};
    --h1-border-color: ${t.h1BorderColor};
    --h1-border-width: ${t.h1BorderWidth};
  }`;
}
