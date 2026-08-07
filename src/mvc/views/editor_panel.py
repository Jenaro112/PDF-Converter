from PyQt6.QtWidgets import QPlainTextEdit, QWidget, QTextEdit
from PyQt6.QtGui import QFont, QColor, QPainter, QPaintEvent, QTextFormat
from PyQt6.QtCore import Qt, QRect, QSize, pyqtSignal
from PyQt6.QtGui import QKeySequence
from .markdown_highlighter import MarkdownHighlighter

class LineNumberArea(QWidget):
    """Widget lateral que dibuja los números de línea para el editor QPlainTextEdit."""
    def __init__(self, editor: 'EditorPanel'):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self) -> QSize:
        return QSize(self.code_editor.line_number_area_width(), 0)

    def paintEvent(self, event: QPaintEvent):
        self.code_editor.line_number_area_paint_event(event)

class EditorPanel(QPlainTextEdit):
    """
    Editor Markdown con características avanzadas estilo IDE:
    - Gutter con números de línea dinámicos
    - Resaltado de sintaxis Markdown en vivo (MarkdownHighlighter)
    - Resaltado de la línea actual del cursor
    - Tipografía monoespaciada prolija (JetBrains Mono / Fira Code)
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFont(QFont("JetBrains Mono", 11))
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(" ") * 4)

        # Placeholder con estilo acorde
        self.setPlaceholderText("Escribí Markdown aquí…")

        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #0b0c16;
                color: #e8eaed;
                border: none;
                padding: 8px 12px;
                selection-background-color: #282e4a;
                selection-color: #ffffff;
                font-family: 'JetBrains Mono', 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
                font-size: 10.5pt;
            }
        """)

        # Widget de números de línea (Gutter)
        self.line_number_area = LineNumberArea(self)

        # Conectar señales para actualización de línea y números
        self.blockCountChanged.connect(self._update_line_number_area_width)
        self.updateRequest.connect(self._update_line_number_area)
        self.cursorPositionChanged.connect(self._highlight_current_line)

        self._update_line_number_area_width(0)
        self._highlight_current_line()

        # Resaltador de sintaxis Markdown en vivo
        self.highlighter = MarkdownHighlighter(self.document())

    def line_number_area_width(self) -> int:
        digits = 1
        max_blocks = max(1, self.blockCount())
        while max_blocks >= 10:
            max_blocks //= 10
            digits += 1
        space = 16 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def _update_line_number_area_width(self, _=0):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def _update_line_number_area(self, rect: QRect, dy: int):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self._update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(
            QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height())
        )

    def _highlight_current_line(self):
        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor("#161826")
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)
        self.line_number_area.update()

    def line_number_area_paint_event(self, event: QPaintEvent):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor("#121422"))

        # Borde derecho del gutter
        painter.setPen(QColor("#1e2235"))
        painter.drawLine(event.rect().topRight(), event.rect().bottomRight())

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(block).height())

        current_block_number = self.textCursor().block().blockNumber()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                if block_number == current_block_number:
                    painter.setPen(QColor("#73d0ff"))  # Resaltar número de línea activa
                    font = painter.font()
                    font.setBold(True)
                    painter.setFont(font)
                else:
                    painter.setPen(QColor("#4a5278"))  # Líneas inactivas
                    font = painter.font()
                    font.setBold(False)
                    painter.setFont(font)

                painter.drawText(
                    0, top, self.line_number_area.width() - 8, self.fontMetrics().height(),
                    Qt.AlignmentFlag.AlignRight, number
                )

            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            block_number += 1

    def insertFromMimeData(self, source):
        """Turn clipboard images into document-owned Markdown images.

        The controller owns persistence because it knows the active .md path.
        Text pastes keep Qt's normal, undoable behaviour.
        """
        if source.hasImage():
            image = source.imageData()
            if image is not None:
                self.image_pasted.emit(image)
                return
        super().insertFromMimeData(source)
    image_pasted = pyqtSignal(object)
