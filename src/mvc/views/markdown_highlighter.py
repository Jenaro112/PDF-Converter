from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor
from PyQt6.QtCore import QRegularExpression
from mvc.models.theme_manager import PASTEL_COLORS

class MarkdownHighlighter(QSyntaxHighlighter):
    """
    Resaltador de sintaxis Markdown en vivo para el editor estilo IDE.
    Soporta encabezados H1-H6, negrita, cursiva, código inline, bloques de código,
    citas, enlaces, marcadores pastel ==texto==(color) en vivo y saltos de página.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_formats()
        self._init_rules()

    def _color(self, hex_color: str) -> QColor:
        return QColor(hex_color)

    def _init_formats(self):
        # 1. Encabezados (H1 - H6)
        self.h_formats = []
        h_colors = ["#ff79c6", "#bd93f9", "#f1fa8c", "#8be9fd", "#50fa7b", "#ffb86c"]
        for i in range(6):
            fmt = QTextCharFormat()
            fmt.setFontWeight(QFont.Weight.Bold)
            fmt.setForeground(self._color(h_colors[i]))
            self.h_formats.append(fmt)

        # 2. Negrita
        self.bold_delim_fmt = QTextCharFormat()
        self.bold_delim_fmt.setForeground(self._color("#5c6370"))

        self.bold_text_fmt = QTextCharFormat()
        self.bold_text_fmt.setFontWeight(QFont.Weight.Bold)
        self.bold_text_fmt.setForeground(self._color("#e8eaed"))

        # 3. Cursiva
        self.italic_delim_fmt = QTextCharFormat()
        self.italic_delim_fmt.setForeground(self._color("#5c6370"))

        self.italic_text_fmt = QTextCharFormat()
        self.italic_text_fmt.setFontItalic(True)
        self.italic_text_fmt.setForeground(self._color("#e8eaed"))

        # 4. Código Inline
        self.inline_code_fmt = QTextCharFormat()
        self.inline_code_fmt.setFontFamilies(["JetBrains Mono", "Fira Code", "Consolas", "monospace"])
        self.inline_code_fmt.setForeground(self._color("#e5c07b"))
        self.inline_code_fmt.setBackground(self._color("#1e2235"))

        # 5. Bloques de Código (Fence line: ```)
        self.code_fence_fmt = QTextCharFormat()
        self.code_fence_fmt.setFontFamilies(["JetBrains Mono", "Fira Code", "Consolas", "monospace"])
        self.code_fence_fmt.setForeground(self._color("#61afef"))
        self.code_fence_fmt.setBackground(self._color("#1a1d2d"))
        self.code_fence_fmt.setFontWeight(QFont.Weight.Bold)

        self.code_block_inside_fmt = QTextCharFormat()
        self.code_block_inside_fmt.setFontFamilies(["JetBrains Mono", "Fira Code", "Consolas", "monospace"])
        self.code_block_inside_fmt.setForeground(self._color("#abb2bf"))
        self.code_block_inside_fmt.setBackground(self._color("#161824"))

        # 6. Citas (> texto)
        self.quote_prefix_fmt = QTextCharFormat()
        self.quote_prefix_fmt.setForeground(self._color("#c9a84c"))
        self.quote_prefix_fmt.setFontWeight(QFont.Weight.Bold)

        self.quote_text_fmt = QTextCharFormat()
        self.quote_text_fmt.setForeground(self._color("#c9a84c"))
        self.quote_text_fmt.setFontItalic(True)

        # 7. Enlaces [texto](url)
        self.link_delim_fmt = QTextCharFormat()
        self.link_delim_fmt.setForeground(self._color("#5c6370"))

        self.link_text_fmt = QTextCharFormat()
        self.link_text_fmt.setForeground(self._color("#61afef"))
        self.link_text_fmt.setFontWeight(QFont.Weight.Bold)

        self.link_url_fmt = QTextCharFormat()
        self.link_url_fmt.setForeground(self._color("#569cd6"))
        self.link_url_fmt.setFontItalic(True)

        # 8. Saltos de página <!-- PAGEBREAK --> / \newpage
        self.pagebreak_fmt = QTextCharFormat()
        self.pagebreak_fmt.setForeground(self._color("#ff79c6"))
        self.pagebreak_fmt.setBackground(self._color("#2d3149"))
        self.pagebreak_fmt.setFontWeight(QFont.Weight.Bold)

        # 9. Listas
        self.list_fmt = QTextCharFormat()
        self.list_fmt.setForeground(self._color("#50fa7b"))
        self.list_fmt.setFontWeight(QFont.Weight.Bold)

    def _init_rules(self):
        self._rules = []

        # Encabezados H6 a H1 (para priorizar patrones más largos de #)
        for i in range(6, 0, -1):
            pattern = QRegularExpression(rf'^(#{{{i}}})(\s+.*)$')
            self._rules.append(('heading', pattern, i - 1))

        # Salto de página
        pagebreak_pattern = QRegularExpression(r'^\s*(<!--\s*PAGE-?BREAK\s*-->|[-=]{3,}\s*PAGE-?BREAK\s*[-=]{3,}|\\{1,2}(?:newpage|pagebreak))\s*$', QRegularExpression.PatternOption.CaseInsensitiveOption)
        self._rules.append(('pagebreak', pagebreak_pattern, None))

        # Citas
        self._rules.append(('quote', QRegularExpression(r'^(>)\s*(.*)$'), None))

        # Listas
        self._rules.append(('list', QRegularExpression(r'^\s*([-*+]|\d+\.)\s'), None))

        # Bloque de código apertura/cierre
        self._rules.append(('fence', QRegularExpression(r'^\s*```.*$'), None))

        # Enlaces [texto](url)
        self._rules.append(('link', QRegularExpression(r'(\[)([^\]]+)(\]\()([^\)]+)(\))'), None))

        # Negrita **texto** o __texto__
        self._rules.append(('bold', QRegularExpression(r'(\*\*|__)(.*?)\1'), None))

        # Cursiva *texto* o _texto_
        self._rules.append(('italic', QRegularExpression(r'(?<![\*_])(\*|_)(?!\1)(.*?)\1'), None))

        # Código inline `código`
        self._rules.append(('inline_code', QRegularExpression(r'`[^`]+`'), None))

        # Resaltado pastel ==texto==(color) o ==texto==
        self._rules.append(('highlight_color', QRegularExpression(r'==((?:(?!==).)+?)==\(([^)]+)\)'), None))
        self._rules.append(('highlight_default', QRegularExpression(r'==((?:(?!==).)+?)=='), None))

    def highlightBlock(self, text: str):
        # Manejo de bloques multilinea de código ```
        prev_state = self.previousBlockState()
        in_code_block = (prev_state == 1)

        is_fence = text.strip().startswith('```')

        if in_code_block:
            self.setFormat(0, len(text), self.code_block_inside_fmt)
            if is_fence:
                self.setFormat(0, len(text), self.code_fence_fmt)
                self.setCurrentBlockState(0)
            else:
                self.setCurrentBlockState(1)
            return
        elif is_fence:
            self.setFormat(0, len(text), self.code_fence_fmt)
            self.setCurrentBlockState(1)
            return
        else:
            self.setCurrentBlockState(0)

        # Reglas estándar por bloque
        for rule_type, pattern, idx in self._rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                match = it.next()
                start = match.capturedStart()
                length = match.capturedLength()

                if rule_type == 'heading':
                    # # Hash symbols y espacio
                    prefix_len = match.capturedLength(1)
                    self.setFormat(start, prefix_len, self.bold_delim_fmt)
                    self.setFormat(start + prefix_len, length - prefix_len, self.h_formats[idx])

                elif rule_type == 'pagebreak':
                    self.setFormat(start, length, self.pagebreak_fmt)

                elif rule_type == 'quote':
                    self.setFormat(match.capturedStart(1), match.capturedLength(1), self.quote_prefix_fmt)
                    if match.capturedLength(2) > 0:
                        self.setFormat(match.capturedStart(2), match.capturedLength(2), self.quote_text_fmt)

                elif rule_type == 'list':
                    self.setFormat(start, length, self.list_fmt)

                elif rule_type == 'link':
                    # [ texto ] ( url )
                    self.setFormat(match.capturedStart(1), match.capturedLength(1), self.link_delim_fmt)
                    self.setFormat(match.capturedStart(2), match.capturedLength(2), self.link_text_fmt)
                    self.setFormat(match.capturedStart(3), match.capturedLength(3), self.link_delim_fmt)
                    self.setFormat(match.capturedStart(4), match.capturedLength(4), self.link_url_fmt)
                    self.setFormat(match.capturedStart(5), match.capturedLength(5), self.link_delim_fmt)

                elif rule_type == 'bold':
                    d_len = match.capturedLength(1)
                    self.setFormat(start, d_len, self.bold_delim_fmt)
                    self.setFormat(start + d_len, match.capturedLength(2), self.bold_text_fmt)
                    self.setFormat(start + d_len + match.capturedLength(2), d_len, self.bold_delim_fmt)

                elif rule_type == 'italic':
                    d_len = match.capturedLength(1)
                    self.setFormat(start, d_len, self.italic_delim_fmt)
                    self.setFormat(start + d_len, match.capturedLength(2), self.italic_text_fmt)
                    self.setFormat(start + d_len + match.capturedLength(2), d_len, self.italic_delim_fmt)

                elif rule_type == 'inline_code':
                    self.setFormat(start, length, self.inline_code_fmt)

                elif rule_type in ('highlight_color', 'highlight_default'):
                    color_param = match.captured(2).lower().strip() if rule_type == 'highlight_color' else 'amarillo'
                    hex_color = PASTEL_COLORS.get(color_param, color_param if color_param.startswith('#') else PASTEL_COLORS['amarillo'])

                    fmt = QTextCharFormat()
                    fmt.setBackground(self._color(hex_color))
                    fmt.setForeground(self._color("#1a1a1a"))  # Texto oscuro para legibilidad sobre pastel
                    fmt.setFontWeight(QFont.Weight.Bold)
                    self.setFormat(start, length, fmt)
