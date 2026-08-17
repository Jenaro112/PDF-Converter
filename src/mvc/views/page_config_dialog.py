from typing import Optional, Dict
import json
from pathlib import Path
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QFrame,
    QScrollArea, QWidget, QComboBox, QFileDialog
)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPixmap

_CRUST = "#11111b"
_MANTLE = "#181825"
_BASE = "#1e1e2e"
_SURFACE0 = "#313244"
_TEXT = "#cdd6f4"
_SUBTEXT0 = "#a6adc8"
_BLUE = "#89b4fa"
_RED = "#f38ba8"

class CustomTitleBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_dialog = parent
        self.setFixedHeight(70)
        self.setStyleSheet("background-color: transparent; border: none;")
        self._start_pos = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(15)

        icon_label = QLabel()
        svg = f'''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{_BLUE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>'''
        pixmap = QPixmap()
        pixmap.loadFromData(svg.encode('utf-8'))
        icon_label.setPixmap(pixmap)
        
        text_layout = QVBoxLayout()
        text_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        text_layout.setSpacing(2)
        
        title_label = QLabel("Configuración de Página")
        title_label.setStyleSheet(f"color: {_TEXT}; font-size: 14pt; font-weight: bold;")
        subtitle_label = QLabel("Personaliza encabezados, pies de página y numeración")
        subtitle_label.setStyleSheet(f"color: {_SUBTEXT0}; font-size: 9pt;")
        
        text_layout.addWidget(title_label)
        text_layout.addWidget(subtitle_label)

        self.close_btn = QPushButton("✕")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.setStyleSheet(f"""
            QPushButton {{ background-color: transparent; color: {_SUBTEXT0}; border: none; font-size: 14pt; font-weight: bold; border-radius: 15px; }}
            QPushButton:hover {{ background-color: {_RED}; color: {_CRUST}; }}
        """)
        self.close_btn.clicked.connect(self.parent_dialog.reject)

        layout.addWidget(icon_label)
        layout.addLayout(text_layout)
        layout.addStretch()
        layout.addWidget(self.close_btn)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._start_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self._start_pos is not None:
            delta = event.globalPosition().toPoint() - self._start_pos
            self.parent_dialog.move(self.parent_dialog.pos() + delta)
            self._start_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self._start_pos = None


class ToggleSwitch(QCheckBox):
    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"""
            QCheckBox {{ color: {_TEXT}; font-size: 10pt; font-weight: 500; spacing: 10px; }}
            QCheckBox::indicator {{ width: 44px; height: 24px; border-radius: 12px; }}
            QCheckBox::indicator:unchecked {{ background-color: {_SURFACE0}; border: 1px solid {_SUBTEXT0}; }}
            QCheckBox::indicator:checked {{ background-color: {_BLUE}; border: 1px solid {_TEXT}; }}
        """)


