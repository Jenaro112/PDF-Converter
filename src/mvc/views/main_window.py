import platform
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QMainWindow, QSplitter, QComboBox, QFileDialog,
    QLabel, QWidget, QStatusBar, QMenu, QToolButton, QColorDialog,
    QPushButton, QHBoxLayout, QVBoxLayout, QFrame, QSizePolicy, QLineEdit,
    QDockWidget, QMessageBox, QTreeView, QFileSystemModel
)
from PySide6.QtGui import QAction, QColor, QIcon, QPixmap, QPainter, QTextCursor, QTextDocument, QKeySequence

from .editor_panel import EditorPanel
from .preview_panel import PreviewPanel
from mvc.models.theme_manager import PASTEL_COLORS, THEMES


# ── Cross-platform font stacks ──────────────────────────────────────
_FONT_UI = "'Inter', 'Segoe UI', system-ui, sans-serif"
_FONT_MONO = "'JetBrains Mono', 'Cascadia Code', 'Consolas', monospace"

# ── Catppuccin Mocha Palette ─────────────────────────────────────────
_BASE      = "#1e1e2e"
_MANTLE    = "#181825"
_CRUST     = "#11111b"
_SURFACE0  = "#313244"
_SURFACE1  = "#45475a"
_SURFACE2  = "#585b70"
_OVERLAY0  = "#6c7086"
_OVERLAY1  = "#7f849c"
_SUBTEXT0  = "#a6adc8"
_SUBTEXT1  = "#bac2de"
_TEXT      = "#cdd6f4"
_BLUE      = "#89b4fa"
_LAVENDER  = "#b4befe"
_SAPPHIRE  = "#74c7ec"
_GREEN     = "#a6e3a1"
_RED       = "#f38ba8"
_PEACH     = "#fab387"
_YELLOW    = "#f9e2af"

# ── SVG Icons ────────────────────────────────────────────────────────
def create_svg_icon(svg_path: str, color: str) -> QIcon:
    """Generates an SVG icon on the fly with the given color."""
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{svg_path}</svg>'
    pixmap = QPixmap()
    pixmap.loadFromData(svg.encode('utf-8'))
    return QIcon(pixmap)

SVG_PATHS = {
    'folder': '<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>',
    'export': '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="12" y1="18" x2="12" y2="12"></line><polyline points="9 15 12 18 15 15"></polyline>',
    'puzzle': '<path d="M19.439 7.85c-.049.322.059.648.289.878l1.568 1.568c.47.47.706 1.087.706 1.704s-.235 1.233-.706 1.704l-1.611 1.611a.98.98 0 0 1-.837.276c-.47-.07-.802-.48-.968-.925a2.501 2.501 0 1 0-3.214 3.214c.446.166.855.497.925.968a.979.979 0 0 1-.276.837l-1.61 1.611c-.94.94-2.469.94-3.408 0L8.73 19.73a.98.98 0 0 1-.276-.837c.07-.47.48-.802.925-.968a2.5 2.5 0 1 0-3.214-3.214c-.166-.446-.497-.855-.968-.925a.979.979 0 0 1-.837-.276L2.749 11.9a2.41 2.41 0 0 1 0-3.408l1.568-1.568c.23-.23.556-.338.878-.289.467.071.799.48.966.925a2.5 2.5 0 1 0 3.214-3.214c-.446-.167-.855-.498-.925-.968a.979.979 0 0 1 .276-.837l1.611-1.61c.94-.94 2.469-.94 3.408 0l1.568 1.568c.23.23.556.338.878.289.467-.071.799-.48.966-.925a2.5 2.5 0 1 0 3.214 3.214c.167.446.498.855.968.925z"></path>',
    'layout': '<rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><line x1="9" y1="3" x2="9" y2="21"></line>',
    'marker': '<path d="M20.24 12.24a6 6 0 0 0-8.49-8.49L5 10.5V19h8.5z"></path><line x1="16" y1="8" x2="2" y2="22"></line><line x1="17.5" y1="15" x2="9" y2="15"></line>',
    'search': '<circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line>',
    'layers': '<polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline>',
    'exit': '<line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line>',
    'doc': '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline>',
    'zoom_in': '<circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line><line x1="11" y1="8" x2="11" y2="14"></line><line x1="8" y1="11" x2="14" y2="11"></line>',
    'zoom_out': '<circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line><line x1="8" y1="11" x2="14" y2="11"></line>',
    'download': '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line>',
    'file-text': '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline>',
    'pagebreak': '<path d="M4 18h4v-2H4v2zm0-5h16v-2H4v2zm0-7v2h16V6H4zm12 12h4v-2h-4v2zm-4 0h2v-2h-2v2z"></path>'
}


