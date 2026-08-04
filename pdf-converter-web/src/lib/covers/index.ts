export type CoverStyle = 'classic' | 'sidebar' | 'minimal' | 'technical';

export interface CoverConfig {
  title?: string;
  subtitle?: string;
  materia?: string;
  integrantes?: string;
  profesores?: string;
  showLogo?: boolean;
  logoPosition?: 'left' | 'center' | 'right';
  coverStyle?: CoverStyle;
}

/**
 * Generates the HTML for the cover page.
 */
export function generateCoverHtml(config: CoverConfig | null, logoUrl: string = '/assets/UADER_logo.png'): string {
  if (!config || !config.title) return '';

  const {
    title,
    subtitle = '',
    materia = '',
    integrantes = '',
    profesores = '',
    showLogo = true,
    logoPosition = 'center',
    coverStyle = 'classic',
  } = config;

  const logoHtml = showLogo
    ? `<img src="${logoUrl}" class="cover-logo logo-pos-${logoPosition}" alt="Logo Institucional" />`
    : '';

  const subtitleHtml = subtitle
    ? `<p class="cover-subtitle">${subtitle}</p>`
    : '';

  const metaItems = [
    materia ? `<div class="cover-meta-item"><span class="meta-label">Materia:</span> <span class="meta-value">${materia}</span></div>` : '',
    integrantes ? `<div class="cover-meta-item"><span class="meta-label">Integrantes:</span> <span class="meta-value">${integrantes}</span></div>` : '',
    profesores ? `<div class="cover-meta-item"><span class="meta-label">Profesores:</span> <span class="meta-value">${profesores}</span></div>` : '',
  ].filter(Boolean).join('');

  return `
    <div class="preview-page cover-page cover-style-${coverStyle}">
      ${coverStyle === 'sidebar' ? '<div class="cover-sidebar-stripe"></div>' : ''}
      <div class="cover-inner">
        <div class="cover-header">
          ${logoHtml}
          <div class="cover-kicker">DOCUMENTO ACADÉMICO / TÉCNICO</div>
        </div>
        <div class="cover-body">
          <h1 class="cover-title">${title}</h1>
          ${subtitleHtml}
        </div>
        ${metaItems ? `<div class="cover-footer-meta">${metaItems}</div>` : ''}
      </div>
    </div>
  `;
}