class PageConfigDialog(QDialog):
    def __init__(self, parent=None, initial_data: Optional[Dict] = None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(750, 700)
        self.setModal(True)
        
        self.setStyleSheet(f"""
            QLabel {{ color: {_SUBTEXT0}; font-size: 9.5pt; font-weight: 500; border: none; }}
            QLineEdit {{ background-color: {_CRUST}; color: {_TEXT}; border: 1px solid {_SURFACE0}; border-radius: 6px; padding: 8px 12px; font-size: 9.5pt; }}
            QLineEdit:focus {{ border: 1px solid {_BLUE}; background-color: {_CRUST}; }}
            QComboBox {{ background-color: {_CRUST}; color: {_TEXT}; border: 1px solid {_SURFACE0}; border-radius: 6px; padding: 6px 10px; font-size: 9.5pt; }}
            QComboBox:hover {{ border-color: {_BLUE}; }}
            QComboBox::drop-down {{ border: none; width: 20px; }}
            QComboBox QAbstractItemView {{ background-color: {_BASE}; color: {_TEXT}; selection-background-color: {_BLUE}; selection-color: {_CRUST}; border: 1px solid {_SURFACE0}; }}
            QScrollBar:vertical {{ background-color: transparent; width: 8px; border: none; }}
            QScrollBar::handle:vertical {{ background-color: {_SURFACE0}; border-radius: 4px; min-height: 30px; }}
            QScrollBar::handle:vertical:hover {{ background-color: {_SUBTEXT0}; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
        """)
        self._init_ui()
        if initial_data: self.set_page_config(initial_data)

    def _get_svg_header(self, path_d: str) -> QLabel:
        lbl = QLabel()
        svg = f'''<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{_BLUE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{path_d}</svg>'''
        pixmap = QPixmap()
        pixmap.loadFromData(svg.encode('utf-8'))
        lbl.setPixmap(pixmap)
        lbl.setStyleSheet("border: none; background: transparent;")
        return lbl

    def _create_block(self, title: str, svg_path_d: str) -> tuple[QFrame, QVBoxLayout]:
        block = QFrame()
        block.setStyleSheet(f"QFrame {{ background-color: {_MANTLE}; border: 1px solid {_SURFACE0}; border-radius: 8px; }}")
        
        layout = QVBoxLayout(block)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)
        header_layout.addWidget(self._get_svg_header(svg_path_d))
        
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"font-size: 11pt; font-weight: bold; color: {_TEXT}; border: none; background: transparent;")
        header_layout.addWidget(title_lbl)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        return block, layout

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.main_container = QFrame(self)
        self.main_container.setObjectName("MainContainer")
        self.main_container.setStyleSheet(f"#MainContainer {{ background-color: {_CRUST}; border-radius: 12px; border: 1px solid {_SURFACE0}; }}")
        
        container_layout = QVBoxLayout(self.main_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        self.title_bar = CustomTitleBar(self)
        container_layout.addWidget(self.title_bar)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(scroll_content)
        content_layout.setSpacing(16)
        content_layout.setContentsMargins(20, 10, 20, 20)

        # Templates Block
        tpl_block, tpl_layout = self._create_block("PLANTILLAS GUARDADAS", '<path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>')
        tpl_row = QHBoxLayout()
        self.template_selector = QComboBox()
        self.template_selector.addItem("Seleccionar plantilla…", None)
        self._load_templates_into_selector()
        
        btn_style = f"QPushButton {{ background-color: {_SURFACE0}; color: {_TEXT}; border: 1px solid {_BASE}; border-radius: 6px; padding: 6px 12px; font-weight: 500; }} QPushButton:hover {{ background-color: {_BLUE}; color: {_CRUST}; border-color: {_BLUE}; }}"
        
        btn_apply = QPushButton("Aplicar")
        btn_apply.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_apply.setStyleSheet(btn_style)
        btn_apply.clicked.connect(self._apply_template)
        
        btn_delete = QPushButton("Eliminar")
        btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_delete.setStyleSheet(f"QPushButton {{ background-color: {_SURFACE0}; color: {_RED}; border: 1px solid {_BASE}; border-radius: 6px; padding: 6px 12px; font-weight: 500; }} QPushButton:hover {{ background-color: {_RED}; color: {_CRUST}; }}")
        btn_delete.clicked.connect(self._delete_template)
        
        btn_save = QPushButton("Guardar actual")
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.setStyleSheet(btn_style)
        btn_save.clicked.connect(self._save_template)

        tpl_row.addWidget(self.template_selector, 1)
        tpl_row.addWidget(btn_apply)
        tpl_row.addWidget(btn_delete)
        tpl_row.addWidget(btn_save)
        tpl_layout.addLayout(tpl_row)
        content_layout.addWidget(tpl_block)

        # Numeracion
        num_block, num_layout = self._create_block("NUMERACIÓN", '<circle cx="12" cy="12" r="10"></circle><path d="M12 8v8"></path><path d="M8 12h8"></path>')
        lbl_num = QLabel("Estilo de Numeración:")
        self.combo_num = QComboBox()
        self.combo_num.addItems(["Ninguno", "1", "- 1 -", "Página 1 de N"])
        num_layout.addWidget(lbl_num)
        num_layout.addWidget(self.combo_num)
        content_layout.addWidget(num_block)

        # Encabezado
        enc_block, enc_layout = self._create_block("ENCABEZADO", '<path d="M4 6h16"></path><path d="M4 12h16"></path><path d="M4 18h7"></path>')
        
        lbl_enc_l = QLabel("Izquierda:")
        self.inp_enc_l = QLineEdit()
        self.inp_enc_l.setPlaceholderText("Ej: {{page}} o Texto libre...")
        
        lbl_enc_c = QLabel("Centro:")
        self.inp_enc_c = QLineEdit()
        
        lbl_enc_r = QLabel("Derecha:")
        self.inp_enc_r = QLineEdit()
        
        enc_layout.addWidget(lbl_enc_l)
        enc_layout.addWidget(self.inp_enc_l)
        enc_layout.addWidget(lbl_enc_c)
        enc_layout.addWidget(self.inp_enc_c)
        enc_layout.addWidget(lbl_enc_r)
        enc_layout.addWidget(self.inp_enc_r)
        
        self.toggle_logo = ToggleSwitch("Incluir logo en el encabezado (Izquierda)")
        enc_layout.addWidget(self.toggle_logo)
        
        logo_row = QHBoxLayout()
        self.inp_logo_path = QLineEdit()
        self.inp_logo_path.setPlaceholderText("Ruta de la imagen...")
        self.inp_logo_path.setReadOnly(True)
        btn_browse = QPushButton("Examinar")
        btn_browse.setStyleSheet(btn_style)
        btn_browse.clicked.connect(self._browse_logo)
        logo_row.addWidget(self.inp_logo_path)
        logo_row.addWidget(btn_browse)
        enc_layout.addLayout(logo_row)

        content_layout.addWidget(enc_block)

        # Pie de Pagina
        pie_block, pie_layout = self._create_block("PIE DE PÁGINA", '<path d="M19 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2z"></path><path d="M3 15h18"></path>')
        
        lbl_pie_l = QLabel("Izquierda:")
        self.inp_pie_l = QLineEdit()
        
        lbl_pie_c = QLabel("Centro:")
        self.inp_pie_c = QLineEdit()
        
        lbl_pie_r = QLabel("Derecha:")
        self.inp_pie_r = QLineEdit()
        
        pie_layout.addWidget(lbl_pie_l)
        pie_layout.addWidget(self.inp_pie_l)
        pie_layout.addWidget(lbl_pie_c)
        pie_layout.addWidget(self.inp_pie_c)
        pie_layout.addWidget(lbl_pie_r)
        pie_layout.addWidget(self.inp_pie_r)

        content_layout.addWidget(pie_block)

        scroll.setWidget(scroll_content)
        container_layout.addWidget(scroll)

        # Bottom Buttons
        bottom_panel = QFrame()
        bottom_panel.setStyleSheet(f"background-color: {_MANTLE}; border-top: 1px solid {_SURFACE0}; border-bottom-left-radius: 12px; border-bottom-right-radius: 12px;")
        bottom_layout = QHBoxLayout(bottom_panel)
        bottom_layout.setContentsMargins(20, 15, 20, 15)

        btn_clear = QPushButton("🗑 Limpiar")
        btn_clear.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_clear.setStyleSheet(f"QPushButton {{ background-color: {_SURFACE0}; color: {_RED}; border: 1px solid {_RED}; border-radius: 6px; padding: 8px 16px; font-weight: bold; }} QPushButton:hover {{ background-color: {_RED}; color: {_CRUST}; }}")
        btn_clear.clicked.connect(self._clear)
        
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancel.setStyleSheet(f"QPushButton {{ background-color: transparent; color: {_SUBTEXT0}; border: 1px solid {_SURFACE0}; border-radius: 6px; padding: 8px 16px; font-weight: bold; }} QPushButton:hover {{ background-color: {_SURFACE0}; color: {_TEXT}; }}")
        btn_cancel.clicked.connect(self.reject)
        
        btn_save_config = QPushButton("💾 Guardar Configuración")
        btn_save_config.setDefault(True)
        btn_save_config.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save_config.setStyleSheet(f"QPushButton {{ background-color: {_BLUE}; color: {_CRUST}; border: 1px solid {_BLUE}; border-radius: 6px; padding: 8px 24px; font-weight: bold; }} QPushButton:hover {{ background-color: #74a0ea; }}")
        btn_save_config.clicked.connect(self.accept)

        bottom_layout.addWidget(btn_clear)
        bottom_layout.addStretch()
        bottom_layout.addWidget(btn_cancel)
        bottom_layout.addWidget(btn_save_config)

        container_layout.addWidget(bottom_panel)
        main_layout.addWidget(self.main_container)

    @property
    def _templates_path(self) -> Path: return Path.home() / '.pdf_converter_page_templates.json'

    def _read_templates(self):
        try: return json.loads(self._templates_path.read_text(encoding='utf-8'))
        except (OSError, json.JSONDecodeError): return {}

    def _write_templates(self, templates):
        self._templates_path.write_text(json.dumps(templates, ensure_ascii=False, indent=2), encoding='utf-8')

    def _load_templates_into_selector(self):
        for name in self._read_templates(): self.template_selector.addItem(name, name)

    def _save_template(self):
        from PySide6.QtWidgets import QInputDialog
        name, ok = QInputDialog.getText(self, 'Guardar plantilla', 'Nombre de la plantilla:')
        if not ok or not name.strip(): return
        templates = self._read_templates()
        templates[name.strip()] = self.get_page_config()
        self._write_templates(templates)
        self.template_selector.clear()
        self.template_selector.addItem('Seleccionar plantilla…', None)
        self._load_templates_into_selector()

    def _apply_template(self):
        name = self.template_selector.currentData()
        if name and name in self._read_templates(): self.set_page_config(self._read_templates()[name])

    def _delete_template(self):
        name = self.template_selector.currentData()
        if not name: return
        templates = self._read_templates()
        templates.pop(name, None)
        self._write_templates(templates)
        self.template_selector.clear()
        self.template_selector.addItem('Seleccionar plantilla…', None)
        self._load_templates_into_selector()

    def _browse_logo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Logo", "", "Imágenes (*.png *.jpg *.jpeg *.svg)")
        if file_path:
            self.inp_logo_path.setText(file_path)

    def _clear(self):
        self.combo_num.setCurrentIndex(0)
        self.inp_enc_l.clear()
        self.inp_enc_c.clear()
        self.inp_enc_r.clear()
        self.inp_pie_l.clear()
        self.inp_pie_c.clear()
        self.inp_pie_r.clear()
        self.toggle_logo.setChecked(False)
        self.inp_logo_path.clear()

    def get_page_config(self) -> Dict:
        # Resolve logo file path to URI for proper HTML loading
        logo_path = self.inp_logo_path.text().strip()
        if logo_path:
            logo_path = Path(logo_path).as_uri()
            
        return {
            'numbering': self.combo_num.currentText(),
            'header_left': self.inp_enc_l.text().strip(),
            'header_center': self.inp_enc_c.text().strip(),
            'header_right': self.inp_enc_r.text().strip(),
            'footer_left': self.inp_pie_l.text().strip(),
            'footer_center': self.inp_pie_c.text().strip(),
            'footer_right': self.inp_pie_r.text().strip(),
            'include_logo': self.toggle_logo.isChecked(),
            'logo_path': logo_path
        }

    def set_page_config(self, data: Dict):
        num = data.get('numbering', 'Ninguno')
        idx = self.combo_num.findText(num)
        if idx >= 0: self.combo_num.setCurrentIndex(idx)
        
        self.inp_enc_l.setText(data.get('header_left', ''))
        self.inp_enc_c.setText(data.get('header_center', ''))
        self.inp_enc_r.setText(data.get('header_right', ''))
        
        self.inp_pie_l.setText(data.get('footer_left', ''))
        self.inp_pie_c.setText(data.get('footer_center', ''))
        self.inp_pie_r.setText(data.get('footer_right', ''))
        
        self.toggle_logo.setChecked(data.get('include_logo', False))
        
        # Convert URI back to local path if possible
        logo_path = data.get('logo_path', '')
        if logo_path and logo_path.startswith('file://'):
            from urllib.request import url2pathname
            logo_path = url2pathname(logo_path[7:])
        self.inp_logo_path.setText(logo_path)