def create_color_icon(hex_color: str) -> QIcon:
    pixmap = QPixmap(16, 16)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(QColor(hex_color))
    painter.setPen(QColor(_SURFACE2))
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

    painter.setBrush(QColor(bg_color))
    painter.setPen(QColor(_SURFACE2))
    painter.drawRoundedRect(1, 1, 14, 14, 3, 3)

    painter.setBrush(QColor(accent_color))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(8, 2, 6, 12, 1, 1)

    painter.end()
    return QIcon(pixmap)


class PreviewWrapper(QWidget):
    """Wrapper around PreviewPanel adding a header with title and zoom controls.
    
    Matches the Visily mockup: SVG Document icon "Vista previa" on the left,
    zoom -/+/% and download SVG button on the right.
    """
    export_requested = Signal()

    def __init__(self, preview: PreviewPanel, parent=None):
        super().__init__(parent)
        self.preview = preview
        self._zoom_level = 100
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header bar
        header = QFrame()
        header.setObjectName("preview_header")
        header.setFixedHeight(36)
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(12, 0, 12, 0)
        h_layout.setSpacing(8)

        # SVG Doc Icon + Title
        lbl_icon = QLabel()
        lbl_icon.setPixmap(create_svg_icon(SVG_PATHS['doc'], _SUBTEXT0).pixmap(16, 16))
        h_layout.addWidget(lbl_icon)

        lbl_title = QLabel("Vista previa")
        lbl_title.setStyleSheet(f"color: {_TEXT}; font-weight: 600; font-size: 13px; background: transparent; border: none;")
        h_layout.addWidget(lbl_title)
        h_layout.addStretch()

        # Zoom controls (SVG Icons)
        btn_zoom_out = QPushButton()
        btn_zoom_out.setIcon(create_svg_icon(SVG_PATHS['zoom_out'], _SUBTEXT0))
        btn_zoom_out.setToolTip("Reducir zoom")
        btn_zoom_out.setFixedSize(30, 24)
        btn_zoom_out.clicked.connect(self._zoom_out)
        h_layout.addWidget(btn_zoom_out)

        self.zoom_label = QLabel("100%")
        self.zoom_label.setStyleSheet(f"color: {_SUBTEXT0}; font-size: 12px; background: transparent; border: none;")
        h_layout.addWidget(self.zoom_label)

        btn_zoom_in = QPushButton()
        btn_zoom_in.setIcon(create_svg_icon(SVG_PATHS['zoom_in'], _SUBTEXT0))
        btn_zoom_in.setToolTip("Aumentar zoom")
        btn_zoom_in.setFixedSize(30, 24)
        btn_zoom_in.clicked.connect(self._zoom_in)
        h_layout.addWidget(btn_zoom_in)

        # Add small separator
        sep = QFrame()
        sep.setFixedWidth(1)
        sep.setStyleSheet(f"background-color: {_SURFACE1}; margin: 4px 6px;")
        h_layout.addWidget(sep)

        # Download button
        btn_download = QPushButton()
        btn_download.setIcon(create_svg_icon(SVG_PATHS['download'], _SUBTEXT0))
        btn_download.setToolTip("Exportar PDF")
        btn_download.setFixedSize(30, 24)
        btn_download.clicked.connect(self.export_requested.emit)
        h_layout.addWidget(btn_download)

        layout.addWidget(header)
        layout.addWidget(self.preview, 1)

    def _zoom_in(self):
        if self._zoom_level < 200:
            self._zoom_level += 10
            self._apply_zoom()

    def _zoom_out(self):
        if self._zoom_level > 50:
            self._zoom_level -= 10
            self._apply_zoom()

    def _apply_zoom(self):
        factor = self._zoom_level / 100.0
        self.preview.setZoomFactor(factor)
        self.zoom_label.setText(f"{self._zoom_level}%")


