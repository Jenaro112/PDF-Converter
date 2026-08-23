import re
import platform
from pathlib import Path
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, guess_lexer, TextLexer
    from pygments.formatters import HtmlFormatter
    from pygments.styles import get_all_styles
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False

from markdown import markdown as md_convert
from markdown.extensions.extra import ExtraExtension
from .theme_manager import ThemeManager
from .markdown_formatter import MarkdownFormatter

_IS_WINDOWS = platform.system() == 'Windows'

class DocumentModel:
    """
    Se encarga de procesar el texto Markdown, extraer metadatos
    y generar el código HTML final inyectando el tema y KaTeX.
    """
    def __init__(self):
        self.highlight_css = self._generate_highlight_css()

    def format_markdown(self, md_text: str) -> str:
        """Formatea el Markdown preservando fórmulas LaTeX y extensiones."""
        return MarkdownFormatter.format_text(md_text)

    def _generate_highlight_css(self):
        if not PYGMENTS_AVAILABLE:
            return ""
        try:
            return HtmlFormatter(style='monokai').get_style_defs('.codehilite')
        except Exception:
            return ""

    def extract_metadata(self, md_text: str) -> tuple[str, str, str]:
        title = ""
        subject = ""
        authors = ""
        m = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
        if m:
            title = self._strip_markdown(m.group(1).strip())
        m = re.search(r'\*\*Materia:\*\*\s*(.+?)(?:\n|$)', md_text)
        if m:
            subject = self._strip_markdown(m.group(1).strip())
        m = re.search(r'\*\*Integrantes:\*\*\s*(.+?)(?:\n|$)', md_text)
        if m:
            authors = self._strip_markdown(m.group(1).strip())
        return title, subject, authors

    def _strip_markdown(self, text: str) -> str:
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'\*(.+?)\*', r'\1', text)
        text = re.sub(r'__(.+?)__', r'\1', text)
        text = re.sub(r'_(.+?)_', r'\1', text)
        text = re.sub(r'~~(.+?)~~', r'\1', text)
        text = re.sub(r'`(.+?)`', r'\1', text)
        text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
        return text

    def _normalize_list_indent(self, text: str) -> str:
        lines = text.split('\n')
        result = []
        for line in lines:
            m = re.match(r'^(\s*)([-*+]|\d+\.)\s', line)
            if m:
                indent = len(m.group(1))
                if indent > 0:
                    new_indent = ((indent + 3) // 4) * 4
                    line = ' ' * new_indent + line[indent:]
            result.append(line)
        return '\n'.join(result)

    def _protect_latex(self, text: str):
        display_maths = []
        inline_maths = []
        def _capture_display(m):
            display_maths.append(m.group(1))
            return f"\x00MATH_D_{len(display_maths) - 1}\x00"
        text = re.sub(r'\$\$(.*?)\$\$', _capture_display, text, flags=re.DOTALL)
        def _capture_inline(m):
            inline_maths.append(m.group(1))
            return f"\x00MATH_I_{len(inline_maths) - 1}\x00"
        text = re.sub(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)', _capture_inline, text)
        return text, display_maths, inline_maths

    def _restore_latex(self, html: str, display_maths: list, inline_maths: list, server_rendered: bool):
        for i, expr in enumerate(display_maths):
            placeholder = f"\x00MATH_D_{i}\x00"
            if server_rendered:
                html = html.replace(placeholder, expr)
            else:
                replacement = f'<div class="math-display">$$\n{expr}\n$$</div>'
                p_pattern = re.compile(rf'<p>\s*{re.escape(placeholder)}\s*</p>', re.DOTALL)
                if p_pattern.search(html):
                    html = p_pattern.sub(lambda m: replacement, html)
                else:
                    html = html.replace(placeholder, replacement)
        for i, expr in enumerate(inline_maths):
            placeholder = f"\x00MATH_I_{i}\x00"
            if server_rendered:
                html = html.replace(placeholder, expr)
            else:
                html = html.replace(
                    placeholder,
                    f'<span class="math-inline">${expr}$</span>'
                )
        return html

    def _clean_pandoc_attributes(self, text: str) -> str:
        text = re.sub(r'^\s*(<!--\s*PAGE-?BREAK\s*-->|[-=]{3,}\s*PAGE-?BREAK\s*[-=]{3,})\s*$', r'<div class="page-break"></div>', text, flags=re.MULTILINE | re.IGNORECASE)
        text = re.sub(r'\\{1,2}(newpage|pagebreak)', r'<div class="page-break"></div>', text)
        text = re.sub(r'<div[^>]*style="[^"]*page-break-[^"]*"[^>]*>\s*</div>', r'<div class="page-break"></div>', text)
        text = re.sub(r'(!\[[^\]]*\]\([^)]*\))\s*\{[^}]*\}', r'\1', text)
        text = re.sub(r'\[([^\]]*)\]\{[^}]*\}', r'\1', text)
        text = re.sub(r'^(#{1,6}\s+.*?)\s*\{[^}]*\}\s*$', r'\1', text, flags=re.MULTILINE)
        text = re.sub(r'^\s*\{[^}]*\}\s*$', '', text, flags=re.MULTILINE)
        return text

    def _process_highlights(self, text: str) -> str:
        from mvc.models.theme_manager import PASTEL_COLORS
        default_color = PASTEL_COLORS['amarillo']
        def _repl_with_color(m):
            content = m.group(1)
            color_param = m.group(2).lower().strip()
            hex_color = PASTEL_COLORS.get(color_param, color_param if color_param.startswith('#') else default_color)
            return f'<mark style="background-color: {hex_color}; padding: 1px 5px; border-radius: 4px; color: inherit;">{content}</mark>'
        text = re.sub(r'==((?:(?!==).)+?)==\(([^)]+)\)', _repl_with_color, text, flags=re.DOTALL)
        def _repl_default(m):
            content = m.group(1)
            return f'<mark style="background-color: {default_color}; padding: 1px 5px; border-radius: 4px; color: inherit;">{content}</mark>'
        text = re.sub(r'==((?:(?!==).)+?)==', _repl_default, text, flags=re.DOTALL)
        return text

    def _get_mermaid_theme_config(self, theme_key: str) -> dict:
        t = ThemeManager.get_theme(theme_key)
        font_family = t.get('font_family_content', "'Inter', sans-serif").replace("'", "").split(",")[0].strip()
        
        # Notion-style clean, elegant theme variables
        theme_vars = {
            'fontFamily': font_family + ', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            'fontSize': '12px',
            
            # Nodes (Clean Notion white boxes with subtle crisp border)
            'primaryColor': '#FFFFFF',
            'primaryTextColor': '#1F2937',
            'primaryBorderColor': '#D1D5DB',
            'nodeBorder': '#D1D5DB',
            'nodeTextColor': '#1F2937',
            
            # Lines and arrows
            'lineColor': '#6B7280',
            'arrowheadColor': '#6B7280',
            
            # Subgraphs / Clusters
            'clusterBkg': '#F9FAFB',
            'clusterBorder': '#E5E7EB',
            'titleColor': '#374151',
            
            # Secondary / Tertiary
            'secondaryColor': '#F3F4F6',
            'tertiaryColor': '#FFFFFF',
            'mainBkg': '#FFFFFF',
            
            # Edge Labels
            'edgeLabelBackground': '#FFFFFF',
            'labelTextColor': '#4B5563',
            'labelBoxBkgColor': '#FFFFFF',
            'labelBoxBorderColor': '#E5E7EB',
            
            # Sequence diagram actors & signals
            'actorBorder': '#D1D5DB',
            'actorBkg': '#FFFFFF',
            'actorTextColor': '#1F2937',
            'actorLineColor': '#9CA3AF',
            'signalColor': '#6B7280',
            'signalTextColor': '#374151',
            'loopTextColor': '#374151',
            
            # Notes
            'noteBorderColor': '#FDE68A',
            'noteBkgColor': '#FEF9C3',
            'noteTextColor': '#78350F',
            
            # Class diagrams
            'classText': '#1F2937',
        }
        return {
            "theme": "base",
            "themeVariables": theme_vars,
            "flowchart": {
                "padding": 16,
                "nodeSpacing": 45,
                "rankSpacing": 45,
                "htmlLabels": True,
                "useMaxWidth": False,
                "curve": "basis"
            },
            "sequence": {
                "diagramMarginX": 30,
                "diagramMarginY": 20,
                "actorMargin": 50,
                "width": 140,
                "height": 45,
                "boxMargin": 10,
                "boxTextMargin": 5,
                "noteMargin": 10,
                "messageMargin": 35,
                "mirrorActors": False,
                "useMaxWidth": False
            },
            "class": {
                "useMaxWidth": False
            },
            "state": {
                "useMaxWidth": False
            },
            "er": {
                "useMaxWidth": False
            }
        }

    def _process_mermaid_diagrams(self, md_text: str, theme_key: str) -> str:
        """Replace mermaid fenced blocks with placeholders before markdown processing."""
        import html as html_mod
        self._mermaid_blocks = {}
        counter = [0]
        def _replace_mermaid(match):
            code = match.group(1).strip()
            placeholder = f'<!--MERMAID_PLACEHOLDER_{counter[0]}-->'
            self._mermaid_blocks[placeholder] = f'<pre class="mermaid">{html_mod.escape(code)}</pre>'
            counter[0] += 1
            return placeholder
        return re.sub(r'```mermaid\s*\n(.*?)\n```', _replace_mermaid, md_text, flags=re.DOTALL | re.IGNORECASE)

    def _restore_mermaid_diagrams(self, html: str) -> str:
        """Restore mermaid placeholders with actual <pre class='mermaid'> tags after markdown processing."""
        for placeholder, mermaid_html in getattr(self, '_mermaid_blocks', {}).items():
            html = html.replace(placeholder, mermaid_html)
        return html

    def process_markdown(self, md_text: str, theme_key: str = 'minimal') -> tuple[str, bool]:
        safe_text = self._clean_pandoc_attributes(md_text)
        safe_text = self._process_highlights(safe_text)
        safe_text = self._process_mermaid_diagrams(safe_text, theme_key=theme_key)
        safe_text = self._normalize_list_indent(safe_text)

        server_katex = False
        katex_ext = None
        try:
            from markdown_katex import KatexExtension
            katex_ext = KatexExtension()
            server_katex = True
        except ImportError:
            pass

        extensions = ['markdown.extensions.extra', 'pymdownx.tilde', 'pymdownx.caret', 'pymdownx.tasklist', 'fenced_code', 'codehilite']
        extension_configs = {'codehilite': {'css_class': 'codehilite', 'use_pygments': True, 'linenums': False}}

        if server_katex:
            extensions.append(katex_ext)
            html = md_convert(safe_text, extensions=extensions, extension_configs=extension_configs)
        else:
            safe, disp_maths, inl_maths = self._protect_latex(safe_text)
            html = md_convert(safe, extensions=extensions, extension_configs=extension_configs)
            html = self._restore_latex(html, disp_maths, inl_maths, server_rendered=False)

        html = re.sub(r'^<h1>.*?</h1>\s*', '', html, count=1, flags=re.DOTALL)
        html = re.sub(r'^<p><strong>Integrantes:</strong>.*?</p>\s*', '', html, count=1, flags=re.DOTALL | re.IGNORECASE)

        # Restore mermaid blocks after markdown processing
        html = self._restore_mermaid_diagrams(html)

        import os
        base_dir = os.getcwd()
        def make_absolute_uri(match):
            src = match.group(1)
            if src.startswith(('http://', 'https://', 'data:', 'file://')) or os.path.isabs(src): return match.group(0)
            file_uri = Path(os.path.normpath(os.path.join(base_dir, src))).as_uri()
            return f'src="{file_uri}"'
        html = re.sub(r'src="([^"]+)"', make_absolute_uri, html)
        return html, server_katex

    def get_pygments_css(self, theme_key: str) -> str:
        try:
            from pygments.formatters import HtmlFormatter
            theme = ThemeManager.get_theme(theme_key)
            return HtmlFormatter(style=theme.get('pygments_style', 'monokai')).get_style_defs('.codehilite')
        except: return ""

    def _clean_redundant_pagebreaks(self, html: str, has_cover: bool = True) -> str:
        if not html: return html
        # Fix ReDoS by using a literal marker instead of complex regex
        html = re.sub(r'<div[^>]*class="[^"]*page-break[^"]*"[^>]*>\s*</div>', 
                      r'<!--PAGE_BREAK-->', html, flags=re.IGNORECASE)
                      
        if has_cover:
            html = re.sub(r'^\s*(?:<!--PAGE_BREAK-->|<p>\s*</p>|\s+)+', '', html, flags=re.IGNORECASE)
            
        html = re.sub(r'(?:<!--PAGE_BREAK-->\s*(?:<p>\s*</p>\s*)*){2,}', r'<!--PAGE_BREAK-->', html, flags=re.IGNORECASE)
        html = re.sub(r'(?:<!--PAGE_BREAK-->|<p>\s*</p>|\s+)+$', '', html, flags=re.IGNORECASE)
        
        html = html.replace('<!--PAGE_BREAK-->', '<div class="page-break" style="page-break-after: always; break-after: page;"></div>')
        return html

    def _inject_toc(self, md_text: str) -> str:
        if not re.search(r'<!--\s*TOC\s*-->', md_text, re.IGNORECASE): return md_text
        headings = []
        for line in md_text.splitlines():
            match = re.match(r'^(#{1,3})\s+(.+?)\s*#*\s*$', line)
            if match: headings.append((len(match.group(1)), self._strip_markdown(match.group(2))))
        rows = ['<nav class="toc"><h2>Índice</h2><ol>']
        for idx, (level, title) in enumerate(headings):
            rows.append(f'<li class="toc-level-{level}"><a href="#toc-heading-{idx}">{title}</a><span class="toc-page" data-target="toc-heading-{idx}">…</span></li>')
        rows.append('</ol></nav>')
        return re.sub(r'<!--\s*TOC\s*-->', '\n'.join(rows), md_text, flags=re.IGNORECASE)

    def _add_heading_ids(self, html: str) -> str:
        index = 0
        def repl(match):
            nonlocal index
            result = f'<h{match.group(1)} id="toc-heading-{index}"{match.group(2)}>'
            index += 1
            return result
        return re.sub(r'<h([1-3])(\s*)>', repl, html)

    def _build_logo_html(self, show_cover: bool, show_logo: bool, logo_position: str = 'top-left') -> str:
        if not (show_cover and show_logo):
            return ""
        import os
        logo_path = None
        for candidate in ["assets/logo.png", "assets/UADER_logo.png"]:
            candidate_abs = os.path.normpath(os.path.join(os.getcwd(), candidate))
            if os.path.exists(candidate_abs):
                logo_path = candidate_abs
                break
        if not logo_path and os.path.exists(os.path.join(os.getcwd(), "assets")):
            assets_dir = os.path.join(os.getcwd(), "assets")
            files = [f for f in os.listdir(assets_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.svg'))]
            if files:
                logo_path = os.path.join(assets_dir, files[0])
        if logo_path:
            logo_uri = Path(logo_path).as_uri()
            return f'<img src="{logo_uri}" class="cover-logo logo-{logo_position}" alt="Logo Facultad">'
        return ""

    def _build_cover_html(self, show_cover: bool, doc_title: str, subtitle: str = '',
                          subject: str = '', authors: str = '', profesores: str = '',
                          logo_html: str = '', cover_style: str = 'sidebar_logo') -> str:
        if not (show_cover and doc_title):
            return ""
        sub_str, subj_str, auth_str, prof_str = subtitle.strip(), subject.strip(), authors.strip(), profesores.strip()
        meta = ''.join(
            f'<div class="cover-meta-row"><span>{label}</span><b>{value}</b></div>'
            for label, value in [('Materia', subj_str), ('Integrantes', auth_str), ('Docentes', prof_str)] if value
        )
        subtitle_html = f'<p class="cover-subtitle">{sub_str}</p>' if sub_str else ''
        style = cover_style if cover_style in {
            'sidebar_logo', 'academica_clasica', 'corporativa', 'bloque_color', 'marco_fino', 'folio'
        } else 'sidebar_logo'
        return f'''<div class="page cover-page cover-style-{style}">
          <div class="cover-header">{logo_html}</div>
          <div class="cover-content"><h1>{doc_title}</h1>{subtitle_html}</div>
          <div class="cover-meta">{meta}</div>
        </div>'''

    def render_preview_content(self, md_text: str, theme_key: str = 'minimal', show_cover: bool = True,
                               subtitle: str = '', materia: str = '', integrantes: str = '', profesores: str = '',
                               show_logo: bool = False, logo_position: str = 'top-left',
                               cover_style: str = 'sidebar_logo', title: str = '') -> str:
        """
        Genera únicamente el HTML interno del cuerpo (portada + markdown procesado)
        para inyección directa via JavaScript sin recargar la página.
        """
        if not md_text or not md_text.strip():
            return '<div id="paginate-content"><p style="color:var(--muted-color);padding:22mm;">Escribí Markdown aquí…</p></div>'

        md_text = self._inject_toc(md_text)
        body_html, _ = self.process_markdown(md_text, theme_key=theme_key)
        body_html = self._add_heading_ids(body_html)
        md_title, md_subject, md_authors = self.extract_metadata(md_text)

        doc_title = title.strip() if title.strip() else (md_title if md_title else "Documento")
        subject = materia.strip() if materia.strip() else md_subject
        authors = integrantes.strip() if integrantes.strip() else md_authors

        has_cover = bool(show_cover and doc_title)
        body_html = self._clean_redundant_pagebreaks(body_html, has_cover=has_cover)

        logo_html = self._build_logo_html(show_cover, show_logo, logo_position)
        cover_html = self._build_cover_html(
            show_cover, doc_title, subtitle, subject, authors, profesores, logo_html, cover_style
        )

        return f"""{cover_html}
<div id="paginate-content">
{body_html}
</div>"""

    def render_html(self, md_text: str, theme_key: str = 'minimal', show_cover: bool = True,
                    subtitle: str = '', materia: str = '', integrantes: str = '', profesores: str = '',
                    show_logo: bool = False, logo_position: str = 'top-left',
                    cover_style: str = 'sidebar_logo',
                    page_config: dict = None,
                    is_preview: bool = True, title: str = '') -> str:
        
        if not md_text or not md_text.strip():
            body_html = '<div id="paginate-content"><p style="color:var(--muted-color);padding:22mm;">Escribí Markdown aquí…</p></div>' if is_preview else ''
            server_katex = False
            md_title, md_subject, md_authors = "", "", ""
        else:
            md_text = self._inject_toc(md_text)
            body_html, server_katex = self.process_markdown(md_text, theme_key=theme_key)
            body_html = self._add_heading_ids(body_html)
            md_title, md_subject, md_authors = self.extract_metadata(md_text)
            
        doc_title = title.strip() if title.strip() else (md_title if md_title else "Documento")
        subject = materia.strip() if materia.strip() else (md_subject if 'md_subject' in locals() else '')
        authors = integrantes.strip() if integrantes.strip() else (md_authors if 'md_authors' in locals() else '')

        has_cover = bool(show_cover and doc_title)
        body_html = self._clean_redundant_pagebreaks(body_html, has_cover=has_cover)

        logo_html = self._build_logo_html(show_cover, show_logo, logo_position)
        cover_html = self._build_cover_html(
            show_cover, doc_title, subtitle, subject, authors, profesores, logo_html, cover_style
        )

        root_css = ThemeManager.generate_root_css(theme_key) if hasattr(ThemeManager, 'generate_root_css') else ""
        katex_head = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">'
        katex_footer = """<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
        <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
        onload='renderMathInElement(document.body, {delimiters: [{left: "$$", right: "$$", display: true}, {left: "$", right: "$", display: false}], ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"], throwOnError: false});'></script>"""
        katex_footer = katex_footer.replace("});", "}); window.katexRendered = true; if(window.runPagination) window.runPagination();")

        if is_preview:
            content_wrap = f'<div id="preview-container">\n{cover_html}\n<div id="paginate-content">\n{body_html}\n</div>\n</div>'
        else:
            content_wrap = f'{cover_html}\n<div id="paginate-content">\n{body_html}\n</div>'

        core_css = self._get_core_css(is_preview)
        pygments_css = self.get_pygments_css(theme_key)
        
        fonts_head = """<link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Figtree:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&family=Manrope:wght@400;500;600;700;800&family=Outfit:wght@500;600;700;800&family=Poppins:wght@600;700;800&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
        <link href="https://api.fontshare.com/v2/css?f[]=cabinet-grotesk@400;500;700;800&f[]=satoshi@400;500;700&display=swap" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/geist@1/dist/fonts/geist-sans/style.css" rel="stylesheet">"""

        import json as _json
        mermaid_config = self._get_mermaid_theme_config(theme_key)
        mermaid_config_json = _json.dumps(mermaid_config)
        mermaid_script = f"""<script type="module">
        (async () => {{
          try {{
            const {{ default: mermaid }} = await import('https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs');
            window._mermaid = mermaid;
            window._mermaidConfig = {mermaid_config_json};
            mermaid.initialize({{ startOnLoad: false, ...{mermaid_config_json} }});
            await mermaid.run({{ querySelector: 'pre.mermaid, .mermaid' }});

            // Ajuste proporcional para evitar que diagramas compactos se estiren al 100% del ancho
            document.querySelectorAll('pre.mermaid svg').forEach(svg => {{
              if (svg.getAttribute('width') === '100%') {{
                svg.removeAttribute('width');
              }}
              const viewBox = svg.getAttribute('viewBox');
              if (viewBox) {{
                const parts = viewBox.split(/[\\s,]+/).map(Number);
                if (parts.length === 4 && parts[2] > 0) {{
                  svg.style.maxWidth = Math.min(parts[2], 640) + 'px';
                }}
              }}
            }});
          }} catch (e) {{
            console.error('Error inicializando Mermaid:', e);
          }} finally {{
            window.mermaidRendered = true;
            if (window.runPagination) window.runPagination();
          }}
        }})();
        </script>"""

        update_script = """<script>
        window.updateContent = function(newHtml) {
          var container = document.getElementById('preview-container');
          if (!container) return;

          var prevScrollY = window.scrollY;

          // 1. Parsear nuevo contenido en contenedor temporal en memoria
          var temp = document.createElement('div');
          temp.innerHTML = newHtml;

          // 2. Renderizar KaTeX sobre el árbol en memoria
          if (window.renderMathInElement) {
            try {
              renderMathInElement(temp, {
                delimiters: [
                  {left: "$$", right: "$$", display: true},
                  {left: "$", right: "$", display: false}
                ],
                ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"],
                throwOnError: false
              });
            } catch(e) {
              console.error("Error KaTeX update:", e);
            }
          }

          // 3. Paginar en memoria directamente a hojas A4 (.page)
          var fragment = document.createDocumentFragment();
          var coverPage = temp.querySelector('.cover-page');
          if (coverPage) {
            fragment.appendChild(coverPage);
          }

          var src = temp.querySelector('#paginate-content');
          if (src && src.children.length) {
            var children = Array.from(src.children);

            var calcEl = document.createElement('div');
            calcEl.style.cssText = 'position:fixed;left:-9999px;top:0;height:257mm;width:210mm;padding:0 20mm;box-sizing:border-box;visibility:hidden;';
            document.body.appendChild(calcEl);
            var maxPagePx = calcEl.clientHeight || 971;
            document.body.removeChild(calcEl);

            var ruler = document.createElement('div');
            ruler.style.cssText = 'position:fixed;left:-9999px;top:0;width:210mm;padding:0 20mm;box-sizing:border-box;overflow:hidden;font-family:inherit;font-size:inherit;line-height:inherit;';
            document.body.appendChild(ruler);

            var currentPage = document.createElement('div');
            currentPage.className = 'page';
            fragment.appendChild(currentPage);

            for (var i = 0; i < children.length; i++) {
              var el = children[i];
              var isManualBreak = (el.classList && el.classList.contains('page-break'));
              if (isManualBreak) {
                currentPage = document.createElement('div');
                currentPage.className = 'page';
                fragment.appendChild(currentPage);
                ruler.innerHTML = '';
                continue;
              }
              var clone = el.cloneNode(true);
              ruler.appendChild(clone);
              if (ruler.scrollHeight > maxPagePx && currentPage.children.length > 0) {
                ruler.innerHTML = '';
                currentPage = document.createElement('div');
                currentPage.className = 'page';
                fragment.appendChild(currentPage);
                ruler.appendChild(clone);
              }
              currentPage.appendChild(el);
            }
            document.body.removeChild(ruler);
          } else if (src) {
            var emptyPage = document.createElement('div');
            emptyPage.className = 'page';
            emptyPage.appendChild(src);
            fragment.appendChild(emptyPage);
          }

          // 4. Reemplazo atómico: el DOM nunca colapsa a altura 0
          container.replaceChildren(fragment);

          // 5. Preservar y restaurar la posición de scroll exacta
          if (prevScrollY > 0) {
            window.scrollTo(0, prevScrollY);
            requestAnimationFrame(function() {
              window.scrollTo(0, prevScrollY);
            });
          }

          // 6. Re-renderizar diagramas Mermaid si existen
          if (window._mermaid) {
            try {
              var mermaids = container.querySelectorAll('pre.mermaid, .mermaid');
              if (mermaids.length > 0) {
                mermaids.forEach(function(el) {
                  el.removeAttribute('data-processed');
                });
                window._mermaid.run({ querySelector: '#preview-container pre.mermaid, #preview-container .mermaid' }).then(function() {
                  container.querySelectorAll('pre.mermaid svg').forEach(function(svg) {
                    if (svg.getAttribute('width') === '100%') {
                      svg.removeAttribute('width');
                    }
                    var viewBox = svg.getAttribute('viewBox');
                    if (viewBox) {
                      var parts = viewBox.split(/[\\s,]+/).map(Number);
                      if (parts.length === 4 && parts[2] > 0) {
                        svg.style.maxWidth = Math.min(parts[2], 640) + 'px';
                      }
                    }
                  });
                  if (prevScrollY > 0) {
                    window.scrollTo(0, prevScrollY);
                  }
                }).catch(function(e) {
                  console.error("Error Mermaid update:", e);
                });
              }
            } catch(e) {
              console.error("Error Mermaid update:", e);
            }
          }
        };
        </script>""" if is_preview else ""

        return f"""<!DOCTYPE html>
        <html lang="es">
        <head>
          <meta charset="UTF-8">
          <title>{doc_title}</title>
          {fonts_head}
          {katex_head}
          <style>
          {root_css}
          {core_css}
          {pygments_css}
          pre.mermaid {{
              text-align: center;
              background: transparent !important;
              border: none !important;
              padding: 4mm 0 !important;
              margin: 4mm auto !important;
              page-break-inside: avoid !important;
              break-inside: avoid !important;
              display: flex;
              justify-content: center;
              align-items: center;
          }}
          pre.mermaid svg {{
              max-width: 100% !important;
              max-height: 115mm !important;
              width: auto !important;
              height: auto !important;
              display: block !important;
              margin: 0 auto !important;
          }}
          /* Notion aesthetic enhancements */
          pre.mermaid .node rect,
          pre.mermaid .node polygon,
          pre.mermaid .node circle {{
              rx: 6px !important;
              ry: 6px !important;
              stroke-width: 1.25px !important;
              filter: drop-shadow(0 1px 2px rgba(0,0,0,0.04));
          }}
          pre.mermaid .cluster rect {{
              rx: 8px !important;
              ry: 8px !important;
              stroke-width: 1px !important;
              stroke-dasharray: 4 4 !important;
          }}
          pre.mermaid .edgeLabel {{
              border-radius: 4px !important;
              padding: 2px 6px !important;
              font-size: 11px !important;
              background: #ffffff !important;
              box-shadow: 0 1px 2px rgba(0,0,0,0.05);
          }}
          pre.mermaid .edgePath .path {{
              stroke-width: 1.5px !important;
          }}
          </style>
        </head>
        <body class="theme-{theme_key}">
          {content_wrap}
          {katex_footer}
          {mermaid_script}
          {update_script}
          {self._get_pagination_script()}
        </body>
        </html>"""

    def _get_core_css(self, is_preview: bool) -> str:
        css = """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html, body { width: 100%; font-family: var(--font-family-content, 'Inter', sans-serif); color: var(--text-color, #333); font-size: 11pt; line-height: 1.6; }
        
        .cover-page { position: relative !important; overflow: hidden !important; background: var(--page-bg, #fff); }
        .toc { margin: 0 0 10mm; padding: 7mm 9mm; border: 1px solid var(--accent-color, #ccc); border-radius: 5px; }
        .toc h2 { border: 0; margin: 0 0 4mm; }
        .toc ol { list-style: none; padding: 0; }
        .toc li { display: flex; gap: 8px; border-bottom: 1px dotted var(--muted-color, #888); padding: 2px 0; }
        .toc a { color: inherit; text-decoration: none; flex: 1; }
        .toc-page { min-width: 1.5em; text-align: right; }
        .cover-logo { position: absolute !important; max-width: 120px !important; max-height: 80px !important; width: auto; height: auto; object-fit: contain; z-index: 10; }
        .logo-top-left { top: 20mm; left: 20mm; }
        .logo-top-right { top: 20mm; right: 20mm; }
        .logo-bottom-left { bottom: 20mm; left: 20mm; }
        .logo-bottom-right { bottom: 20mm; right: 20mm; }

        /* --- NUEVAS PORTADAS ACADÉMICAS / PROFESIONALES --- */

        /* 1. Sidebar Logo (Banda Izquierda con Logo, totalmente centrada en la barra) */
        .cover-page.cover-style-sidebar_logo {
            display: flex !important;
            flex-direction: column !important;
            padding: 0 !important;
            min-height: 297mm !important;
            position: relative !important;
        }
        .cover-style-sidebar_logo::before {
            content: "";
            position: absolute; left: 0; top: 0; bottom: 0;
            width: 45mm; /* Barra gruesa */
            background-color: #1a4f76; /* Azul UADER/Institucional */
            z-index: 1;
        }
        .cover-style-sidebar_logo .cover-header {
            position: absolute;
            left: 0; top: 0;
            width: 45mm; height: 100%;
            z-index: 2; padding: 0; margin: 0;
            pointer-events: none;
        }
        .cover-style-sidebar_logo .cover-logo {
            position: absolute !important;
            top: 45mm !important;
            left: 22.5mm !important;
            transform: translateX(-50%) !important;
            max-width: 32mm !important;
            max-height: 60mm !important;
            width: auto !important;
            height: auto !important;
            padding: 4mm !important;
            margin: 0 !important;
            background: #ffffff !important;
            border-radius: 6px !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.18) !important;
            object-fit: contain !important;
        }
        .cover-style-sidebar_logo .cover-kicker { display: none !important; }
        .cover-style-sidebar_logo .cover-content {
            margin-left: 45mm;
            width: calc(100% - 45mm);
            margin-top: 80mm !important;
            padding: 0 20mm;
            text-align: center;
        }
        .cover-style-sidebar_logo .cover-content h1 {
            font-size: 38pt;
            color: #111827 !important;
            border: none !important; /* Sin puntos ni lineas debajo del titulo */
            margin-bottom: 5mm;
            font-family: 'Inter', sans-serif;
            font-weight: 800;
        }
        .cover-style-sidebar_logo .cover-subtitle {
            font-size: 16pt; color: #4b5563; font-weight: 500;
        }
        .cover-style-sidebar_logo .cover-meta {
            margin-left: 45mm;
            width: calc(100% - 45mm);
            position: absolute; bottom: 40mm;
            padding: 0 20mm;
            text-align: center;
            display: flex; flex-direction: column; align-items: center; gap: 8mm;
        }
        .cover-style-sidebar_logo .cover-meta-row {
            border: none !important; display: flex; flex-direction: column; align-items: center; gap: 2mm;
        }
        .cover-style-sidebar_logo .cover-meta-row span {
            font-weight: bold; color: #111827; font-size: 11pt; text-transform: uppercase; letter-spacing: 1px;
        }
        .cover-style-sidebar_logo .cover-meta-row b {
            font-weight: normal; color: #374151; font-size: 12pt;
        }

        /* 2. Académica Clásica (Estilo Tesis Formal) */
        .cover-style-academica_clasica {
            display: flex !important; flex-direction: column !important; align-items: center !important; text-align: center;
            padding: 40mm 30mm !important;
            border-top: 2px solid #111827; border-bottom: 2px solid #111827;
            margin: 15mm; height: calc(100% - 30mm); box-sizing: border-box;
        }
        .cover-style-academica_clasica .cover-header { justify-content: center; width: 100%; margin-bottom: 25mm; display:flex; flex-direction: column; align-items: center;}
        .cover-style-academica_clasica .cover-header .cover-logo { position: static !important; max-width: 45mm !important; margin-bottom: 10mm; display: block; }
        .cover-style-academica_clasica .cover-content { margin-top: auto; margin-bottom: auto; }
        .cover-style-academica_clasica .cover-content h1 { font-family: 'Inter', sans-serif; font-size: 36pt; border: none !important; font-weight: 700; color: #111827 !important;}
        .cover-style-academica_clasica .cover-meta { display: flex; flex-direction: column; align-items: center; gap: 6mm; border-top: 1px solid #d1d5db; padding-top: 10mm; width: 80%; margin-top: auto; }
        .cover-style-academica_clasica .cover-meta-row { border: none !important; display: flex; flex-direction: column; align-items: center; }

        /* 3. Corporativa Moderna (Limpia, Alineación Izquierda) */
        .cover-style-corporativa {
            padding: 40mm 30mm !important; display: flex !important; flex-direction: column !important;
        }
        .cover-style-corporativa .cover-header { margin-bottom: 40mm; position: relative;}
        .cover-style-corporativa .cover-header .cover-logo { position: static !important; max-width: 50mm !important;}
        .cover-style-corporativa .cover-content { text-align: left; border-left: 2.5mm solid #2563eb; padding-left: 10mm; }
        .cover-style-corporativa .cover-content h1 { font-size: 42pt; text-align: left; border: none !important; line-height: 1.1; margin-bottom: 8mm; color: #0f172a !important; letter-spacing: -1px;}
        .cover-style-corporativa .cover-subtitle { font-size: 18pt; color: #64748b; }
        .cover-style-corporativa .cover-meta { position: absolute; bottom: 40mm; left: 40mm; width: calc(100% - 80mm); display: flex; justify-content: flex-start; gap: 20mm; flex-wrap: wrap; }
        .cover-style-corporativa .cover-meta-row { border: none !important; display: flex; flex-direction: column; }
        .cover-style-corporativa .cover-meta-row span { color: #94a3b8; font-size: 10pt; text-transform: uppercase; margin-bottom: 2px;}

        /* 4. Bloque Superior Color */
        .cover-style-bloque_color {
            padding: 0 !important; position: relative;
        }
        .cover-style-bloque_color::before {
            content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 45%; background-color: #1e293b; z-index: 1;
        }
        .cover-style-bloque_color .cover-header { position: absolute; top: 20mm; left: 20mm; z-index: 2; color: #fff; width: 100%;}
        .cover-style-bloque_color .cover-header .cover-logo { position: static !important; background: white; padding: 4mm; border-radius: 4px; max-width: 40mm !important; display: inline-block;}
        .cover-style-bloque_color .cover-content { position: absolute; top: 22%; left: 20mm; right: 20mm; z-index: 2; color: #fff; }
        .cover-style-bloque_color .cover-content h1 { color: #ffffff !important; font-size: 40pt; border: none !important; font-weight: 800; line-height: 1.1;}
        .cover-style-bloque_color .cover-subtitle { color: #94a3b8; font-size: 16pt; margin-top: 5mm;}
        .cover-style-bloque_color .cover-meta { position: absolute; top: 52%; left: 20mm; width: calc(100% - 40mm); display: grid; grid-template-columns: 1fr 1fr; gap: 10mm; color: #111827; }
        .cover-style-bloque_color .cover-meta-row { border: none !important; border-bottom: 1px solid #cbd5e1 !important; display: block; padding-bottom: 4mm; }
        .cover-style-bloque_color .cover-meta-row span { color: #64748b; font-size: 10pt; display: block; text-transform: uppercase;}

        /* 5. Elegancia Minimalista (Marco Fino) */
        .cover-style-marco_fino {
            padding: 25mm !important; position: relative; display: flex !important; flex-direction: column !important;
        }
        .cover-style-marco_fino::after {
            content: ""; position: absolute; top: 15mm; bottom: 15mm; left: 15mm; right: 15mm; border: 1px solid #9ca3af; pointer-events: none;
        }
        .cover-style-marco_fino .cover-header { display: flex; justify-content: center; align-items: center; flex-direction: column; margin-bottom: 30mm; margin-top: 10mm;}
        .cover-style-marco_fino .cover-header .cover-logo { position: static !important; display: block; margin: 0 auto; max-width: 45mm !important;}
        .cover-style-marco_fino .cover-content { text-align: center; margin-top: 30mm;}
        .cover-style-marco_fino .cover-content h1 { font-family: 'Inter', sans-serif; font-weight: 300; font-size: 38pt; border: none !important; letter-spacing: -1px; color: #1f2937 !important;}
        .cover-style-marco_fino .cover-subtitle { font-style: italic; color: #6b7280; }
        .cover-style-marco_fino .cover-meta { position: absolute; bottom: 35mm; left: 30mm; right: 30mm; text-align: center; display: flex; justify-content: space-around;}
        .cover-style-marco_fino .cover-meta-row { border: none !important; display: flex; flex-direction: column; gap: 2mm;}
        .cover-style-marco_fino .cover-meta-row span { color: #9ca3af; letter-spacing: 2px; font-size: 9pt;}

        h1, h2, h3, h4, h5, h6 { font-family: var(--font-family-headings, 'Inter', sans-serif); color: var(--heading-color, #111); margin-top: 0; page-break-after: avoid !important; break-after: avoid !important; }
        h1 { font-size: 20pt; font-weight: 700; line-height: 1.25; margin-top: 10mm; margin-bottom: 4mm; border-bottom: var(--h1-border-width, 1px) solid var(--h1-border-color, #ccc); padding-bottom: 2mm; }
        h2 { font-size: 15pt; font-weight: 700; line-height: 1.3; margin-top: 7.5mm; margin-bottom: 3mm; }
        h3 { font-size: 13pt; font-weight: 600; line-height: 1.35; margin-top: 5.5mm; margin-bottom: 2.5mm; }
        h4 { font-size: 12pt; font-weight: 600; line-height: 1.4; margin-top: 4.5mm; margin-bottom: 2mm; color: var(--heading-color, #111); }
        h5 { font-size: 10.5pt; font-weight: 600; line-height: 1.4; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 3.5mm; margin-bottom: 1.5mm; color: var(--muted-color, #64748b); }
        h6 { font-size: 10pt; font-weight: 600; font-style: italic; line-height: 1.4; margin-top: 3mm; margin-bottom: 1.5mm; color: var(--muted-color, #64748b); }
        p { margin-bottom: 3mm; }

        /* Listas — jerarquía visual correcta */
        ul, ol { margin: 2mm 0; padding-left: 8mm; }
        ul ul, ol ol, ul ol, ol ul { margin: 1mm 0; padding-left: 6mm; }
        ul ul ul, ol ol ol, ul ol ul, ol ul ol { padding-left: 5mm; }
        li { margin-bottom: 1.5mm; }
        li > ul, li > ol { margin-top: 1mm; }
        ul { list-style-type: disc; }
        ul ul { list-style-type: circle; }
        ul ul ul { list-style-type: square; }

        /* Task lists (pymdownx.tasklist) */
        ul.task-list { list-style: none; padding-left: 4mm; }
        ul.task-list li { position: relative; }
        
        .codehilite, .highlight { border-radius: 8px; padding: 12px 18px; margin: 14px 0; overflow: visible !important; border: 1px solid var(--code-border, #313244); font-size: 9.5pt; line-height: 1.5; background: var(--code-bg, #1e1e2e) !important; color: var(--code-color, #cdd6f4) !important; page-break-inside: avoid !important; break-inside: avoid !important; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
        .codehilite pre, .highlight pre { margin: 0; padding: 0; background: transparent !important; color: inherit !important; }
        pre, code { font-family: 'JetBrains Mono', monospace !important; }
        
        /* Estilos de código inline según la paleta del tema */
        :not(pre) > code {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 0.88em !important;
            background-color: var(--inline-code-bg, #f3f4f6) !important;
            color: var(--inline-code-color, #d63384) !important;
            border: 1px solid var(--inline-code-border, #e1e4e8) !important;
            padding: 1.5px 5.5px !important;
            border-radius: 4px !important;
            word-break: break-word !important;
            vertical-align: baseline;
        }
        blockquote { border-left: 4px solid var(--accent-color, #ccc); padding: 8px 16px; margin: 12px 0; background: rgba(0,0,0,0.02); border-radius: 0 8px 8px 0; font-style: italic; }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
            font-size: 9.5pt;
            page-break-inside: auto;
        }
        tr {
            page-break-inside: avoid !important;
            break-inside: avoid !important;
        }
        th, td {
            padding: 8px 12px;
            border: 1px solid var(--table-border, #e5e7eb);
            text-align: left;
            vertical-align: middle;
        }
        th {
            background-color: var(--table-header-bg, #27272a) !important;
            color: var(--table-header-fg, #ffffff) !important;
            font-weight: 600;
            letter-spacing: 0.2px;
            border-color: var(--table-header-bg, #27272a) !important;
        }
        tbody tr:nth-child(even) {
            background-color: var(--table-row-even-bg, #fafafa);
        }
        
        .page-break { page-break-after: always !important; break-after: page !important; }
        @media print { .page-break { page-break-after: always !important; break-after: page !important; } }
        @page { size: A4; margin: 0; }
        
        img { max-width: 100%; height: auto; display: block; margin: 6mm auto; page-break-inside: avoid !important; break-inside: avoid !important; }
        .math-display { text-align: center; margin: 4mm 0; overflow-x: auto; page-break-inside: avoid !important; break-inside: avoid !important; }
        """
        if is_preview:
            css += """
            body { background: #e5e5e5; padding: 40px 0; display: flex; flex-direction: column; align-items: center; overflow-x: hidden; overflow-y: auto; }
            #preview-container { width: 100%; display: flex; flex-direction: column; align-items: center; }
            #paginate-content { width: 210mm; min-height: 297mm; box-sizing: border-box; background: #fff; padding: 20mm; margin-bottom: 40px; box-shadow: 0 8px 32px rgba(0,0,0,0.35); flex-shrink: 0; }
            .page { width: 210mm; min-height: 297mm; box-sizing: border-box; background: #fff; padding: 20mm; margin-bottom: 40px; box-shadow: 0 8px 32px rgba(0,0,0,0.35); flex-shrink: 0; }
            .cover-page { padding: 40mm 20mm !important; }
            .cover-page.cover-style-sidebar_logo, .cover-page.cover-style-bloque_color { padding: 0 !important; }
            """
        else:
            css += """
            html, body { width: 210mm; margin: 0; padding: 0; background-color: #fff !important; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
            .page { width: 210mm; min-height: 297mm; height: 297mm; box-sizing: border-box; background-color: #fff !important; padding: 20mm; margin: 0; page-break-after: always !important; break-after: page !important; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
            .cover-page { padding: 40mm 20mm !important; }
            .cover-page.cover-style-sidebar_logo, .cover-page.cover-style-bloque_color { padding: 0 !important; }
            """
        return css

    def _get_pagination_script(self):
        return """<script>
        (function() {
          'use strict';
          window.katexRendered = window.katexRendered || false;
          window.mermaidRendered = window.mermaidRendered || false;
          window.paginationDone = false;
          var _paginateTimer = null;

          function hasMermaid() {
            return document.querySelectorAll('pre.mermaid, .mermaid').length > 0;
          }

          function paginate() {
            var container = document.getElementById('preview-container') || document.body;
            var src = document.getElementById('paginate-content');
            if (!src || !src.children.length) return;
            
            // Si hay diagramas mermaid y todavia no se renderizaron, esperar
            if (hasMermaid() && !window.mermaidRendered) {
              return;
            }

            var prevScrollY = window.scrollY;
            var children = Array.from(src.children);
            
            var calcEl = document.createElement('div');
            calcEl.style.cssText = 'position:fixed;left:-9999px;top:0;height:257mm;width:210mm;padding:0 20mm;box-sizing:border-box;visibility:hidden;';
            document.body.appendChild(calcEl);
            var maxPagePx = calcEl.clientHeight || 971;
            document.body.removeChild(calcEl);

            var ruler = document.createElement('div');
            ruler.style.cssText = 'position:fixed;left:-9999px;top:0;width:210mm;padding:0 20mm;box-sizing:border-box;overflow:hidden;font-family:inherit;font-size:inherit;line-height:inherit;';
            document.body.appendChild(ruler);
            
            var fragment = document.createDocumentFragment();
            var cover = container.querySelector('.cover-page');
            if (cover) {
              fragment.appendChild(cover);
            }

            var currentPage = document.createElement('div');
            currentPage.className = 'page';
            fragment.appendChild(currentPage);
            
            for (var i = 0; i < children.length; i++) {
              var el = children[i];
              var isManualBreak = (el.classList && el.classList.contains('page-break'));
              if (isManualBreak) {
                currentPage = document.createElement('div');
                currentPage.className = 'page';
                fragment.appendChild(currentPage);
                ruler.innerHTML = '';
                continue;
              }
              var clone = el.cloneNode(true);
              ruler.appendChild(clone);
              if (ruler.scrollHeight > maxPagePx && currentPage.children.length > 0) {
                ruler.innerHTML = '';
                currentPage = document.createElement('div');
                currentPage.className = 'page';
                fragment.appendChild(currentPage);
                ruler.appendChild(clone);
              }
              currentPage.appendChild(el);
            }
            document.body.removeChild(ruler);

            container.replaceChildren(fragment);
            window.paginationDone = true;

            if (prevScrollY > 0) {
              window.scrollTo(0, prevScrollY);
              requestAnimationFrame(function() {
                window.scrollTo(0, prevScrollY);
              });
            }
          }

          window.schedulePagination = function(delay) {
            if (_paginateTimer) clearTimeout(_paginateTimer);
            _paginateTimer = setTimeout(function() {
              if (document.fonts && document.fonts.ready) {
                document.fonts.ready.then(paginate);
              } else {
                paginate();
              }
            }, delay || 500);
          };

          window.runPagination = function() {
            window.schedulePagination(30);
          };

          window.addEventListener('load', function() {
            window.runPagination();
          });

          // Fallback de seguridad: si mermaid o fonts tardan mas de 2.5s, forzar paginacion
          setTimeout(function() {
            window.mermaidRendered = true;
            window.runPagination();
          }, 2500);
        })();
        </script>"""