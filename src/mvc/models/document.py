import re
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
        """
        Limpia atributos extendidos de Pandoc/Google Docs del Markdown
        y reemplaza marcadores manuales de salto de página por <div class="page-break"></div>.
        
        Marcadores soportados:
          <!-- PAGEBREAK -->, <!-- PAGE-BREAK -->
          ---PAGEBREAK---, ---pagebreak---
          <div class="page-break"></div>
          \\newpage, \\pagebreak
        """
        # 0. Reemplazar marcadores manuales explícitos por el div de salto de página
        text = re.sub(
            r'^\s*(<!--\s*PAGE-?BREAK\s*-->|[-=]{3,}\s*PAGE-?BREAK\s*[-=]{3,})\s*$',
            r'<div class="page-break"></div>',
            text,
            flags=re.MULTILINE | re.IGNORECASE
        )

        # Soportar también \newpage y \pagebreak
        text = re.sub(
            r'\\{1,2}(newpage|pagebreak)',
            r'<div class="page-break"></div>',
            text
        )
        
        # Normalizar divs con estilo page-break inline
        text = re.sub(
            r'<div[^>]*style="[^"]*page-break-[^"]*"[^>]*>\s*</div>',
            r'<div class="page-break"></div>',
            text
        )

        # 1. Imágenes con atributos: ![alt](src){...} → ![alt](src)
        text = re.sub(r'(!\[[^\]]*\]\([^)]*\))\s*\{[^}]*\}', r'\1', text)

        # 2. Spans con clase (ej: [texto]{.underline}) → texto
        text = re.sub(r'\[([^\]]*)\]\{[^}]*\}', r'\1', text)

        # 3. Headers con atributos: # Título {#id .class} → # Título
        text = re.sub(r'^(#{1,6}\s+.*?)\s*\{[^}]*\}\s*$', r'\1', text, flags=re.MULTILINE)

        # 4. Atributos sueltos en su propia línea: {width="5in" height="3in"}
        text = re.sub(r'^\s*\{[^}]*\}\s*$', '', text, flags=re.MULTILINE)

        return text

    def _process_highlights(self, text: str) -> str:
        """
        Procesa la sintaxis de resaltado de texto (highlight):
          ==texto==(color)  →  <mark style="background-color: {color};">texto</mark>
          ==texto==         →  <mark style="background-color: #fff3b0;">texto</mark>
        """
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
        """
        Devuelve la configuración JSON de tema para mmdc/Mermaid según el tema del documento.
        """
        font_map = {
            'minimal': 'Space Grotesk, sans-serif',
            'classic': 'Literata, serif',
            'institutional': 'Inter, sans-serif',
            'editorial': 'Inter, sans-serif',
            'blueprint': 'IBM Plex Sans, sans-serif',
            'pastel': 'Poppins, sans-serif',
        }
        font_family = font_map.get(theme_key, 'Inter, sans-serif')
        
        theme_vars_map = {
            'minimal': {
                'fontFamily': font_family,
                'fontSize': '13px',
                'nodePadding': '20',
                'primaryColor': '#f4f4f5',
                'primaryTextColor': '#1a1a1a',
                'primaryBorderColor': '#d4d4d8',
                'lineColor': '#3a3a3a',
                'secondaryColor': '#e4e4e7',
                'tertiaryColor': '#ffffff'
            },
            'classic': {
                'fontFamily': font_family,
                'fontSize': '13px',
                'nodePadding': '20',
                'primaryColor': '#f5f0e1',
                'primaryTextColor': '#1a1410',
                'primaryBorderColor': '#d4c9b0',
                'lineColor': '#8b4513',
                'secondaryColor': '#f0ebe0',
                'tertiaryColor': '#FCFBF4'
            },
            'institutional': {
                'fontFamily': font_family,
                'fontSize': '13px',
                'nodePadding': '20',
                'primaryColor': '#f0f4f8',
                'primaryTextColor': '#1e3a5f',
                'primaryBorderColor': '#cbd5e1',
                'lineColor': '#1e3a5f',
                'secondaryColor': '#c9a84c',
                'tertiaryColor': '#ffffff'
            },
            'editorial': {
                'fontFamily': font_family,
                'fontSize': '13px',
                'nodePadding': '20',
                'primaryColor': '#f7f5f0',
                'primaryTextColor': '#7a2e3b',
                'primaryBorderColor': '#e2dfd7',
                'lineColor': '#7a2e3b',
                'secondaryColor': '#fdfdfb',
                'tertiaryColor': '#ffffff'
            },
            'blueprint': {
                'fontFamily': font_family,
                'fontSize': '13px',
                'nodePadding': '20',
                'primaryColor': '#eff6ff',
                'primaryTextColor': '#0f172a',
                'primaryBorderColor': '#bfdbfe',
                'lineColor': '#2563eb',
                'secondaryColor': '#dbe2ea',
                'tertiaryColor': '#f7f9fb'
            },
            'pastel': {
                'fontFamily': font_family,
                'fontSize': '13px',
                'nodePadding': '20',
                'primaryColor': '#f5f0fb',
                'primaryTextColor': '#332c27',
                'primaryBorderColor': '#ebd5d0',
                'lineColor': '#d96b52',
                'secondaryColor': '#8b78b5',
                'tertiaryColor': '#fffaf3'
            },
        }
        
        vars_dict = theme_vars_map.get(theme_key, theme_vars_map['minimal'])
        return {
            "theme": "base",
            "themeVariables": vars_dict,
            "flowchart": {
                "padding": 30,
                "nodeSpacing": 60,
                "rankSpacing": 60,
                "htmlLabels": False,
                "useMaxWidth": False
            },
            "sequence": {
                "boxPadding": 30,
                "useMaxWidth": False
            }
        }

    def _process_mermaid_diagrams(self, md_text: str, theme_key: str) -> str:
        """
        Intercepta bloques ```mermaid ... ``` antes del renderizado Markdown/Pygments
        y los reemplaza por SVGs pre-renderizados con tipografías embebidas localmente
        vía --cssFile + @font-face (con caché v4 por hash de contenido + tema).
        Fallback estilizado si mmdc no está disponible o falla.
        """
        import hashlib
        import os
        import tempfile
        import json
        import subprocess
        import html

        cache_dir = os.path.join(tempfile.gettempdir(), "pdf_converter_mermaid_cache")
        os.makedirs(cache_dir, exist_ok=True)

        # Ruta absoluta a la carpeta de fuentes embebidas
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        fonts_dir = os.path.join(project_root, "assets", "fonts")

        font_files_map = {
            'minimal': {'family': 'Space Grotesk', 'fallback': 'sans-serif', 'files': [('SpaceGrotesk-Regular.woff2', 400), ('SpaceGrotesk-SemiBold.woff2', 600)]},
            'classic': {'family': 'Literata', 'fallback': 'serif', 'files': [('Literata-Regular.woff2', 400), ('Literata-SemiBold.woff2', 600), ('Literata-Bold.woff2', 700)]},
            'institutional': {'family': 'Inter', 'fallback': 'sans-serif', 'files': [('Inter-Regular.woff2', 400), ('Inter-SemiBold.woff2', 600), ('Inter-Bold.woff2', 700)]},
            'editorial': {'family': 'Inter', 'fallback': 'sans-serif', 'files': [('Inter-Regular.woff2', 400), ('Inter-SemiBold.woff2', 600), ('Inter-Bold.woff2', 700)]},
            'blueprint': {'family': 'IBM Plex Sans', 'fallback': 'sans-serif', 'files': [('IBMPlexSans-Regular.woff2', 400), ('IBMPlexSans-SemiBold.woff2', 600), ('IBMPlexSans-Bold.woff2', 700)]},
            'pastel': {'family': 'Poppins', 'fallback': 'sans-serif', 'files': [('Poppins-Regular.woff2', 400), ('Poppins-SemiBold.woff2', 600), ('Poppins-Bold.woff2', 700)]},
        }

        def _build_css_for_theme(theme_key: str) -> str:
            """Genera CSS con @font-face embebidos como Data URIs base64 + reglas de color para inyectar en mmdc."""
            font_info = font_files_map.get(theme_key, font_files_map['institutional'])
            family = font_info['family']
            fallback = font_info['fallback']
            theme_vars = self._get_mermaid_theme_config(theme_key).get('themeVariables', {})

            # @font-face declarations embebidos como base64 data URIs
            import base64
            font_face_blocks = []
            for filename, weight in font_info['files']:
                font_path = os.path.join(fonts_dir, filename)
                if os.path.exists(font_path):
                    with open(font_path, 'rb') as ff:
                        b64_font = base64.b64encode(ff.read()).decode('utf-8')
                    data_url = f"data:font/woff2;base64,{b64_font}"
                    font_face_blocks.append(f"""@font-face {{
  font-family: '{family}';
  src: url('{data_url}') format('woff2');
  font-weight: {weight};
  font-style: normal;
}}""")

            font_faces_css = "\n".join(font_face_blocks)

            primary_color = theme_vars.get('primaryColor', '#f4f4f5')
            text_color = theme_vars.get('primaryTextColor', '#1a1a1a')
            border_color = theme_vars.get('primaryBorderColor', '#d4d4d8')
            line_color = theme_vars.get('lineColor', '#3a3a3a')

            return f"""{font_faces_css}

svg, svg * {{
  font-family: '{family}', {fallback} !important;
}}
svg .node rect, svg .node circle, svg .node ellipse, svg .node polygon, svg .node path {{
  fill: {primary_color} !important;
  stroke: {border_color} !important;
  stroke-width: 1.5px !important;
}}
svg .label, svg .nodeLabel, svg .edgeLabel, svg .node .label, svg text, svg tspan, text, tspan {{
  fill: {text_color} !important;
  font-family: '{family}', {fallback} !important;
  font-size: 14px !important;
  dominant-baseline: middle !important;
}}
svg .edgePath .path, svg .flowchart-link {{
  stroke: {line_color} !important;
  stroke-width: 2px !important;
}}
svg marker {{
  fill: {line_color} !important;
  stroke: {line_color} !important;
}}
svg .label-container {{
  fill: {primary_color} !important;
  stroke: {border_color} !important;
}}
foreignObject {{
  overflow: visible !important;
}}
foreignObject div, foreignObject span, foreignObject p {{
  overflow: visible !important;
  white-space: nowrap !important;
  text-align: center !important;
}}
"""

        def _replace_mermaid(match):
            mermaid_code = match.group(1).strip()
            if not mermaid_code:
                return ""

            hash_input = f"v9:{theme_key}:{mermaid_code}".encode('utf-8')
            cache_hash = hashlib.md5(hash_input).hexdigest()
            cache_file = os.path.join(cache_dir, f"{cache_hash}.svg")

            if os.path.exists(cache_file):
                try:
                    with open(cache_file, "r", encoding="utf-8") as f:
                        svg_content = f.read()
                    return f'<div class="mermaid-diagram">{svg_content}</div>'
                except Exception:
                    pass

            config_dict = self._get_mermaid_theme_config(theme_key)
            mermaid_css = _build_css_for_theme(theme_key)

            with tempfile.TemporaryDirectory() as tmp_dir:
                mmd_file = os.path.join(tmp_dir, "input.mmd")
                svg_tmp = os.path.join(tmp_dir, "output.svg")
                cfg_file = os.path.join(tmp_dir, "config.json")
                css_file = os.path.join(tmp_dir, "theme.css")

                with open(mmd_file, "w", encoding="utf-8") as f:
                    f.write(mermaid_code)
                with open(cfg_file, "w", encoding="utf-8") as f:
                    json.dump(config_dict, f)
                with open(css_file, "w", encoding="utf-8") as f:
                    f.write(mermaid_css)

                cmd_options = [
                    ["mmdc", "-i", mmd_file, "-o", svg_tmp, "-c", cfg_file, "-C", css_file, "-b", "transparent"],
                    ["npx", "-y", "@mermaid-js/mermaid-cli", "-i", mmd_file, "-o", svg_tmp, "-c", cfg_file, "-C", css_file, "-b", "transparent"]
                ]

                rendered_svg = None
                for cmd in cmd_options:
                    try:
                        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                        if res.returncode == 0 and os.path.exists(svg_tmp):
                            with open(svg_tmp, "r", encoding="utf-8") as f:
                                rendered_svg = f.read()
                            break
                    except Exception:
                        pass

                if rendered_svg:
                    # Post-procesar SVG: expandir foreignObject y translate de forma simétrica (factor 1.6x) para dar espacio al texto real
                    def _expand_fo(m):
                        h_val = m.group(1)
                        w_val = float(m.group(2))
                        new_w = w_val * 1.6
                        new_x = -new_w / 2.0
                        return f'transform="translate({new_x:.2f}, {h_val})"><rect/><foreignObject width="{new_w:.2f}"'

                    rendered_svg = re.sub(
                        r'transform="translate\(-[\d\.]+\s*,\s*(-?[\d\.]+)\)"\s*><rect/>\s*<foreignObject\s+width="([\d\.]+)"',
                        _expand_fo,
                        rendered_svg
                    )
                    rendered_svg = re.sub(r'max-width:\s*200px', 'max-width:none', rendered_svg)
                    # Convertir display: table-cell a Flexbox perfectamente centrado (horizontal y vertical)
                    rendered_svg = re.sub(
                        r'display:\s*table-cell;',
                        'display: flex !important; align-items: center !important; justify-content: center !important; width: 100% !important; text-align: center !important;',
                        rendered_svg
                    )
                    try:
                        with open(cache_file, "w", encoding="utf-8") as f:
                            f.write(rendered_svg)
                    except Exception:
                        pass
                    return f'<div class="mermaid-diagram">{rendered_svg}</div>'

            return f'''<div class="mermaid-fallback-box">
              <div class="mermaid-fallback-header">📊 Diagrama Mermaid (Código Fuente)</div>
              <pre class="mermaid-fallback-code"><code>{html.escape(mermaid_code)}</code></pre>
            </div>'''

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

        extensions = [
            ExtraExtension(),
            'pymdownx.tilde',
            'pymdownx.caret',
            'pymdownx.tasklist',
            'fenced_code',
            'codehilite',
        ]
        extension_configs = {
            'codehilite': {
                'css_class': 'codehilite',
                'use_pygments': True,
                'linenums': False,
            },
        }

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
        from urllib.request import pathname2url
        base_dir = os.getcwd()
        
        def make_absolute_uri(match):
            src = match.group(1)
            if src.startswith(('http://', 'https://', 'data:', 'file://')) or os.path.isabs(src):
                return match.group(0)
            abs_path = os.path.normpath(os.path.join(base_dir, src))
            file_uri = 'file://' + pathname2url(abs_path)
            return f'src="{file_uri}"'
            
        html = re.sub(r'src="([^"]+)"', make_absolute_uri, html)

        return html, server_katex

    def get_pygments_css(self, theme_key: str) -> str:
        """
        Genera dinámicamente el CSS de resaltado de sintaxis Pygments según el estilo asignado al tema.
        """
        try:
            from pygments.formatters import HtmlFormatter
            from pygments.styles import get_all_styles
            
            theme = ThemeManager.get_theme(theme_key)
            style_name = theme.get('pygments_style', 'monokai')
            
            available = list(get_all_styles())
            if style_name not in available:
                style_name = 'default'
                
            formatter = HtmlFormatter(style=style_name)
            return formatter.get_style_defs('.codehilite')
        except Exception as e:
            print(f"[Pygments Error] {e}")
            return ""

    def _clean_redundant_pagebreaks(self, html: str, has_cover: bool = True) -> str:
        if not html:
            return html
        pb_pattern = r'<div[^>]*class="[^"]*page-break[^"]*"[^>]*>\s*</div>'
        if has_cover:
            html = re.sub(r'^\s*(?:' + pb_pattern + r'|<p>\s*</p>|\s+)+', '', html, flags=re.IGNORECASE)
        html = re.sub(r'(?:' + pb_pattern + r'\s*(?:<p>\s*</p>\s*)*){2,}', r'<div class="page-break" style="page-break-after: always; break-after: page;"></div>', html, flags=re.IGNORECASE)
        html = re.sub(r'(?:' + pb_pattern + r'|<p>\s*</p>|\s+)+$', '', html, flags=re.IGNORECASE)
        return html

    def _inject_toc(self, md_text: str) -> str:
        """Replace the explicit TOC marker with link targets before Markdown parsing.

        Page labels are populated after the existing browser pagination pass, so
        they reflect the final PDF layout rather than an estimate.
        """
        if not re.search(r'<!--\s*TOC\s*-->', md_text, re.IGNORECASE):
            return md_text
        headings = []
        for line in md_text.splitlines():
            match = re.match(r'^(#{1,3})\s+(.+?)\s*#*\s*$', line)
            if match:
                headings.append((len(match.group(1)), self._strip_markdown(match.group(2))))
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
                    cover_style: str = 'folio',
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
            from urllib.request import pathname2url
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
                logo_uri = "file://" + pathname2url(logo_path)
                logo_html = f'<img src="{logo_uri}" class="cover-logo logo-{logo_position}" alt="Logo Facultad">'

        cover_html = ""
        if show_cover and doc_title:
            sub_str, subj_str, auth_str, prof_str = subtitle.strip(), subject.strip(), authors.strip(), profesores.strip()
            meta = ''.join(
                f'<div class="cover-meta-row"><span>{label}</span><b>{value}</b></div>'
                for label, value in [('Materia', subj_str), ('Integrantes', auth_str), ('Docentes', prof_str)] if value
            )
            subtitle_html = f'<p class="cover-subtitle">{sub_str}</p>' if sub_str else ''
            style = cover_style if cover_style in {'folio', 'centered', 'rule', 'margin', 'panel', 'notebook'} else 'folio'
            cover_html = f'''<div class="page cover-page cover-style-{style}">
              <div class="cover-header">{logo_html}<div class="cover-kicker">DOCUMENTO ACADÉMICO</div></div>
              <div class="cover-content"><h1>{doc_title}</h1>{subtitle_html}</div>
              <div class="cover-meta">{meta}</div>
            </div>'''

        root_css = ThemeManager.generate_root_css(theme_key)
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
        <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;600&family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;0,7..72,700;1,7..72,400&family=Outfit:wght@400;600;700;800&family=Playfair+Display:wght@700;800&family=Poppins:wght@600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">"""

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
        html, body {
          width: 100%;
          font-family: var(--font-family-content);
          color: var(--text-color);
          font-size: 11pt;
          line-height: 1.6;
        }
        
        /* Portada y Logo */
        .cover-page {
          position: relative !important;
          overflow: hidden !important;
        }
        .toc { margin: 0 0 10mm; padding: 7mm 9mm; border: 1px solid var(--accent-color); border-radius: 5px; }
        .toc h2 { border: 0; margin: 0 0 4mm; }
        .toc ol { list-style: none; padding: 0; }
        .toc li { display: flex; gap: 8px; border-bottom: 1px dotted var(--muted-color); padding: 2px 0; }
        .toc a { color: inherit; text-decoration: none; flex: 1; }
        .toc-level-2 { padding-left: 5mm !important; }.toc-level-3 { padding-left: 10mm !important; }
        .toc-page { min-width: 1.5em; text-align: right; }
        .cover-logo {
          position: absolute !important;
          max-width: 120px !important;
          max-height: 80px !important;
          width: auto;
          height: auto;
          object-fit: contain;
          z-index: 10;
        }
        .logo-top-left { top: 20mm; left: 20mm; }
        .logo-top-right { top: 20mm; right: 20mm; }
        .logo-bottom-left { bottom: 20mm; left: 20mm; }
        .logo-bottom-right { bottom: 20mm; right: 20mm; }

        /* 1. Clásica Centrada */
        .cover-style-classic {
          display: flex !important;
          flex-direction: column !important;
          justify-content: center !important;
          align-items: center !important;
          text-align: center !important;
          min-height: 297mm !important;
          height: 100% !important;
        }
        .cover-style-classic .cover-content {
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          width: 100%;
          height: 100%;
        }
        .cover-style-classic h1 {
          font-family: var(--font-family-headings);
          font-size: 32pt;
          font-weight: 700;
          margin-bottom: 8mm;
          color: var(--heading-color);
          border: none;
          padding: 0;
          line-height: 1.2;
        }
        .cover-style-classic .subtitle {
          font-family: var(--font-family-content);
          font-size: 16pt;
          font-weight: 300;
          font-style: italic;
          margin-bottom: 20mm;
          color: var(--muted-color);
        }
        .cover-style-classic .meta {
          font-family: var(--font-family-headings);
          font-size: 11pt;
          color: var(--muted-color);
          line-height: 2.2;
        }
        .cover-style-classic .meta strong { color: var(--text-color); }

        /* 2. Editorial con Franja Lateral */
        .cover-style-sidebar {
          display: flex !important;
          flex-direction: row !important;
          padding: 0 !important;
          margin: 0 !important;
          position: relative !important;
          min-height: 297mm !important;
          height: 100% !important;
          box-sizing: border-box !important;
        }
        .sidebar-stripe {
          width: 28%;
          background: var(--accent-color) !important;
          height: 100% !important;
          min-height: 297mm !important;
          position: absolute;
          top: 0;
          bottom: 0;
          left: 0;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          padding: 20mm 10mm;
          box-sizing: border-box;
          z-index: 2;
        }
        .logo-sidebar {
          position: relative !important;
          top: auto !important;
          left: auto !important;
          right: auto !important;
          bottom: auto !important;
          max-width: 110px !important;
          max-height: 100px !important;
          filter: brightness(0) invert(1);
          margin: 0 auto;
        }
        .sidebar-content {
          margin-left: 28%;
          width: 72%;
          height: 100%;
          min-height: 297mm;
          padding: 30mm 25mm 30mm 25mm;
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: flex-start;
          text-align: left;
          box-sizing: border-box;
        }
        .sidebar-main-block {
          width: 100%;
        }
        .sidebar-title {
          font-family: var(--font-family-headings);
          font-size: 34pt;
          font-weight: 800;
          line-height: 1.15;
          color: var(--heading-color);
          margin-bottom: 6mm;
          border: none !important;
          letter-spacing: -0.5px;
        }
        .sidebar-subtitle {
          font-family: var(--font-family-content);
          font-size: 15pt;
          font-weight: 400;
          color: var(--muted-color);
          margin-bottom: 10mm;
          font-style: italic;
        }
        .sidebar-accent-line {
          width: 80px;
          height: 5px;
          background: var(--accent-color);
          margin-bottom: 12mm;
          border-radius: 3px;
        }
        .sidebar-meta .meta-item {
          margin-bottom: 4.5mm;
          font-family: var(--font-family-content);
          font-size: 11pt;
          line-height: 1.5;
        }
        .sidebar-meta .meta-label {
          font-weight: 700;
          color: var(--heading-color);
          display: inline-block;
          min-width: 110px;
        }
        .sidebar-meta .meta-val {
          color: var(--text-color);
        }

        /* 3. Portada Asimétrica Tipográfica (Minimalista Rediseñada) */
        .cover-style-minimal {
          display: flex !important;
          flex-direction: column !important;
          justify-content: center !important;
          align-items: center !important;
          position: relative !important;
          padding: 30mm 25mm !important;
          min-height: 297mm !important;
          box-sizing: border-box !important;
          overflow: hidden !important;
        }
        .logo-minimal {
          z-index: 10;
        }
        .minimal-bg-shape {
          position: absolute;
          top: 15%;
          right: -10%;
          width: 320px;
          height: 320px;
          border-radius: 50%;
          background: var(--accent-color);
          opacity: 0.14;
          z-index: 1;
          pointer-events: none;
        }
        .minimal-wrapper {
          position: relative;
          z-index: 2;
          width: 100%;
          height: 100%;
          display: flex;
          flex-direction: column;
          justify-content: space-between;
          padding: 10mm 0;
        }
        .minimal-title-block {
          text-align: left;
          margin-top: 15mm;
          margin-bottom: 25mm;
          max-width: 90%;
        }
        .minimal-title {
          font-family: var(--font-family-headings);
          font-size: 38pt;
          font-weight: 800;
          color: var(--heading-color);
          line-height: 1.1;
          margin-bottom: 8mm;
          border: none !important;
          letter-spacing: -1px;
        }
        .minimal-subtitle {
          font-family: var(--font-family-content);
          font-size: 16pt;
          font-weight: 400;
          color: var(--muted-color);
          line-height: 1.4;
        }
        .minimal-meta-block {
          display: flex;
          align-items: flex-start;
          gap: 16px;
          border-top: 2px solid var(--accent-color);
          padding-top: 10mm;
        }
        .minimal-accent-pill {
          width: 8px;
          height: 44px;
          background: var(--accent-color);
          border-radius: 4px;
          flex-shrink: 0;
          margin-top: 2px;
        }
        .minimal-meta-grid {
          display: flex;
          flex-direction: column;
          gap: 4mm;
          font-family: var(--font-family-content);
          font-size: 11pt;
          color: var(--text-color);
        }
        .minimal-meta-row strong {
          color: var(--heading-color);
          font-family: var(--font-family-headings);
        }

        /* 4. Ficha Técnica */
        .cover-style-technical {
          display: flex !important;
          flex-direction: column !important;
          justify-content: center !important;
          align-items: center !important;
          padding: 20mm !important;
          min-height: 297mm !important;
          box-sizing: border-box !important;
        }
        .tech-box {
          width: 100%;
          border: 3px solid var(--accent-color);
          border-radius: 12px;
          overflow: hidden;
          background: var(--page-bg);
          box-shadow: 0 4px 16px rgba(0,0,0,0.06);
          display: flex;
          flex-direction: column;
          box-sizing: border-box;
        }
        .tech-header-banner {
          background: var(--accent-color);
          padding: 8mm 12mm;
          display: flex;
          align-items: center;
          justify-content: flex-end;
          min-height: 22mm;
          box-sizing: border-box;
        }
        .logo-tech {
          position: relative !important;
          top: auto !important;
          left: auto !important;
          right: auto !important;
          bottom: auto !important;
          max-width: 110px !important;
          max-height: 60px !important;
          filter: brightness(0) invert(1);
        }
        .tech-main-content {
          padding: 14mm 14mm 10mm 14mm;
          text-align: left;
        }
        .tech-title {
          font-family: var(--font-family-headings);
          font-size: 28pt;
          font-weight: 800;
          color: var(--heading-color);
          margin-bottom: 4mm;
          border: none !important;
          line-height: 1.2;
        }
        .tech-subtitle {
          font-family: var(--font-family-content);
          font-size: 14pt;
          color: var(--muted-color);
          font-style: italic;
        }
        .tech-grid {
          border-top: 2px solid var(--accent-color);
          background: var(--page-bg);
        }
        .tech-row {
          display: flex;
          border-bottom: 1px solid var(--table-border);
          font-size: 10.5pt;
        }
        .tech-row:last-child {
          border-bottom: none;
        }
        .tech-label {
          width: 28%;
          background: var(--table-header-bg);
          color: var(--table-header-fg);
          font-family: var(--font-family-headings);
          font-weight: 700;
          padding: 10px 14px;
          font-size: 9.5pt;
          display: flex;
          align-items: center;
          border-left: 5px solid var(--accent-color);
          letter-spacing: 0.5px;
        }
        .tech-value {
          width: 72%;
          padding: 10px 14px;
          color: var(--text-color);
          background: var(--page-bg);
          display: flex;
          align-items: center;
          font-family: var(--font-family-content);
        }

        /* Cuatro portadas multicolor de alta legibilidad. */
        .cover-page[class*="cover-style-"] { min-height: 297mm !important; padding: 22mm !important; isolation: isolate; }
        .cover-page[class*="cover-style-"] .cover-logo { background: rgba(255,255,255,.94); padding: 3mm; border-radius: 4mm; box-shadow: 0 3px 12px rgba(0,0,0,.14); }
        .cover-page[class*="cover-style-"] .cover-art { position: absolute; z-index: -1; pointer-events: none; }
        .cover-page[class*="cover-style-"] .cover-content h1 { border: 0 !important; margin: 0; font-family: var(--font-family-headings); }
        .cover-kicker { font: 700 8.5pt var(--font-family-headings); letter-spacing: 2px; }
        .cover-subtitle { font-size: 15pt; margin-top: 7mm; max-width: 110mm; }.cover-meta { font-family: var(--font-family-content); }
        .cover-meta-row { display: flex; gap: 8mm; padding: 3mm 0; border-bottom: 1px solid currentColor; }.cover-meta-row span { min-width: 30mm; font-weight: 700; opacity: .75; text-transform: uppercase; font-size: 8pt; letter-spacing: .8px; }
        /* Minimalista: salvia, beige y rubor con márgenes generosos. */
        .cover-style-minimalist { background:#f5f0e6 !important; color:#405545 !important; }.cover-style-minimalist .cover-kicker{color:#b66d78;margin-top:10mm}.cover-style-minimalist .cover-content{margin-top:58mm;max-width:120mm}.cover-style-minimalist .cover-content h1{color:#405545 !important;font-size:38pt;line-height:1.12}.cover-style-minimalist .cover-subtitle{color:#857365}.cover-style-minimalist .cover-meta{position:absolute;bottom:22mm;left:22mm;width:105mm}.cover-style-minimalist .art-one{width:78mm;height:297mm;right:0;top:0;background:#b5c7ad}.cover-style-minimalist .art-two{width:35mm;height:35mm;border-radius:50%;background:#e8abb0;right:21mm;top:52mm}.cover-style-minimalist .art-three{width:58mm;height:7mm;background:#d4a859;right:0;bottom:34mm}
        /* Académica: centrada, solemne, azul marino/borgoña/dorado. */
        .cover-style-academic { background:#102746 !important;color:#fbf5e9 !important;text-align:center;border:7mm solid #7a2537}.cover-style-academic .cover-kicker{color:#d9b765;margin-top:24mm}.cover-style-academic .cover-content{margin:44mm auto 0;max-width:145mm}.cover-style-academic .cover-content h1{color:#fff8e8 !important;font-family:'Literata',serif;font-size:39pt;line-height:1.12}.cover-style-academic .cover-subtitle{color:#d9c9af;margin-left:auto;margin-right:auto}.cover-style-academic .cover-meta{position:absolute;bottom:25mm;left:42mm;right:42mm;text-align:left}.cover-style-academic .art-one{width:128mm;height:170mm;border:1.5mm solid #d9b765;left:41mm;top:55mm}.cover-style-academic .art-two{width:52mm;height:5mm;background:#7a2537;left:79mm;top:148mm}.cover-style-academic .art-three{width:16mm;height:16mm;border-radius:50%;background:#d9b765;right:28mm;bottom:28mm}
        /* Tipográfica: contraste de escala, naranja, teal y mostaza. */
        .cover-style-typographic{background:#f26b38 !important;color:#fff9e9 !important}.cover-style-typographic .cover-kicker{color:#f3cf58;margin-top:12mm}.cover-style-typographic .cover-content{margin-top:18mm;max-width:150mm}.cover-style-typographic .cover-content h1{color:#fff9e9 !important;font-size:57pt;line-height:.93;letter-spacing:-2px}.cover-style-typographic .cover-subtitle{color:#fff0c8;font-size:18pt}.cover-style-typographic .cover-meta{position:absolute;bottom:19mm;left:22mm;width:118mm}.cover-style-typographic .art-one{width:72mm;height:297mm;right:0;top:0;background:#075d63}.cover-style-typographic .art-two{width:100%;height:12mm;background:#e9b949;left:0;top:121mm}.cover-style-typographic .art-three{width:37mm;height:37mm;border-radius:50%;background:#e9b949;right:17mm;bottom:25mm}
        /* Orgánica: interpretación libre con manchas fluidas multicolor. */
        .cover-style-organic{background:#fbf4ec !important;color:#263c55 !important}.cover-style-organic .cover-kicker{color:#d85d72;margin-top:14mm}.cover-style-organic .cover-content{margin-top:64mm;max-width:124mm}.cover-style-organic .cover-content h1{color:#263c55 !important;font-size:41pt;line-height:1.06}.cover-style-organic .cover-subtitle{color:#58707d}.cover-style-organic .cover-meta{position:absolute;bottom:21mm;left:22mm;width:112mm}.cover-style-organic .art-one{width:140mm;height:125mm;border-radius:55% 45% 48% 52%;background:#e87980;right:-55mm;top:-36mm;transform:rotate(18deg)}.cover-style-organic .art-two{width:110mm;height:92mm;border-radius:45% 55% 60% 40%;background:#4fa79f;right:-32mm;bottom:-25mm;transform:rotate(-20deg)}.cover-style-organic .art-three{width:46mm;height:46mm;border-radius:50% 38% 60% 42%;background:#e6ba52;left:36mm;top:93mm;transform:rotate(30deg)}

        /* Seis portadas editoriales sobrias: sin formas decorativas; su color,
           fuentes y contraste derivan exclusivamente del tema seleccionado. */
        .cover-page[class*="cover-style-"] { background: var(--page-bg) !important; color: var(--text-color) !important; padding: 22mm !important; }
        .cover-page[class*="cover-style-"] .cover-header { display:flex; align-items:center; gap:6mm; color:var(--accent-color); }
        .cover-page[class*="cover-style-"] .cover-header .cover-logo { position:static !important; display:block; max-width:32mm !important; max-height:22mm !important; padding:0; border-radius:0; background:transparent; box-shadow:none; }
        .cover-page[class*="cover-style-"] .cover-kicker { color:var(--accent-color); font-size:8pt; letter-spacing:1.7px; }
        .cover-page[class*="cover-style-"] .cover-content h1 { color:var(--heading-color) !important; font-size:38pt; line-height:1.1; }
        .cover-page[class*="cover-style-"] .cover-subtitle { color:var(--muted-color); font-size:15pt; }
        .cover-page[class*="cover-style-"] .cover-meta { color:var(--text-color); }
        .cover-page[class*="cover-style-"] .cover-meta-row { border-color: var(--accent-color); }
        /* Folio: composición izquierda con aire y una línea editorial. */
        .cover-style-folio .cover-content { margin-top:70mm; max-width:135mm; border-left:3mm solid var(--accent-color); padding-left:8mm; }
        .cover-style-folio .cover-meta { position:absolute; bottom:24mm; left:22mm; width:120mm; }
        /* Centrada: presentación tradicional con jerarquía serena. */
        .cover-style-centered { text-align:center; }.cover-style-centered .cover-header { justify-content:center; }.cover-style-centered .cover-content { margin:62mm auto 0; max-width:145mm; }.cover-style-centered .cover-content h1 { font-family:var(--font-family-headings); }.cover-style-centered .cover-subtitle { margin-left:auto; margin-right:auto; }.cover-style-centered .cover-meta { position:absolute; bottom:25mm; left:45mm; right:45mm; text-align:left; }.cover-style-centered .cover-meta-row:first-child { border-top:1px solid var(--accent-color); }
        /* Regla: encabezado superior y título alineado a una retícula limpia. */
        .cover-style-rule { border-top:7mm solid var(--heading-color); }.cover-style-rule .cover-header { padding-bottom:7mm; border-bottom:1px solid var(--accent-color); }.cover-style-rule .cover-content { margin-top:48mm; max-width:150mm; }.cover-style-rule .cover-content h1 { font-size:43pt; }.cover-style-rule .cover-meta { position:absolute; bottom:23mm; left:22mm; right:22mm; display:grid; grid-template-columns:1fr 1fr; column-gap:10mm; }.cover-style-rule .cover-meta-row { display:block; }.cover-style-rule .cover-meta-row span { display:block; margin-bottom:1mm; }
        /* Margen: banda lateral mínima, sin elementos ilustrativos. */
        .cover-style-margin { border-left:15mm solid var(--accent-color); padding-left:28mm !important; }.cover-style-margin .cover-content { margin-top:63mm; max-width:128mm; }.cover-style-margin .cover-meta { position:absolute; bottom:22mm; left:28mm; width:110mm; }.cover-style-margin .cover-header { margin-left:-6mm; }
        /* Panel: información organizada dentro de un marco ligero. */
        .cover-style-panel .cover-header { padding-bottom:8mm; }.cover-style-panel .cover-content { margin-top:35mm; padding:13mm; border:1px solid var(--accent-color); border-left:5mm solid var(--heading-color); max-width:150mm; }.cover-style-panel .cover-content h1 { font-size:36pt; }.cover-style-panel .cover-meta { position:absolute; bottom:24mm; left:35mm; width:140mm; display:flex; gap:7mm; }.cover-style-panel .cover-meta-row { flex:1; display:block; }.cover-style-panel .cover-meta-row span { display:block; margin-bottom:1mm; }
        /* Cuaderno: doble regla discreta para un uso cotidiano y personal. */
        .cover-style-notebook { padding-top:28mm !important; border-bottom:5mm solid var(--accent-color); }.cover-style-notebook .cover-header { border-top:1px solid var(--accent-color); padding-top:6mm; }.cover-style-notebook .cover-content { margin-top:66mm; max-width:132mm; }.cover-style-notebook .cover-content h1 { font-size:40pt; }.cover-style-notebook .cover-meta { position:absolute; bottom:25mm; left:22mm; width:118mm; }
        
        /* Contenido General */
        h1, h2, h3, h4, h5, h6 { 
            font-family: var(--font-family-headings); 
            color: var(--heading-color); 
            margin-top: 0; 
        }
        h1:first-child, h2:first-child { margin-top: 0; }
        h1 { font-size: 20pt; font-weight: 700; margin-top: 10mm; margin-bottom: 4mm; border-bottom: var(--h1-border-width) solid var(--h1-border-color); padding-bottom: 2mm; }
        h2 { font-size: 14pt; font-weight: 600; margin-top: 7mm; margin-bottom: 3mm; }
        h3 { font-size: 12pt; font-weight: 600; margin-top: 5mm; margin-bottom: 2mm; font-style: italic; }
        p { margin-bottom: 3mm; }
        
        /* Code y Blockquotes */
        .codehilite, .highlight {
          border-radius: 8px;
          padding: 10px 16px;
          margin: 12px 0;
          overflow: visible !important;
          border: 1px solid var(--code-border);
          font-size: 9pt;
          background: var(--code-bg);
          page-break-inside: avoid !important;
          break-inside: avoid !important;
        }
        .codehilite pre, .codehilite code, .highlight pre, .highlight code, pre, pre code {
          background: transparent !important;
          border: none !important;
          padding: 0 !important;
          font-family: 'JetBrains Mono', Consolas, 'Courier New', monospace !important;
          font-size: inherit;
        }
        :not(pre) > code {
          background: var(--inline-code-bg);
          color: var(--inline-code-color);
          padding: 0.2em 0.4em;
          border-radius: 6px;
          font-family: 'JetBrains Mono', Consolas, 'Courier New', monospace !important;
          font-size: 8.5pt;
          border: 1px solid var(--inline-code-border);
        }
        
        /* KaTeX Formulas */
        .katex, .katex * {
          font-family: KaTeX_Main, 'Times New Roman', serif !important;
        }
        
        blockquote {
          border-left: 4px solid var(--accent-color);
          padding: 8px 16px;
          margin: 12px 0;
          background: rgba(0, 0, 0, 0.02);
          border-radius: 0 8px 8px 0;
          font-style: italic;
          color: var(--muted-color);
        }
        
        table {
          width: 100%;
          border-collapse: collapse;
          margin: 16px 0;
          font-size: 10pt;
        }
        th, td {
          padding: 8px 12px;
          border: 1px solid var(--table-border);
          text-align: left;
        }
        th {
          background-color: var(--table-header-bg) !important;
          color: var(--table-header-fg) !important;
          font-family: var(--font-family-headings);
          font-weight: 600;
        }
        tr:nth-child(even) {
          background-color: var(--table-row-even-bg);
        }
        tr {
            page-break-inside: avoid !important;
            break-inside: avoid !important;
        }
        
        ul, ol {
          padding-left: 24px;
          margin-bottom: 12px;
        }
        li { margin-bottom: 4px; }

        body.theme-institutional h1 { font-weight: 800; letter-spacing: -0.3px; }
        body.theme-institutional h2 { font-weight: 700; border-bottom: 1px solid rgba(30, 58, 95, 0.15); padding-bottom: 2mm; }
        body.theme-institutional h3 { font-weight: 700; font-style: normal; }
        body.theme-institutional h1::after { content: ''; display: block; width: 50px; height: 2px; background: var(--accent-color); margin-top: 3mm; }
        body.theme-institutional .cover-page { border-top: 5px solid var(--heading-color); }
        body.theme-institutional .cover-page h1 { font-size: 34pt; font-weight: 800; border-bottom: none !important; }
        body.theme-institutional .cover-page h1::after { width: 80px; height: 3px; background: var(--accent-color); margin: 6mm auto 0; }
        body.theme-classic blockquote { font-family: 'Literata', serif; }
        
        .page-break, .pagebreak {
            page-break-after: always !important;
            break-after: page !important;
            page-break-before: avoid !important;
            break-before: avoid !important;
            display: block !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            border: none !important;
            clear: both !important;
        }

        @media print {
            .page-break, .pagebreak {
                page-break-after: always !important;
                break-after: page !important;
                page-break-before: avoid !important;
                break-before: avoid !important;
            }
        }

        @page { size: A4; margin: 0; }
        
        img { 
            max-width: 100%; 
            height: auto; 
            display: block; 
            margin: 6mm auto;
            image-rendering: auto;
            page-break-inside: avoid !important;
            break-inside: avoid !important;
        }
        
        hr { border: none; border-top: 1px solid var(--accent-color); opacity: 0.3; margin: 6mm 0; }

        .math-display, .katex-display { 
            text-align: center; 
            margin: 4mm 0; 
            overflow-x: auto; 
            page-break-inside: avoid !important;
            break-inside: avoid !important;
        }
        .math-inline { white-space: nowrap; }
        strong { color: var(--heading-color); }
        del { text-decoration: line-through; color: var(--muted-color); }

        .mermaid-diagram {
            max-width: 100%;
            display: block;
            margin: 6mm auto;
            text-align: center;
            page-break-inside: avoid !important;
            break-inside: avoid !important;
            overflow-x: auto;
        }
        .mermaid-diagram svg {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
        }
        .mermaid-fallback-box {
            border: 1px solid var(--code-border);
            background: var(--code-bg);
            border-radius: 8px;
            padding: 12px 16px;
            margin: 6mm 0;
            page-break-inside: avoid !important;
            break-inside: avoid !important;
        }
        .mermaid-fallback-header {
            font-family: var(--font-family-headings);
            font-size: 9.5pt;
            font-weight: 600;
            color: var(--accent-color);
            margin-bottom: 8px;
        }
        .mermaid-fallback-code {
            font-family: 'JetBrains Mono', monospace;
            font-size: 8.5pt;
            color: var(--text-color);
            margin: 0;
            white-space: pre-wrap;
        }
        """
        
        if is_preview:
            css += """
            body { background: var(--preview-body-bg); padding: 40px 0; display: flex; flex-direction: column; align-items: center; overflow-x: hidden; overflow-y: auto; }
            .page { width: 210mm; min-height: 297mm; box-sizing: border-box; background: var(--page-bg); padding: 20mm; margin-bottom: 40px; box-shadow: 0 8px 32px rgba(0,0,0,0.35); font-family: var(--font-family-content); font-size: 11pt; line-height: 1.6; color: var(--text-color); text-align: justify; flex-shrink: 0; break-inside: avoid; }
            .cover-page { padding: 40mm 20mm !important; }
            """
        else:
            css += """
            html, body {
                width: 210mm;
                margin: 0;
                padding: 0;
                background-color: var(--page-bg) !important;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }
            .page {
                width: 210mm;
                min-height: 297mm;
                height: 297mm;
                box-sizing: border-box;
                background-color: var(--page-bg) !important;
                padding: 20mm;
                margin: 0;
                text-align: justify;
                page-break-after: always !important;
                break-after: page !important;
                page-break-inside: avoid !important;
                break-inside: avoid !important;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }
            .cover-page {
                padding: 40mm 20mm !important;
            }
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
            
            // Medir altura imprimible exacta (257mm = 297mm - 40mm margen) en píxeles
            var calcEl = document.createElement('div');
            calcEl.style.cssText = 'position:fixed;left:-9999px;top:0;height:257mm;width:210mm;padding:0 20mm;box-sizing:border-box;visibility:hidden;';
            document.body.appendChild(calcEl);
            var maxPagePx = calcEl.clientHeight || 971;
            document.body.removeChild(calcEl);

            // Medidor oculto para medir desborde
            var ruler = document.createElement('div');
            ruler.style.cssText = 'position:fixed;left:-9999px;top:0;width:210mm;padding:0 20mm;box-sizing:border-box;overflow:hidden;font-family:inherit;font-size:inherit;line-height:inherit;';
            document.body.appendChild(ruler);
            
            var currentPage = document.createElement('div');
            currentPage.className = 'page';
            document.body.appendChild(currentPage);
            
            for (var i = 0; i < children.length; i++) {
              var el = children[i];
              var isManualBreak = (el.classList && (el.classList.contains('page-break') || el.classList.contains('pagebreak'))) || 
                                  (el.getAttribute && el.getAttribute('style') && el.getAttribute('style').indexOf('break') !== -1);
              
              if (isManualBreak) {
                // Salto de página manual (<!-- PAGEBREAK -->)
                currentPage = document.createElement('div');
                currentPage.className = 'page';
                document.body.appendChild(currentPage);
                ruler.innerHTML = '';
                continue;
              }
              
              var clone = el.cloneNode(true);
              ruler.appendChild(clone);
              
              // Si el elemento desborda la capacidad de la hoja A4
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
            // The index is resolved only after final page cards exist.  This
            // keeps its numbers aligned with Puppeteer's exported pages.
            Array.from(document.querySelectorAll('.toc-page')).forEach(function(label) {
              var heading = document.getElementById(label.dataset.target);
              var page = heading && heading.closest('.page');
              if (page) label.textContent = Array.from(document.querySelectorAll('.page')).indexOf(page) + 1;
            });
          }
        
          window.runPagination = function() {
            if (window.paginationDone) return;
            if (document.fonts && document.fonts.ready) {
              document.fonts.ready.then(function() {
                setTimeout(paginate, 50);
              });
            } else {
              setTimeout(paginate, 100);
            }
          };

          window.addEventListener('load', window.runPagination);
          if (document.readyState === 'complete') { window.runPagination(); }
          setTimeout(window.runPagination, 1200);
        })();
        </script>"""
