import re
from typing import Optional


class MarkdownFormatter:
    """
    Formateador de Markdown seguro y de alta fidelidad.
    
    Protege fórmulas matemáticas de KaTeX/LaTeX, resaltados pastel, bloques de código,
    marcadores de paginación y diagramas Mermaid contra la corrupción producida
    por el formateador CommonMark estándar (mdformat).
    """

    @classmethod
    def format_text(cls, text: str) -> str:
        """
        Formatea el texto Markdown respetando todas las sintaxis extendidas.
        """
        if not text or not text.strip():
            return text

        import mdformat

        tokens: dict[str, str] = {}
        counter = 0

        def get_token(val: str, prefix: str = "TKN") -> str:
            nonlocal counter
            # Token estrictamente alfanumérico para no ser interpretado por CommonMark
            token = f"XPROTECTED{prefix}{counter}X"
            tokens[token] = val
            counter += 1
            return token

        # 1. Proteger bloques de código multilínea (``` o ~~~)
        def _repl_fenced_code(m: re.Match) -> str:
            return get_token(m.group(0), "FCODE")

        text_protected = re.sub(
            r'(```[^\n]*\n[\s\S]*?\n```|~~~[^\n]*\n[\s\S]*?\n~~~)',
            _repl_fenced_code,
            text
        )

        # 2. Proteger código en línea (`...`)
        def _repl_inline_code(m: re.Match) -> str:
            return get_token(m.group(0), "ICODE")

        text_protected = re.sub(r'(`+[^`\n]+?`+)', _repl_inline_code, text_protected)

        # 3. Proteger matemáticas en bloque ($$ ... $$)
        def _repl_disp_math(m: re.Match) -> str:
            return get_token(m.group(0), "DMATH")

        text_protected = re.sub(r'\$\$([\s\S]*?)\$\$', _repl_disp_math, text_protected)

        # 4. Proteger delimitadores de corchetes LaTeX \[ ... \] y \( ... \)
        def _repl_bracket_math(m: re.Match) -> str:
            return get_token(m.group(0), "BMATH")

        text_protected = re.sub(r'\\\[[\s\S]*?\\\]', _repl_bracket_math, text_protected)
        text_protected = re.sub(r'\\\([\s\S]*?\\\)', _repl_bracket_math, text_protected)

        # 5. Proteger signos de dólar escapados (\$ o \\$)
        def _repl_esc_dollar(m: re.Match) -> str:
            return get_token(m.group(0), "ESCDOL")

        text_protected = re.sub(r'\\\$', _repl_esc_dollar, text_protected)

        # 6. Proteger matemáticas en línea ($ ... $)
        def _repl_inline_math(m: re.Match) -> str:
            return get_token(m.group(0), "IMATH")

        text_protected = re.sub(
            r'(?<!\$)\$(?!\$)(?!\s)([^\n\$]+?)(?<!\s)(?<!\$)\$(?!\$)',
            _repl_inline_math,
            text_protected
        )

        # 7. Proteger marcadores especiales y saltos de página manuales
        def _repl_custom_markers(m: re.Match) -> str:
            return get_token(m.group(0), "CUSTOM")

        text_protected = re.sub(
            r'<!--\s*(?:PAGE-?BREAK|TOC)\s*-->',
            _repl_custom_markers,
            text_protected,
            flags=re.IGNORECASE
        )
        text_protected = re.sub(
            r'\\(?:newpage|pagebreak)',
            _repl_custom_markers,
            text_protected
        )

        # Formatear el texto protegido con mdformat
        formatted = mdformat.text(text_protected)

        # 8. Restaurar todos los tokens en orden inverso de captura
        for token, original_val in reversed(list(tokens.items())):
            formatted = formatted.replace(token, original_val)

        # 9. Post-procesamiento estético
        # Reemplazar líneas de subrayado excesivas de mdformat (ej: 70 guiones bajos) por '---'
        formatted = re.sub(r'^_{3,}\s*$', '---', formatted, flags=re.MULTILINE)

        # Reemplazar saltos de línea con contrabarra final (\) por dos espacios para compatibilidad con Python-Markdown
        formatted = re.sub(r'(?<!\\)\\\n', '  \n', formatted)

        return formatted
