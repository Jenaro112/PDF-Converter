from typing import Optional, List, Dict
import json
from pathlib import Path
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QCheckBox, QFrame,
    QScrollArea, QWidget, QGridLayout, QGraphicsOpacityEffect, QComboBox
)
from PySide6.QtCore import Qt, Signal, QPoint
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
        svg = f'''<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{_BLUE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>'''
        pixmap = QPixmap()
        pixmap.loadFromData(svg.encode('utf-8'))
        icon_label.setPixmap(pixmap)
        
        text_layout = QVBoxLayout()
        text_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        text_layout.setSpacing(2)
        
        title_label = QLabel("Configurar Portada del Documento")
        title_label.setStyleSheet(f"color: {_TEXT}; font-size: 14pt; font-weight: bold;")
        subtitle_label = QLabel("Personaliza el aspecto visual de la primera página de tu proyecto")
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


class LogoPositionDiagram(QFrame):
    position_changed = Signal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_position = "top-left"
        self.setFixedSize(140, 100)
        self.setStyleSheet(f"LogoPositionDiagram {{ background-color: {_SURFACE0}; border: 2px solid {_BASE}; border-radius: 8px; }}")
        self._init_buttons()

    def _init_buttons(self):
        layout = QGridLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        self.buttons = {}
        for pos_key, label, row, col in [("top-left", "↖", 0, 0), ("top-right", "↗", 0, 1), ("bottom-left", "↙", 1, 0), ("bottom-right", "↘", 1, 1)]:
            btn = QPushButton(label)
            btn.setFixedSize(36, 36)
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, pk=pos_key: self.set_position(pk))
            layout.addWidget(btn, row, col, alignment=Qt.AlignmentFlag.AlignCenter)
            self.buttons[pos_key] = btn
        self._update_styles()

    def set_position(self, pos_key: str):
        if pos_key in self.buttons:
            self.current_position = pos_key
            self._update_styles()
            self.position_changed.emit(pos_key)

    def _update_styles(self):
        for pk, btn in self.buttons.items():
            if pk == self.current_position:
                btn.setChecked(True)
                btn.setStyleSheet(f"QPushButton {{ background-color: {_BLUE}; color: {_CRUST}; border: 2px solid {_TEXT}; border-radius: 6px; font-weight: bold; font-size: 11pt; }}")
            else:
                btn.setChecked(False)
                btn.setStyleSheet(f"QPushButton {{ background-color: {_BASE}; color: {_SUBTEXT0}; border: 1px solid {_SURFACE0}; border-radius: 6px; font-size: 11pt; }} QPushButton:hover {{ background-color: {_SURFACE0}; color: {_TEXT}; border-color: {_BLUE}; }}")


class ChipItem(QFrame):
    removed = Signal(str)
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.text = text
        self.setStyleSheet(f"""
            ChipItem {{ background-color: {_SURFACE0}; border: 1px solid {_BASE}; border-radius: 14px; padding: 2px 8px; }}
            QLabel {{ color: {_TEXT}; font-size: 9pt; font-weight: 500; border: none; }}
            QPushButton {{ background-color: transparent; color: {_SUBTEXT0}; border: none; font-weight: bold; font-size: 10pt; padding: 0 4px; }}
            QPushButton:hover {{ color: {_RED}; }}
        """)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 2, 6, 2)
        layout.setSpacing(4)
        label = QLabel(text)
        btn_close = QPushButton("✕")
        btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_close.clicked.connect(lambda: self.removed.emit(self.text))
        layout.addWidget(label)
        layout.addWidget(btn_close)

class ChipListWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.items: List[str] = []
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(6)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

    def add_item(self, text: str):
        text = text.strip()
        if text and text not in self.items:
            self.items.append(text)
            chip = ChipItem(text)
            chip.removed.connect(self.remove_item)
            self.layout.addWidget(chip)

    def remove_item(self, text: str):
        if text in self.items:
            self.items.remove(text)
            for i in range(self.layout.count()):
                child = self.layout.itemAt(i).widget()
                if isinstance(child, ChipItem) and child.text == text:
                    child.deleteLater()
                    break

    def clear(self):
        self.items.clear()
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def get_items(self) -> List[str]: return list(self.items)
    def set_items(self, items: List[str]):
        self.clear()
        for item in items: self.add_item(item)


