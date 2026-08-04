from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QMainWindow, QSplitter, QToolBar, QComboBox, QFileDialog,
    QLabel, QWidget, QStatusBar, QMenu, QToolButton, QColorDialog,
    QPushButton, QHBoxLayout, QVBoxLayout, QFrame, QSizePolicy, QLineEdit,
    QListWidget, QListWidgetItem, QDockWidget, QMessageBox
)
from PyQt6.QtGui import QAction, QColor, QIcon, QPixmap, QPainter, QTextCursor, QTextDocument, QKeySequence

from .editor_panel import EditorPanel
from .preview_panel import PreviewPanel
from mvc.models.theme_manager import PASTEL_COLORS, THEMES

def create_color_icon(hex_color: str) -> QIcon:
    pixmap = QPixmap(16, 16)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(QColor(hex_color))
    painter.setPen(QColor("#64748b"))
    painter.drawRoundedRect(1, 1, 14, 14, 4, 4)
    painter.end()
    return QIcon(pixmap)

def create_theme_icon(theme_key: str) -> QIcon:
    theme = THEMES.get(theme_key, THEMES['minimal'])
    bg_color = theme.get('page_bg', '#ffffff')
    accent_color = theme.get('accent_color', '#3a3a3a')

    pixmap = QPixmap(16, 16)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    # Mitad izquierda bg, mitad derecha acento
    painter.setBrush(QColor(bg_color))
    painter.setPen(QColor("#475569"))
    painter.drawRoundedRect(1, 1, 14, 14, 3, 3)

    painter.setBrush(QColor(accent_color))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(8, 2, 6, 12, 1, 1)

    painter.end()
    return QIcon(pixmap)