class MainWindow(QMainWindow):
    # Señales emitidas al Controlador
    text_changed = Signal(str)
    theme_changed = Signal(str)
    options_changed = Signal(dict)
    export_requested = Signal()
    file_opened = Signal(str)
    file_selected_from_explorer = Signal(str)
    cover_requested = Signal()
    page_config_requested = Signal()
    closed = Signal()
    combine_requested = Signal()
    pagebreak_requested = Signal()
    save_requested = Signal()
    
    def __init__(self, theme_choices: list[tuple[str, str]]):
        super().__init__()
        self.setWindowTitle("PDF Converter — Editor Markdown & IDE")
        self.resize(1400, 900)
        
        self.theme_choices = theme_choices
        
        # Central layout
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setCentralWidget(self.main_widget)

        self._init_toolbar()
        self._init_ui()
        self._init_status_bar()
        self._init_shortcuts()

    def _init_ui(self):
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)

        # ── Explorer Panel ─────────────────────────────────────────────
        import os
        docs_path = os.path.join(os.getcwd(), 'docs')
        os.makedirs(docs_path, exist_ok=True)
        
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(docs_path)
        self.file_model.setNameFilters(["*.md"])
        self.file_model.setNameFilterDisables(False) # Hide non-matching instead of disabling
        
        self.explorer = QTreeView()
        self.explorer.setModel(self.file_model)
        self.explorer.setRootIndex(self.file_model.index(docs_path))
        self.explorer.setColumnHidden(1, True) # Size
        self.explorer.setColumnHidden(2, True) # Type
        self.explorer.setColumnHidden(3, True) # Date
        self.explorer.setHeaderHidden(True)
        self.explorer.setStyleSheet(f"QTreeView {{ background-color: {_MANTLE}; color: {_TEXT}; border: none; font-size: 13px; }} QTreeView::item:hover {{ background-color: {_SURFACE0}; }} QTreeView::item:selected {{ background-color: {_SURFACE1}; }}")
        
        self.explorer.clicked.connect(self._on_explorer_clicked)

        self.editor = EditorPanel()
        self.editor.textChanged.connect(self._on_text_changed)
        self.editor.cursorPositionChanged.connect(self._update_cursor_info)
        
        self.preview = PreviewPanel()
        self.preview_wrapper = PreviewWrapper(self.preview)
        self.preview_wrapper.export_requested.connect(self.export_requested.emit)
        
        splitter.addWidget(self.explorer)
        splitter.addWidget(self.editor)
        splitter.addWidget(self.preview_wrapper)
        splitter.setSizes([200, 600, 600])
        
        self.main_layout.addWidget(splitter, 1)

    def _on_explorer_clicked(self, index):
        if not self.file_model.isDir(index):
            file_path = self.file_model.filePath(index)
            self.file_selected_from_explorer.emit(file_path)

    def _create_separator(self):
        sep = QFrame()
        sep.setFixedWidth(1)
        sep.setStyleSheet(f"background-color: {_SURFACE0}; margin: 8px 6px;")
        return sep

    def _create_btn(self, text, icon_key, color, is_tool=False):
        btn = QToolButton() if is_tool else QPushButton()
        btn.setText(text)
        if icon_key:
            btn.setIcon(create_svg_icon(SVG_PATHS[icon_key], color))
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        return btn

    def _init_toolbar(self):
        """Custom QFrame toolbar matching the Visily mockup exactly."""
        self.toolbar = QFrame()
        self.toolbar.setObjectName("custom_toolbar")
        self.toolbar.setFixedHeight(48)
        self.toolbar.setStyleSheet(f"""
            #custom_toolbar {{
                background-color: {_MANTLE};
                border-bottom: 1px solid {_SURFACE0};
            }}
            QPushButton, QToolButton {{
                background-color: transparent;
                color: {_TEXT};
                border: 1px solid transparent;
                border-radius: 6px;
                padding: 6px 12px;
                font-family: {_FONT_UI};
                font-size: 13px;
                font-weight: 500;
            }}
            QPushButton:hover, QToolButton:hover {{
                background-color: {_SURFACE0};
                border-color: {_SURFACE1};
            }}
            QPushButton:pressed, QToolButton:pressed {{
                background-color: {_SURFACE1};
            }}
            QToolButton::menu-button {{
                border: none;
                background: transparent;
                width: 20px;
            }}
            QToolButton::menu-button:hover {{
                background-color: {_SURFACE0};
                border-radius: 6px;
            }}
            QToolButton::menu-indicator {{ image: none; width: 0px; }}
        """)

        t_layout = QHBoxLayout(self.toolbar)
        t_layout.setContentsMargins(12, 6, 12, 6)
        t_layout.setSpacing(6)

        # ── Group 1: FILE ────────────────────────────────────────────
        btn_open = self._create_btn(" Abrir Archivo", 'folder', _YELLOW)
        btn_open.clicked.connect(self._on_open_file)
        t_layout.addWidget(btn_open)

        btn_export = self._create_btn(" Exportar PDF", 'export', _BLUE)
        btn_export.clicked.connect(self.export_requested.emit)
        t_layout.addWidget(btn_export)

        btn_combine = self._create_btn(" Combinar", 'puzzle', _GREEN)
        btn_combine.clicked.connect(self.combine_requested.emit)
        t_layout.addWidget(btn_combine)

        t_layout.addWidget(self._create_separator())

        # ── Group 2: DOCUMENT ────────────────────────────────────────
        lbl_theme = QLabel("Tema:")
        lbl_theme.setStyleSheet(f"color: {_SUBTEXT0}; font-size: 13px; font-weight: 500;")
        t_layout.addWidget(lbl_theme)

        self.theme_selector = QComboBox()
        self.theme_selector.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_selector.setStyleSheet("""
            QComboBox {
                background-color: _SURFACE0; color: _TEXT;
                border: 1px solid _SURFACE1; border-radius: 6px;
                padding: 5px 28px 5px 12px; font-size: 13px; min-width: 200px;
            }
            QComboBox:hover { border-color: _BLUE; }
            QComboBox::drop-down { border: none; width: 24px; }
            QComboBox QAbstractItemView {
                background-color: _BASE; color: _TEXT;
                selection-background-color: _SURFACE1;
                border: 1px solid _SURFACE1; outline: none;
            }
        """.replace("_SURFACE0", _SURFACE0).replace("_SURFACE1", _SURFACE1).replace("_TEXT", _TEXT).replace("_BLUE", _BLUE).replace("_BASE", _BASE))
        for label, key in self.theme_choices:
            icon = create_theme_icon(key)
            self.theme_selector.addItem(icon, label, key)
        self.theme_selector.currentIndexChanged.connect(self._on_options_changed)
        t_layout.addWidget(self.theme_selector)

        t_layout.addWidget(self._create_separator())

        btn_cover = self._create_btn(" Configurar Portada", 'layout', _BLUE)
        btn_cover.clicked.connect(self.cover_requested.emit)
        t_layout.addWidget(btn_cover)

        btn_page = self._create_btn(" Configurar Página", 'file-text', _BLUE)
        btn_page.clicked.connect(self.page_config_requested.emit)
        t_layout.addWidget(btn_page)

        t_layout.addWidget(self._create_separator())

        # ── Group 3: FORMAT ──────────────────────────────────────────
        highlight_btn = self._create_btn(" Resaltar ⌄", 'marker', _GREEN, is_tool=True)
        highlight_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        highlight_btn.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        highlight_btn.clicked.connect(lambda: self._apply_highlight("amarillo"))
        
        highlight_menu = QMenu(self)
        highlight_menu.setStyleSheet(f"""
            QMenu {{ background-color: {_BASE}; color: {_TEXT}; border: 1px solid {_SURFACE1}; border-radius: 6px; padding: 4px; }}
            QMenu::item {{ padding: 6px 14px; border-radius: 4px; }}
            QMenu::item:selected {{ background-color: {_SURFACE1}; color: {_TEXT}; }}
            QMenu::separator {{ height: 1px; background: {_SURFACE0}; margin: 4px 8px; }}
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
        t_layout.addWidget(highlight_btn)

        btn_find = self._create_btn(" Buscar", 'search', _BLUE)
        btn_find.clicked.connect(self.show_find_panel)
        t_layout.addWidget(btn_find)

        btn_pagebreak = self._create_btn(" Salto de Página", 'pagebreak', _LAVENDER)
        btn_pagebreak.setToolTip("Insertar salto de página (<!-- PAGEBREAK -->)")
        btn_pagebreak.clicked.connect(self._insert_pagebreak)
        t_layout.addWidget(btn_pagebreak)

        # ── Expanding spacer ─────────────────────────────────────────
        t_layout.addStretch()

        # ── Exit Button ──────────────────────────────────────────────
        btn_exit = self._create_btn(" Salir", 'exit', _RED)
        btn_exit.setStyleSheet(f"""
            QPushButton {{
                background-color: #3b1e28;
                color: {_RED};
                border: 1px solid #5a2a38;
            }}
            QPushButton:hover {{
                background-color: {_RED};
                color: {_BASE};
                border-color: {_RED};
            }}
        """)
        btn_exit.clicked.connect(self.close)
        t_layout.addWidget(btn_exit)

        # Add the custom toolbar to the top of the main layout
        self.main_layout.insertWidget(0, self.toolbar)

    def _init_status_bar(self):
        """Enriched status bar matching the Visily design."""
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.status_save = QLabel("● Guardado")
        self.status_save.setObjectName("status_save")
        self.status.addWidget(self.status_save)

        self.status_mode = QLabel("</> ")
        self.status_mode.setObjectName("status_mode")
        self.status.addWidget(self.status_mode)

        self.status_cursor = QLabel("Ln 1, Col 1")
        self.status_cursor.setObjectName("status_cursor")
        self.status.addWidget(self.status_cursor)

        self.status_words = QLabel("T 0 palabras")
        self.status_words.setObjectName("status_words")
        self.status.addWidget(self.status_words)

        self.status_encoding = QLabel("UTF-8")
        self.status_encoding.setObjectName("status_encoding")
        self.status.addPermanentWidget(self.status_encoding)

        self.status_filetype = QLabel("Markdown")
        self.status_filetype.setObjectName("status_filetype")
        self.status.addPermanentWidget(self.status_filetype)

        self.status.showMessage("Listo")

    def _update_cursor_info(self):
        """Update status bar with cursor position and word count."""
        cursor = self.editor.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        self.status_cursor.setText(f"Ln {line}, Col {col}")

        text = self.editor.toPlainText()
        words = len(text.split()) if text.strip() else 0
        self.status_words.setText(f"T {words:,} palabras")

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

    def _create_highlight_handler(self, color_name: str):
        return lambda: self._apply_highlight(color_name)

    def _apply_highlight(self, color_name_or_hex: str):
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

    _MOD = 'Meta' if platform.system() == 'Darwin' else 'Ctrl'
    KEY_BINDINGS = {
        'find': f'{_MOD}+F', 'bold': f'{_MOD}+B', 'italic': f'{_MOD}+I',
        'link': f'{_MOD}+K', 'highlight': f'{_MOD}+Shift+H', 'save': f'{_MOD}+S',
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

    def _insert_pagebreak(self):
        """Inserta un salto de página en la posición actual del cursor."""
        cursor = self.editor.textCursor()
        cursor.insertText('\n\n<!-- PAGEBREAK -->\n\n')
        self.editor.setTextCursor(cursor)
        self.editor.setFocus()

    def _save_document(self):
        self.save_requested.emit()

    def show_find_panel(self):
        if hasattr(self, 'find_dock'):
            self.find_dock.show(); self.find_input.setFocus(); return

        self.find_dock = QDockWidget('Buscar y reemplazar', self)
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        self.find_input = QLineEdit()
        self.find_input.setPlaceholderText('Buscar…')
        self.replace_input = QLineEdit()
        self.replace_input.setPlaceholderText('Reemplazar por…')

        buttons = QHBoxLayout()
        buttons.setSpacing(4)
        for text, fn in [('◀', lambda: self._find(False)), ('▶', lambda: self._find(True)), ('Reemplazar', self._replace_one), ('Todo', self._replace_all)]:
            button = QPushButton(text)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(fn)
            buttons.addWidget(button)

        layout.addWidget(self.find_input)
        layout.addWidget(self.replace_input)
        layout.addLayout(buttons)

        self.find_dock.setWidget(panel)
        self.addDockWidget(Qt.DockWidgetArea.TopDockWidgetArea, self.find_dock)
        self.find_input.returnPressed.connect(lambda: self._find(True))
        self.find_input.setFocus()

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

    def _choose_custom_highlight(self):
        color = QColorDialog.getColor(QColor("#fff3b0"), self, "Seleccionar Color Pastel")
        if color.isValid():
            hex_color = color.name()
            self._apply_highlight(hex_color)

    def _on_text_changed(self):
        self.text_changed.emit(self.editor.toPlainText())
        self._update_cursor_info()
        
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