class LayoutCard(QFrame):
    selected = Signal(str)
    def __init__(self, style_key: str, title: str, description: str, parent=None):
        super().__init__(parent)
        self.style_key = style_key
        self.is_active = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(110)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        self.thumbnail = QLabel()
        self.thumbnail.setFixedHeight(45)
        self.thumbnail.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thumbnail.setStyleSheet("border: none; background: transparent;")
        self._render_thumbnail(style_key)

        lbl_title = QLabel(title)
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_title.setStyleSheet(f"font-weight: bold; font-size: 8.5pt; color: {_TEXT}; border: none; background: transparent;")

        layout.addWidget(self.thumbnail)
        layout.addWidget(lbl_title)
        self._update_style()

    def _render_thumbnail(self, key: str):
        art = {
            'sidebar_logo': f'<rect width="15" height="40" fill="{_BLUE}"/><circle cx="7.5" cy="20" r="4" fill="{_CRUST}"/><rect x="25" y="15" width="25" height="4" fill="{_TEXT}"/><rect x="30" y="22" width="15" height="2" fill="{_SUBTEXT0}"/>',
            'academica_clasica': f'<rect x="5" y="5" width="50" height="30" fill="none" stroke="{_SURFACE0}"/><rect x="25" y="8" width="10" height="4" fill="{_SUBTEXT0}"/><rect x="15" y="18" width="30" height="4" fill="{_TEXT}"/><rect x="20" y="28" width="20" height="2" fill="{_SUBTEXT0}"/>',
            'corporativa': f'<rect x="10" y="10" width="3" height="20" fill="{_BLUE}"/><rect x="15" y="15" width="30" height="4" fill="{_TEXT}"/><rect x="15" y="25" width="20" height="2" fill="{_SUBTEXT0}"/>',
            'bloque_color': f'<rect width="60" height="15" fill="{_SURFACE0}"/><rect x="10" y="5" width="8" height="4" fill="{_TEXT}"/><rect x="10" y="20" width="30" height="4" fill="{_TEXT}"/><rect x="10" y="30" width="20" height="2" fill="{_SUBTEXT0}"/>',
            'marco_fino': f'<rect x="2" y="2" width="56" height="36" fill="none" stroke="{_SUBTEXT0}"/><rect x="25" y="8" width="10" height="4" fill="{_SUBTEXT0}"/><rect x="15" y="18" width="30" height="3" fill="{_TEXT}"/><rect x="20" y="30" width="20" height="2" fill="{_SUBTEXT0}"/>',
        }.get(key, f'<rect width="60" height="40" fill="{_SURFACE0}"/><rect x="7" y="8" width="3" height="24" fill="{_BLUE}"/>')
        
        svg_icon = f'''<svg width="60" height="40" viewBox="0 0 60 40">{art}</svg>'''
        pixmap = QPixmap()
        pixmap.loadFromData(svg_icon.encode('utf-8'))
        self.thumbnail.setPixmap(pixmap)

    def set_active(self, active: bool):
        self.is_active = active
        self._update_style()

    def _update_style(self):
        if self.is_active:
            self.setStyleSheet(f"LayoutCard {{ background-color: {_SURFACE0}; border: 2px solid {_BLUE}; border-radius: 8px; }}")
        else:
            self.setStyleSheet(f"LayoutCard {{ background-color: {_MANTLE}; border: 1px solid {_SURFACE0}; border-radius: 8px; }} LayoutCard:hover {{ background-color: {_SURFACE0}; border-color: {_BLUE}; }}")

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.selected.emit(self.style_key)