class MainWindow(QMainWindow):
    # Señales emitidas al Controlador
    text_changed = pyqtSignal(str)
    theme_changed = pyqtSignal(str)
    options_changed = pyqtSignal(dict)
    export_requested = pyqtSignal()
    file_opened = pyqtSignal(str)
    cover_requested = pyqtSignal()
    closed = pyqtSignal()
    combine_requested = pyqtSignal()
    highlights_requested = pyqtSignal()
    
    def __init__(self, theme_choices: list[tuple[str, str]]):
        super().__init__()
        self.setWindowTitle("PDF Converter — Editor Markdown & IDE")
        self.resize(1400, 900)
        
        self.theme_choices = theme_choices
        
        self.setStyleSheet("""
            QMainWindow { background-color: #0f111a; }
            QStatusBar {
                background-color: #0b0c16;
                color: #94a3b8;
                font-family: 'Inter', sans-serif;
                font-size: 9pt;
                border-top: 1px solid #1e2235;
                padding: 4px;
            }
            QSplitter::handle { background-color: #1e2235; width: 2px; }
            
            QToolBar {
                background-color: #121420;
                border-bottom: 1px solid #1e2235;
                padding: 6px 12px;
                spacing: 12px;
            }
            
            /* Tarjeta / Contenedor de Grupo */
            QFrame.toolbar-group {
                background-color: #1a1d2e;
                border: 1px solid #2a2e45;
                border-radius: 8px;
            }
            
            /* Botones principales de la toolbar */
            QPushButton.toolbar-btn, QToolButton.toolbar-btn {
                background-color: transparent;
                color: #e2e8f0;
                border: none;
                border-radius: 6px;
                padding: 5px 12px;
                font-family: 'Inter', sans-serif;
                font-size: 9pt;
                font-weight: 500;
            }
            QPushButton.toolbar-btn:hover, QToolButton.toolbar-btn:hover {
                background-color: #282c44;
                color: #ffffff;
            }
            QPushButton.toolbar-btn:pressed, QToolButton.toolbar-btn:pressed {
                background-color: #3b4266;
            }
            
            QPushButton.toolbar-btn-exit {
                background-color: #451a1a;
                color: #fca5a5;
                border: 1px solid #7f1d1d;
                border-radius: 6px;
                padding: 5px 12px;
                font-family: 'Inter', sans-serif;
                font-size: 9pt;
                font-weight: 600;
            }
            QPushButton.toolbar-btn-exit:hover {
                background-color: #7f1d1d;
                color: #ffffff;
            }
            
            /* Selector de Tema */
            QComboBox.theme-combo {
                background-color: #121422;
                color: #f8fafc;
                border: 1px solid #3b4261;
                border-radius: 6px;
                padding: 4px 10px;
                font-family: 'Inter', sans-serif;
                font-size: 9pt;
                font-weight: 500;
            }
            QComboBox.theme-combo:hover {
                border-color: #60a5fa;
            }
            QComboBox.theme-combo::drop-down {
                border: none;
                width: 16px;
            }
            QComboBox.theme-combo QAbstractItemView {
                background-color: #161927;
                color: #f8fafc;
                selection-background-color: #2563eb;
                selection-color: #ffffff;
                border: 1px solid #3b4261;
                border-radius: 6px;
                padding: 4px;
            }
            
            QLabel.group-label {
                color: #64748b;
                font-family: 'Inter', sans-serif;
                font-size: 8.5pt;
                font-weight: 600;
                margin-right: 4px;
            }
        """)

        self._init_ui()
        self._init_toolbar()
        self._init_shortcuts()

    def _init_ui(self):
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)

        self.editor = EditorPanel()
        self.editor.textChanged.connect(self._on_text_changed)
        
        self.preview = PreviewPanel()
        
        splitter.addWidget(self.editor)
        splitter.addWidget(self.preview)
        splitter.setSizes([700, 700])
        
        self.setCentralWidget(splitter)

        self.outline_dock = QDockWidget("Índice", self)
        self.outline_dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable)
        self.outline = QListWidget()
        self.outline.setStyleSheet("QListWidget { background:#121420; color:#e2e8f0; border:0; padding:6px; }")
        self.outline.itemClicked.connect(self._go_to_outline_item)
        self.outline_dock.setWidget(self.outline)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.outline_dock)
        
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Listo")

    def _init_toolbar(self):
        toolbar = QToolBar("Herramientas")
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        self.addToolBar(toolbar)

        # -------------------------------------------------------------
        # Grupo 1: ARCHIVO (Abrir Archivo, Exportar PDF)
        # -------------------------------------------------------------
        grp_file = QFrame()
        grp_file.setProperty("class", "toolbar-group")
        lay_file = QHBoxLayout(grp_file)
        lay_file.setContentsMargins(4, 3, 4, 3)
        lay_file.setSpacing(4)

        btn_open = QPushButton("📂 Abrir Archivo")
        btn_open.setProperty("class", "toolbar-btn")
        btn_open.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_open.clicked.connect(self._on_open_file)
        lay_file.addWidget(btn_open)

        btn_export = QPushButton("📤 Exportar PDF")
        btn_export.setProperty("class", "toolbar-btn")
        btn_export.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_export.clicked.connect(self.export_requested.emit)
        lay_file.addWidget(btn_export)

        btn_combine = QPushButton("🧩 Combinar")
        btn_combine.setProperty("class", "toolbar-btn")
        btn_combine.clicked.connect(self.combine_requested.emit)
        lay_file.addWidget(btn_combine)

        toolbar.addWidget(grp_file)

        # -------------------------------------------------------------
        # Grupo 2: DOCUMENTO (Tema, Configurar Portada)
        # -------------------------------------------------------------
        grp_doc = QFrame()
        grp_doc.setProperty("class", "toolbar-group")
        lay_doc = QHBoxLayout(grp_doc)
        lay_doc.setContentsMargins(8, 3, 4, 3)
        lay_doc.setSpacing(6)

        lbl_theme = QLabel("Tema:")
        lbl_theme.setProperty("class", "group-label")
        lay_doc.addWidget(lbl_theme)

        self.theme_selector = QComboBox()
        self.theme_selector.setProperty("class", "theme-combo")
        self.theme_selector.setCursor(Qt.CursorShape.PointingHandCursor)

        for label, key in self.theme_choices:
            icon = create_theme_icon(key)
            self.theme_selector.addItem(icon, label, key)

        self.theme_selector.currentIndexChanged.connect(self._on_options_changed)
        lay_doc.addWidget(self.theme_selector)

        btn_cover = QPushButton("📖 Configurar Portada")
        btn_cover.setProperty("class", "toolbar-btn")
        btn_cover.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cover.clicked.connect(self.cover_requested.emit)
        lay_doc.addWidget(btn_cover)

        toolbar.addWidget(grp_doc)

        # -------------------------------------------------------------
        # Grupo 3: FORMATO (Resaltar)
        # -------------------------------------------------------------
        grp_fmt = QFrame()
        grp_fmt.setProperty("class", "toolbar-group")
        lay_fmt = QHBoxLayout(grp_fmt)
        lay_fmt.setContentsMargins(4, 3, 4, 3)
        lay_fmt.setSpacing(4)

        highlight_btn = QToolButton(self)
        highlight_btn.setText("🖍 Resaltar")
        highlight_btn.setProperty("class", "toolbar-btn")
        highlight_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        highlight_btn.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        highlight_btn.clicked.connect(lambda: self._apply_highlight("amarillo"))
        
        highlight_menu = QMenu(self)
        highlight_menu.setStyleSheet("""
            QMenu {
                background-color: #161927;
                color: #e2e8f0;
                border: 1px solid #3b4261;
                border-radius: 6px;
                padding: 4px;
            }
            QMenu::item {
                padding: 6px 12px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #2563eb;
                color: #ffffff;
            }
        """)

        for name, hex_color in PASTEL_COLORS.items():
            icon = create_color_icon(hex_color)
            action = QAction(icon, name.capitalize(), self)
            action.triggered.connect(self._create_highlight_handler(name))
            highlight_menu.addAction(action)

        highlight_menu.addSeparator()
        custom_action = QAction("🎨 Color Personalizado...", self)
        custom_action.triggered.connect(self._choose_custom_highlight)
        highlight_menu.addAction(custom_action)

        highlight_btn.setMenu(highlight_menu)
        lay_fmt.addWidget(highlight_btn)

        btn_find = QPushButton("⌕ Buscar")
        btn_find.setProperty("class", "toolbar-btn")
        btn_find.clicked.connect(self.show_find_panel)
        lay_fmt.addWidget(btn_find)

        btn_highlights = QPushButton("📚 Resaltados")
        btn_highlights.setProperty("class", "toolbar-btn")
        btn_highlights.clicked.connect(self.highlights_requested.emit)
        lay_fmt.addWidget(btn_highlights)

        toolbar.addWidget(grp_fmt)

        # Spacer expansivo a la derecha
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        toolbar.addWidget(spacer)

        # Grupo Sistema (Salir)
        grp_sys = QFrame()
        grp_sys.setProperty("class", "toolbar-group")
        lay_sys = QHBoxLayout(grp_sys)
        lay_sys.setContentsMargins(4, 3, 4, 3)
        lay_sys.setSpacing(4)

        btn_exit = QPushButton("❌ Salir")
        btn_exit.setProperty("class", "toolbar-btn-exit")
        btn_exit.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_exit.clicked.connect(self.close)
        lay_sys.addWidget(btn_exit)

        toolbar.addWidget(grp_sys)

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

    def _create_highlight_handler(self, color_name: str):
        return lambda: self._apply_highlight(color_name)

    def _apply_highlight(self, color_name_or_hex: str):
        # The active cursor is read here, at the colour action, never when the
        # menu was opened.  This prevents stale selections from being wrapped.
        cursor = self.editor.textCursor()
        selected_text = cursor.selectedText()
        if selected_text:
            cursor.insertText(f"=={selected_text}==({color_name_or_hex})")
        else:
            cursor.insertText(f"==texto==({color_name_or_hex})")
            pos = cursor.position()
            cursor.setPosition(pos - len(color_name_or_hex) - 3 - 5)
            cursor.setPosition(pos - len(color_name_or_hex) - 3, QTextCursor.MoveMode.KeepAnchor)
            self.editor.setTextCursor(cursor)
        self.editor.setFocus()

    # Keyboard bindings deliberately live together so Ctrl mappings can be
    # introduced later without searching through widget code.
    KEY_BINDINGS = {
        'find': 'Meta+F', 'bold': 'Meta+B', 'italic': 'Meta+I',
        'link': 'Meta+K', 'highlight': 'Meta+Shift+H', 'save': 'Meta+S',
    }

    def _init_shortcuts(self):
        for name, callback in {
            'find': self.show_find_panel, 'bold': lambda: self._wrap_selection('**', '**'),
            'italic': lambda: self._wrap_selection('*', '*'), 'link': self._insert_link,
            'highlight': lambda: self._apply_highlight('amarillo'), 'save': self._save_document,
        }.items():
            action = QAction(self)
            action.setShortcut(QKeySequence(self.KEY_BINDINGS[name]))
            action.triggered.connect(callback)
            self.addAction(action)

    def _wrap_selection(self, prefix, suffix):
        cursor = self.editor.textCursor()
        selected = cursor.selectedText()
        if selected:
            cursor.insertText(f'{prefix}{selected}{suffix}')
        else:
            cursor.insertText(f'{prefix}texto{suffix}')
            cursor.setPosition(cursor.position() - len(suffix) - 5)
            cursor.setPosition(cursor.position() + 5, QTextCursor.MoveMode.KeepAnchor)
            self.editor.setTextCursor(cursor)
        self.editor.setFocus()

    def _insert_link(self):
        cursor = self.editor.textCursor()
        label = cursor.selectedText() or 'texto'
        cursor.insertText(f'[{label}](url)')
        if not cursor.hasSelection():
            pos = cursor.position()
            cursor.setPosition(pos - 4)
            cursor.setPosition(pos - 1, QTextCursor.MoveMode.KeepAnchor)
            self.editor.setTextCursor(cursor)
        self.editor.setFocus()

    def _save_document(self):
        # The controller owns the concrete path; emitting a normal open/save
        # action is avoided here so shortcuts remain decoupled from persistence.
        self.save_requested.emit()

    save_requested = pyqtSignal()

    def show_find_panel(self):
        if hasattr(self, 'find_dock'):
            self.find_dock.show(); self.find_input.setFocus(); return
        self.find_dock = QDockWidget('Buscar y reemplazar', self)
        panel = QWidget(); layout = QVBoxLayout(panel)
        self.find_input, self.replace_input = QLineEdit(), QLineEdit()
        self.find_input.setPlaceholderText('Buscar…'); self.replace_input.setPlaceholderText('Reemplazar por…')
        buttons = QHBoxLayout()
        for text, fn in [('◀', lambda: self._find(False)), ('▶', lambda: self._find(True)), ('Reemplazar', self._replace_one), ('Todo', self._replace_all)]:
            button = QPushButton(text); button.clicked.connect(fn); buttons.addWidget(button)
        layout.addWidget(self.find_input); layout.addWidget(self.replace_input); layout.addLayout(buttons)
        self.find_dock.setWidget(panel); self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.find_dock)
        self.find_input.returnPressed.connect(lambda: self._find(True)); self.find_input.setFocus()

    def _find(self, forward=True):
        term = self.find_input.text()
        if not term: return
        flags = QTextDocument.FindFlag(0)
        if not forward: flags |= QTextDocument.FindFlag.FindBackward
        found = self.editor.find(term, flags)
        if not found:
            cursor = self.editor.textCursor(); cursor.movePosition(QTextCursor.MoveOperation.Start if forward else QTextCursor.MoveOperation.End)
            self.editor.setTextCursor(cursor); self.editor.find(term, flags)

    def _replace_one(self):
        if self.editor.textCursor().hasSelection() and self.editor.textCursor().selectedText() == self.find_input.text():
            self.editor.textCursor().insertText(self.replace_input.text())
        self._find(True)

    def _replace_all(self):
        term = self.find_input.text()
        if not term: return
        text = self.editor.toPlainText(); count = text.count(term)
        if count: self.editor.setPlainText(text.replace(term, self.replace_input.text()))
        self.status.showMessage(f'{count} coincidencia(s) reemplazada(s)', 2500)

    def update_outline(self, headings):
        self.outline.clear()
        for level, title, block in headings:
            item = QListWidgetItem(('    ' * (level - 1)) + title)
            item.setData(Qt.ItemDataRole.UserRole, block)
            self.outline.addItem(item)

    def _go_to_outline_item(self, item):
        block = self.editor.document().findBlockByNumber(item.data(Qt.ItemDataRole.UserRole))
        if block.isValid():
            cursor = QTextCursor(block); self.editor.setTextCursor(cursor); self.editor.centerCursor(); self.editor.setFocus()

    def _choose_custom_highlight(self):
        color = QColorDialog.getColor(QColor("#fff3b0"), self, "Seleccionar Color Pastel")
        if color.isValid():
            hex_color = color.name()
            self._apply_highlight(hex_color)

    def _on_text_changed(self):
        self.text_changed.emit(self.editor.toPlainText())
        
    def _on_options_changed(self):
        options = {
            'theme': self.theme_selector.currentData(),
        }
        self.options_changed.emit(options)
        
    def get_current_options(self) -> dict:
        return {
            'theme': self.theme_selector.currentData(),
        }
        
    def set_preview_html(self, html: str):
        self.preview.set_html(html)
        self.status.showMessage("Vista previa actualizada", 2000)

    def show_status(self, message: str, timeout: int = 0):
        self.status.showMessage(message, timeout)

    def _on_open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Abrir Archivo",
            "",
            "Documentos (*.md *.docx);;Markdown (*.md);;Word (*.docx)"
        )
        if file_path:
            self.file_opened.emit(file_path)
