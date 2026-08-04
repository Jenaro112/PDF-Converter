export type ThemeKey = 'minimal' | 'classic' | 'institutional' | 'editorial' | 'blueprint' | 'pastel';

export interface ThemeConfig {
    name: string;
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

export const THEMES: Record<ThemeKey, ThemeConfig> = {
    minimal: {
        name: 'Minimalista Moderno',
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
    classic: {
        name: 'Académico Clásico',
        pygmentsStyle: 'friendly',
        previewBodyBg: '#e8e4d9',
        pageBg: '#FCFBF4',
        textColor: '#2e251b',
        headingColor: '#1a1410',
        accentColor: '#8b4513',
        mutedColor: '#7c6a59',
        fontFamilyContent: "'Literata', serif",
        fontFamilyHeadings: "'Literata', serif",
        codeBg: '#1e1e2e',
        codeBorder: '#313244',
        codeColor: '#cdd6f4',
        inlineCodeBg: '#f0ebe0',
        inlineCodeColor: '#9a3412',
        inlineCodeBorder: '#d4c9b0',
        quoteBorder: '#c9a84c',
        quoteBg: '#f5f0e1',
        tableHeaderBg: '#3d2b1f',
        tableHeaderFg: '#ffffff',
        tableBorder: '#d4c9b0',
        tableRowEvenBg: '#f6f1e5',
        h1BorderColor: '#c9a84c',
        h1BorderWidth: '2px',
    },
    institutional: {
        name: 'Institucional',
        pygmentsStyle: 'vs',
        previewBodyBg: '#dde3ea',
        pageBg: '#ffffff',
        textColor: '#1e293b',
        headingColor: '#1e3a5f',
        accentColor: '#c9a84c',
        mutedColor: '#64748b',
        fontFamilyContent: "'Inter', sans-serif",
        fontFamilyHeadings: "'Outfit', sans-serif",
        codeBg: '#1e1e2e',
        codeBorder: '#313244',
        codeColor: '#cdd6f4',
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
    editorial: {
        name: 'Editorial Moderno',
        pygmentsStyle: 'solarized-light',
        previewBodyBg: '#e6e6e2',
        pageBg: '#fdfdfb',
        textColor: '#2b2927',
        headingColor: '#7a2e3b',
        accentColor: '#7a2e3b',
        mutedColor: '#6e6a66',
        fontFamilyContent: "'Inter', system-ui, sans-serif",
        fontFamilyHeadings: "'Playfair Display', Georgia, serif",
        codeBg: '#1e1e2e',
        codeBorder: '#313244',
        codeColor: '#cdd6f4',
        inlineCodeBg: '#f3f2ee',
        inlineCodeColor: '#7a2e3b',
        inlineCodeBorder: '#e2dfd7',
        quoteBorder: '#7a2e3b',
        quoteBg: '#f7f5f0',
        tableHeaderBg: '#7a2e3b',
        tableHeaderFg: '#ffffff',
        tableBorder: '#e2dfd7',
        tableRowEvenBg: '#f9f8f5',
        h1BorderColor: '#7a2e3b',
        h1BorderWidth: '2px',
    },
    blueprint: {
        name: 'Técnico Claro',
        pygmentsStyle: 'tango',
        previewBodyBg: '#dbe2ea',
        pageBg: '#f7f9fb',
        textColor: '#1e293b',
        headingColor: '#0f172a',
        accentColor: '#2563eb',
        mutedColor: '#64748b',
        fontFamilyContent: "'IBM Plex Sans', 'Inter', sans-serif",
        fontFamilyHeadings: "'IBM Plex Sans', 'Inter', sans-serif",
        codeBg: '#0f172a',
        codeBorder: '#2563eb',
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
    pastel: {
        name: 'Cuadernillo Pastel',
        pygmentsStyle: 'autumn',
        previewBodyBg: '#ebdcd0',
        pageBg: '#fffaf3',
        textColor: '#332c27',
        headingColor: '#d96b52',
        accentColor: '#8b78b5',
        mutedColor: '#7d7067',
        fontFamilyContent: "'Inter', sans-serif",
        fontFamilyHeadings: "'Poppins', sans-serif",
        codeBg: '#2d2636',
        codeBorder: '#8b78b5',
        codeColor: '#f4e8ff',
        inlineCodeBg: '#f8eeec',
        inlineCodeColor: '#c44d34',
        inlineCodeBorder: '#ebd5d0',
        quoteBorder: '#8b78b5',
        quoteBg: '#f5f0fb',
        tableHeaderBg: '#d96b52',
        tableHeaderFg: '#ffffff',
        tableBorder: '#ebd5d0',
        tableRowEvenBg: '#fcf5ed',
        h1BorderColor: '#8b78b5',
        h1BorderWidth: '3px',
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

export function generateRootCSS(themeKey: ThemeKey): string {
    const theme = THEMES[themeKey];
    let css = '';
    for (const [key, value] of Object.entries(theme)) {
        if (key === 'name' || key === 'pygmentsStyle') continue;
        const kebabKey = key.replace(/([a-z0-9]|(?=[A-Z]))([A-Z])/g, '$1-$2').toLowerCase();
        css += `  --${kebabKey}: ${value};\n`;
    }
    return css;
}

export const THEME_CHOICES = [
    { label: 'Minimalista Moderno', key: 'minimal' as ThemeKey, emoji: '✨' },
    { label: 'Académico Clásico', key: 'classic' as ThemeKey, emoji: '🎓' },
    { label: 'Institucional', key: 'institutional' as ThemeKey, emoji: '🏛️' },
    { label: 'Editorial Moderno', key: 'editorial' as ThemeKey, emoji: '📰' },
    { label: 'Técnico Claro', key: 'blueprint' as ThemeKey, emoji: '📐' },
    { label: 'Cuadernillo Pastel', key: 'pastel' as ThemeKey, emoji: '🎨' },
];

export const MERMAID_THEME_CONFIG: Record<ThemeKey, any> = {
    minimal: { themeVariables: { primaryColor: '#f4f4f5', primaryTextColor: '#1a1a1a', primaryBorderColor: '#d4d4d8', lineColor: '#3a3a3a', secondaryColor: '#e4e4e7', tertiaryColor: '#ffffff', fontFamily: THEMES.minimal.fontFamilyContent, fontSize: '13px', nodePadding: '20' } },
    classic: { themeVariables: { primaryColor: '#f5f0e1', primaryTextColor: '#1a1410', primaryBorderColor: '#d4c9b0', lineColor: '#8b4513', secondaryColor: '#f0ebe0', tertiaryColor: '#FCFBF4', fontFamily: THEMES.classic.fontFamilyContent, fontSize: '13px', nodePadding: '20' } },
    institutional: { themeVariables: { primaryColor: '#f0f4f8', primaryTextColor: '#1e3a5f', primaryBorderColor: '#cbd5e1', lineColor: '#1e3a5f', secondaryColor: '#c9a84c', tertiaryColor: '#ffffff', fontFamily: THEMES.institutional.fontFamilyContent, fontSize: '13px', nodePadding: '20' } },
    editorial: { themeVariables: { primaryColor: '#f7f5f0', primaryTextColor: '#7a2e3b', primaryBorderColor: '#e2dfd7', lineColor: '#7a2e3b', secondaryColor: '#fdfdfb', tertiaryColor: '#ffffff', fontFamily: THEMES.editorial.fontFamilyContent, fontSize: '13px', nodePadding: '20' } },
    blueprint: { themeVariables: { primaryColor: '#eff6ff', primaryTextColor: '#0f172a', primaryBorderColor: '#bfdbfe', lineColor: '#2563eb', secondaryColor: '#dbe2ea', tertiaryColor: '#f7f9fb', fontFamily: THEMES.blueprint.fontFamilyContent, fontSize: '13px', nodePadding: '20' } },
    pastel: { themeVariables: { primaryColor: '#f5f0fb', primaryTextColor: '#332c27', primaryBorderColor: '#ebd5d0', lineColor: '#d96b52', secondaryColor: '#8b78b5', tertiaryColor: '#fffaf3', fontFamily: THEMES.pastel.fontFamilyContent, fontSize: '13px', nodePadding: '20' } },
};