class CoverDialog(QDialog):
    def __init__(self, parent=None, initial_data: Optional[Dict] = None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(850, 780)
        self.setModal(True)
        self.selected_style = "sidebar_logo"
        self.logo_position = "top-left"
        
        # We handle general typography via inherited 'Inter'.
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
        if initial_data: self.set_cover_data(initial_data)

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

        # Main Container
        self.main_container = QFrame(self)
        self.main_container.setObjectName("MainContainer")
        self.main_container.setStyleSheet(f"#MainContainer {{ background-color: {_CRUST}; border-radius: 12px; border: 1px solid {_SURFACE0}; }}")
        
        container_layout = QVBoxLayout(self.main_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        # Custom TitleBar
        self.title_bar = CustomTitleBar(self)
        container_layout.addWidget(self.title_bar)

        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(scroll_content)
        content_layout.setSpacing(16)
        content_layout.setContentsMargins(20, 10, 20, 20)

        # Block: Estilo de Portada
        style_block, style_layout = self._create_block("ESTILO DE PORTADA", 'M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z')
        grid_styles = QGridLayout()
        grid_styles.setSpacing(12)
        self.style_cards = {}
        styles_info = [
            ("sidebar_logo", "Banda Izquierda", "Barra gruesa con logo"),
            ("academica_clasica", "Académica Clásica", "Estilo tesis tradicional"),
            ("corporativa", "Corporativa", "Moderna, limpia, izq"),
            ("bloque_color", "Bloque Superior", "Cabecera destacada"),
            ("marco_fino", "Elegancia", "Marco minimalista"),
        ]
        for i, (s_key, s_title, s_desc) in enumerate(styles_info):
            card = LayoutCard(s_key, s_title, s_desc)
            card.selected.connect(self._on_style_selected)
            grid_styles.addWidget(card, divmod(i, 3)[0], divmod(i, 3)[1])
            self.style_cards[s_key] = card
        style_layout.addLayout(grid_styles)
        content_layout.addWidget(style_block)

        # Block: Plantillas Guardadas
        tpl_block, tpl_layout = self._create_block("PLANTILLAS GUARDADAS", 'M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z')
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

        # ROW 1: INFO PRINCIPAL & LOGO
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(16)
        
        info_block, info_layout = self._create_block("INFORMACIÓN PRINCIPAL", 'M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z')
        lbl1 = QLabel("Título del Documento *:")
        lbl1.setStyleSheet("background: transparent;")
        info_layout.addWidget(lbl1)
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Ej: Trabajo Práctico Nº 2")
        info_layout.addWidget(self.title_input)
        
        lbl2 = QLabel("Subtítulo (opcional):")
        lbl2.setStyleSheet("background: transparent;")
        info_layout.addWidget(lbl2)
        self.subtitle_input = QLineEdit()
        self.subtitle_input.setPlaceholderText("Ej: Gestión de Memoria")
        info_layout.addWidget(self.subtitle_input)
        
        lbl3 = QLabel("Materia / Asignatura (opcional):")
        lbl3.setStyleSheet("background: transparent;")
        info_layout.addWidget(lbl3)
        self.materia_input = QLineEdit()
        self.materia_input.setPlaceholderText("Ej: Sistemas Operativos")
        info_layout.addWidget(self.materia_input)
        # Mover el Toggle del Logo dentro de Información Principal
        self.toggle_logo = ToggleSwitch("Incluir logo de la facultad")
        self.toggle_logo.setStyleSheet(self.toggle_logo.styleSheet() + " background: transparent; margin-top: 8px;")
        self.toggle_logo.toggled.connect(self._on_logo_toggled)
        info_layout.addWidget(self.toggle_logo)
        
        info_layout.addStretch()

        row1_layout.addWidget(info_block, 1)
        content_layout.addLayout(row1_layout)

        # ROW 2: INTEGRANTES & PROFESORES
        row2_layout = QHBoxLayout()
        row2_layout.setSpacing(16)
        
        int_block, int_layout = self._create_block("INTEGRANTES", 'M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2M9 7a4 4 0 1 0 0-8 4 4 0 0 0 0 8z M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75')
        add_int_h = QHBoxLayout()
        self.int_input = QLineEdit()
        self.int_input.setPlaceholderText("Nombre y Enter...")
        self.int_input.returnPressed.connect(self._add_integrante)
        btn_add_int = QPushButton("+ Agregar")
        btn_add_int.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add_int.setStyleSheet(f"QPushButton {{ background-color: {_SURFACE0}; color: {_BLUE}; border: 1px solid {_BLUE}; border-radius: 6px; padding: 7px 14px; font-weight: bold; }} QPushButton:hover {{ background-color: {_BLUE}; color: {_CRUST}; }}")
        btn_add_int.clicked.connect(self._add_integrante)
        add_int_h.addWidget(self.int_input)
        add_int_h.addWidget(btn_add_int)
        int_layout.addLayout(add_int_h)
        self.int_chips = ChipListWidget()
        self.int_chips.setStyleSheet("background: transparent;")
        int_layout.addWidget(self.int_chips)
        int_layout.addStretch()
        
        prof_block, prof_layout = self._create_block("PROFESORES", 'M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z')
        add_prof_h = QHBoxLayout()
        self.prof_input = QLineEdit()
        self.prof_input.setPlaceholderText("Profesor y Enter...")
        self.prof_input.returnPressed.connect(self._add_profesor)
        btn_add_prof = QPushButton("+ Agregar")
        btn_add_prof.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add_prof.setStyleSheet(f"QPushButton {{ background-color: {_SURFACE0}; color: {_BLUE}; border: 1px solid {_BLUE}; border-radius: 6px; padding: 7px 14px; font-weight: bold; }} QPushButton:hover {{ background-color: {_BLUE}; color: {_CRUST}; }}")
        btn_add_prof.clicked.connect(self._add_profesor)
        add_prof_h.addWidget(self.prof_input)
        add_prof_h.addWidget(btn_add_prof)
        prof_layout.addLayout(add_prof_h)
        self.prof_chips = ChipListWidget()
        self.prof_chips.setStyleSheet("background: transparent;")
        prof_layout.addWidget(self.prof_chips)
        prof_layout.addStretch()

        row2_layout.addWidget(int_block, 1)
        row2_layout.addWidget(prof_block, 1)
        content_layout.addLayout(row2_layout)

        scroll.setWidget(scroll_content)
        container_layout.addWidget(scroll)

        # Bottom Buttons
        bottom_panel = QFrame()
        bottom_panel.setStyleSheet(f"background-color: {_MANTLE}; border-top: 1px solid {_SURFACE0}; border-bottom-left-radius: 12px; border-bottom-right-radius: 12px;")
        bottom_layout = QHBoxLayout(bottom_panel)
        bottom_layout.setContentsMargins(20, 15, 20, 15)

        btn_clear = QPushButton("🗑 Quitar Portada")
        btn_clear.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_clear.setStyleSheet(f"QPushButton {{ background-color: {_SURFACE0}; color: {_RED}; border: 1px solid {_RED}; border-radius: 6px; padding: 8px 16px; font-weight: bold; }} QPushButton:hover {{ background-color: {_RED}; color: {_CRUST}; }}")
        btn_clear.clicked.connect(self._clear_and_close)
        
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancel.setStyleSheet(f"QPushButton {{ background-color: transparent; color: {_SUBTEXT0}; border: 1px solid {_SURFACE0}; border-radius: 6px; padding: 8px 16px; font-weight: bold; }} QPushButton:hover {{ background-color: {_SURFACE0}; color: {_TEXT}; }}")
        btn_cancel.clicked.connect(self.reject)
        
        btn_save_portada = QPushButton("💾 Guardar Portada")
        btn_save_portada.setDefault(True)
        btn_save_portada.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save_portada.setStyleSheet(f"QPushButton {{ background-color: {_BLUE}; color: {_CRUST}; border: 1px solid {_BLUE}; border-radius: 6px; padding: 8px 24px; font-weight: bold; }} QPushButton:hover {{ background-color: #74a0ea; }}")
        btn_save_portada.clicked.connect(self._on_save)

        bottom_layout.addWidget(btn_clear)
        bottom_layout.addStretch()
        bottom_layout.addWidget(btn_cancel)
        bottom_layout.addWidget(btn_save_portada)

        container_layout.addWidget(bottom_panel)
        main_layout.addWidget(self.main_container)

        self._on_style_selected("sidebar_logo")
        self._on_logo_toggled(False)

    def _on_style_selected(self, style_key: str):
        self.selected_style = style_key
        for key, card in self.style_cards.items():
            card.set_active(key == style_key)

    @property
    def _templates_path(self) -> Path: return Path.home() / '.pdf_converter_cover_templates.json'

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
        templates[name.strip()] = self.get_cover_data()
        self._write_templates(templates)
        self.template_selector.clear()
        self.template_selector.addItem('Seleccionar plantilla…', None)
        self._load_templates_into_selector()

    def _apply_template(self):
        name = self.template_selector.currentData()
        if name and name in self._read_templates(): self.set_cover_data(self._read_templates()[name])

    def _delete_template(self):
        name = self.template_selector.currentData()
        if not name: return
        templates = self._read_templates()
        templates.pop(name, None)
        self._write_templates(templates)
        self.template_selector.clear()
        self.template_selector.addItem('Seleccionar plantilla…', None)
        self._load_templates_into_selector()

    def _on_logo_toggled(self, checked: bool):
        pass

    def _on_logo_position_changed(self, pos_key: str):
        self.logo_position = pos_key

    def _add_integrante(self):
        text = self.int_input.text().strip()
        if text:
            self.int_chips.add_item(text)
            self.int_input.clear()

    def _add_profesor(self):
        text = self.prof_input.text().strip()
        if text:
            self.prof_chips.add_item(text)
            self.prof_input.clear()

    def _clear_and_close(self):
        self.title_input.clear()
        self.subtitle_input.clear()
        self.materia_input.clear()
        self.toggle_logo.setChecked(False)
        self.int_chips.clear()
        self.prof_chips.clear()
        self._on_style_selected("sidebar_logo")
        self.accept()

    def _on_save(self):
        title = self.title_input.text().strip()
        if not title and (len(self.int_chips.get_items()) > 0 or self.materia_input.text().strip()):
            QMessageBox.warning(self, "Título Requerido", "Por favor, ingresá al menos el Título del documento para generar la portada.")
            return
        self.accept()

    def get_cover_data(self) -> Dict:
        integrantes = self.int_chips.get_items()
        profesores = self.prof_chips.get_items()
        return {
            'show_cover': bool(self.title_input.text().strip()),
            'title': self.title_input.text().strip(),
            'subtitle': self.subtitle_input.text().strip(),
            'materia': self.materia_input.text().strip(),
            'show_logo': self.toggle_logo.isChecked(),
            'logo_position': self.logo_position,
            'cover_style': self.selected_style,
            'integrantes': ", ".join(integrantes),
            'profesores': ", ".join(profesores),
            'integrantes_list': integrantes,
            'profesores_list': profesores,
        }

    def set_cover_data(self, data: Dict):
        self.title_input.setText(data.get('title', ''))
        self.subtitle_input.setText(data.get('subtitle', ''))
        self.materia_input.setText(data.get('materia', ''))
        self.toggle_logo.setChecked(data.get('show_logo', False))
        pos = data.get('logo_position', 'top-left')
        self.logo_position = pos
        style = data.get('cover_style', 'sidebar_logo')
        if style not in self.style_cards: style = 'sidebar_logo'
        self._on_style_selected(style)
        integrantes = data.get('integrantes_list', [])
        if not integrantes and data.get('integrantes'):
            integrantes = [x.strip() for x in data.get('integrantes', '').split(',') if x.strip()]
        self.int_chips.set_items(integrantes)
        profesores = data.get('profesores_list', [])
        if not profesores and data.get('profesores'):
            profesores = [x.strip() for x in data.get('profesores', '').split(',') if x.strip()]
        self.prof_chips.set_items(profesores)