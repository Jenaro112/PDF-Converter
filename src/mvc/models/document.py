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

_IS_WINDOWS = platform.system() == 'Windows'

class DocumentModel:
    """
    Se encarga de procesar el texto Markdown, extraer metadatos
    y generar el código HTML final inyectando el tema y KaTeX.
    """
    def __init__(self):
        self.highlight_css = self._generate_highlight_css()

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
        font_map = {'minimal': 'Space Grotesk, sans-serif', 'classic': 'Literata, serif', 'institutional': 'Inter, sans-serif', 'editorial': 'Inter, sans-serif', 'blueprint': 'IBM Plex Sans, sans-serif', 'pastel': 'Poppins, sans-serif'}
        font_family = font_map.get(theme_key, 'Inter, sans-serif')
        theme_vars_map = {
            'minimal': {'fontFamily': font_family, 'fontSize': '13px', 'nodePadding': '20', 'primaryColor': '#f4f4f5', 'primaryTextColor': '#1a1a1a', 'primaryBorderColor': '#d4d4d8', 'lineColor': '#3a3a3a', 'secondaryColor': '#e4e4e7', 'tertiaryColor': '#ffffff'},
            'classic': {'fontFamily': font_family, 'fontSize': '13px', 'nodePadding': '20', 'primaryColor': '#f5f0e1', 'primaryTextColor': '#1a1410', 'primaryBorderColor': '#d4c9b0', 'lineColor': '#8b4513', 'secondaryColor': '#f0ebe0', 'tertiaryColor': '#FCFBF4'},
            'institutional': {'fontFamily': font_family, 'fontSize': '13px', 'nodePadding': '20', 'primaryColor': '#f0f4f8', 'primaryTextColor': '#1e3a5f', 'primaryBorderColor': '#cbd5e1', 'lineColor': '#1e3a5f', 'secondaryColor': '#c9a84c', 'tertiaryColor': '#ffffff'}
        }
        vars_dict = theme_vars_map.get(theme_key, theme_vars_map['minimal'])
        return {"theme": "base", "themeVariables": vars_dict, "flowchart": {"padding": 30, "nodeSpacing": 60, "rankSpacing": 60, "htmlLabels": False, "useMaxWidth": False}, "sequence": {"boxPadding": 30, "useMaxWidth": False}}

    def _process_mermaid_diagrams(self, md_text: str, theme_key: str) -> str:
        import hashlib, os, tempfile, json, subprocess, html
        cache_dir = os.path.join(tempfile.gettempdir(), "pdf_converter_mermaid_cache")
        os.makedirs(cache_dir, exist_ok=True)
        def _replace_mermaid(match):
            return f'''<div class="mermaid-fallback-box"><pre><code>{html.escape(match.group(1).strip())}</code></pre></div>'''
        return re.sub(r'```mermaid\s*\n(.*?)\n```', _replace_mermaid, md_text, flags=re.DOTALL | re.IGNORECASE)

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
        pb_pattern = r'<div[^>]*class="[^"]*page-break[^"]*"[^>]*>\s*</div>'
        if has_cover: html = re.sub(r'^\s*(?:' + pb_pattern + r'|<p>\s*</p>|\s+)+', '', html, flags=re.IGNORECASE)
        html = re.sub(r'(?:' + pb_pattern + r'\s*(?:<p>\s*</p>\s*)*){2,}', r'<div class="page-break" style="page-break-after: always; break-after: page;"></div>', html, flags=re.IGNORECASE)
        html = re.sub(r'(?:' + pb_pattern + r'|<p>\s*</p>|\s+)+$', '', html, flags=re.IGNORECASE)
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

    def render_html(self, md_text: str, theme_key: str = 'minimal', show_cover: bool = True,
                    subtitle: str = '', materia: str = '', integrantes: str = '', profesores: str = '',
                    show_logo: bool = False, logo_position: str = 'top-left',
                    cover_style: str = 'sidebar_logo',
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
        profs = profesores.strip()

        has_cover = bool(show_cover and doc_title)
        body_html = self._clean_redundant_pagebreaks(body_html, has_cover=has_cover)

        logo_html = ""
        if show_cover and show_logo:
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
                logo_html = f'<img src="{logo_uri}" class="cover-logo logo-{logo_position}" alt="Logo Facultad">'

        cover_html = ""
        if show_cover and doc_title:
            sub_str, subj_str, auth_str, prof_str = subtitle.strip(), subject.strip(), authors.strip(), profesores.strip()
            meta = ''.join(
                f'<div class="cover-meta-row"><span>{label}</span><b>{value}</b></div>'
                for label, value in [('Materia', subj_str), ('Integrantes', auth_str), ('Docentes', prof_str)] if value
            )
            subtitle_html = f'<p class="cover-subtitle">{sub_str}</p>' if sub_str else ''
            
            # --- NUEVA VALIDACIÓN DE ESTILOS ---
            style = cover_style if cover_style in {
                'sidebar_logo', 'academica_clasica', 'corporativa', 'bloque_color', 'marco_fino', 'folio'
            } else 'sidebar_logo'
            
            cover_html = f'''<div class="page cover-page cover-style-{style}">
              <div class="cover-header">{logo_html}</div>
              <div class="cover-content"><h1>{doc_title}</h1>{subtitle_html}</div>
              <div class="cover-meta">{meta}</div>
            </div>'''

        root_css = ThemeManager.generate_root_css(theme_key) if hasattr(ThemeManager, 'generate_root_css') else ""
        katex_head = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">'
        katex_footer = """<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
        <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
        onload='renderMathInElement(document.body, {delimiters: [{left: "$$", right: "$$", display: true}, {left: "$", right: "$", display: false}], ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"], throwOnError: false});'></script>"""
        katex_footer = katex_footer.replace("});", "}); window.katexRendered = true; if(window.runPagination) window.runPagination();")
        content_wrap = f'<div id="paginate-content">\n{body_html}\n</div>'
        core_css = self._get_core_css(is_preview)
        pygments_css = self.get_pygments_css(theme_key)
        
        fonts_head = """<link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;600&family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;0,7..72,700;1,7..72,400&family=Playfair+Display:wght@700;800&family=Poppins:wght@600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">"""

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
          </style>
        </head>
        <body class="theme-{theme_key}">
          {cover_html}
          {content_wrap}
          {katex_footer}
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
        .cover-style-academica_clasica .cover-content h1 { font-family: 'Literata', 'Times New Roman', serif; font-size: 36pt; border: none !important; font-weight: 700; color: #111827 !important;}
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

        h1, h2, h3, h4, h5, h6 { font-family: var(--font-family-headings, 'Inter', sans-serif); color: var(--heading-color, #111); margin-top: 0; }
        h1 { font-size: 20pt; font-weight: 700; margin-top: 10mm; margin-bottom: 4mm; border-bottom: 1px solid #ccc; padding-bottom: 2mm; }
        h2 { font-size: 14pt; font-weight: 600; margin-top: 7mm; margin-bottom: 3mm; }
        p { margin-bottom: 3mm; }
        
        .codehilite, .highlight { border-radius: 8px; padding: 10px 16px; margin: 12px 0; overflow: visible !important; border: 1px solid #e5e7eb; font-size: 9pt; background: #f9fafb; page-break-inside: avoid !important; break-inside: avoid !important; }
        pre, code { font-family: 'JetBrains Mono', monospace !important; }
        blockquote { border-left: 4px solid var(--accent-color, #ccc); padding: 8px 16px; margin: 12px 0; background: rgba(0,0,0,0.02); border-radius: 0 8px 8px 0; font-style: italic; }
        table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 10pt; }
        th, td { padding: 8px 12px; border: 1px solid #e5e7eb; text-align: left; }
        th { background-color: #f3f4f6 !important; font-weight: 600; }
        
        .page-break { page-break-after: always !important; break-after: page !important; }
        @media print { .page-break { page-break-after: always !important; break-after: page !important; } }
        @page { size: A4; margin: 0; }
        
        img { max-width: 100%; height: auto; display: block; margin: 6mm auto; page-break-inside: avoid !important; break-inside: avoid !important; }
        .math-display { text-align: center; margin: 4mm 0; overflow-x: auto; page-break-inside: avoid !important; break-inside: avoid !important; }
        """
        if is_preview:
            css += """
            body { background: #e5e5e5; padding: 40px 0; display: flex; flex-direction: column; align-items: center; overflow-x: hidden; overflow-y: auto; }
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
          window.paginationDone = false;
          function paginate() {
            if (window.paginationDone) return;
            window.paginationDone = true;
            var src = document.getElementById('paginate-content');
            if (!src || !src.children.length) return;
            var children = Array.from(src.children);
            src.remove();
            
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
            document.body.appendChild(currentPage);
            
            for (var i = 0; i < children.length; i++) {
              var el = children[i];
              var isManualBreak = (el.classList && el.classList.contains('page-break'));
              if (isManualBreak) {
                currentPage = document.createElement('div');
                currentPage.className = 'page';
                document.body.appendChild(currentPage);
                ruler.innerHTML = '';
                continue;
              }
              var clone = el.cloneNode(true);
              ruler.appendChild(clone);
              if (ruler.scrollHeight > maxPagePx && currentPage.children.length > 0) {
                ruler.innerHTML = '';
                currentPage = document.createElement('div');
                currentPage.className = 'page';
                document.body.appendChild(currentPage);
                ruler.appendChild(clone);
              }
              currentPage.appendChild(el);
            }
            document.body.removeChild(ruler);
          }
          window.runPagination = function() {
            if (window.paginationDone) return;
            setTimeout(paginate, 50);
          };
          window.addEventListener('load', window.runPagination);
          setTimeout(window.runPagination, 800);
        })();
        </script>"""