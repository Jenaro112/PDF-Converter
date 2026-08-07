from typing import Optional, List, Dict
import json
from pathlib import Path
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QGroupBox, QMessageBox, QCheckBox, QFrame,
    QScrollArea, QWidget, QGridLayout, QSizePolicy, QGraphicsOpacityEffect, QComboBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QColor, QFont, QPainter, QBrush, QPen

class ToggleSwitch(QCheckBox):
    def __init__(self, text: str = "", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QCheckBox { color: #e2e8f0; font-family: 'Inter', 'Segoe UI', system-ui, sans-serif; font-size: 10pt; font-weight: 500; spacing: 10px; }
            QCheckBox::indicator { width: 44px; height: 24px; border-radius: 12px; }
            QCheckBox::indicator:unchecked { background-color: #334155; border: 1px solid #475569; }
            QCheckBox::indicator:checked { background-color: #2563eb; border: 1px solid #3b82f6; }
        """)

class LogoPositionDiagram(QFrame):
    position_changed = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_position = "top-left"
        self.setFixedSize(140, 100)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("LogoPositionDiagram { background-color: #1e2235; border: 2px solid #3b4261; border-radius: 8px; }")
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
                btn.setStyleSheet("QPushButton { background-color: #2563eb; color: #ffffff; border: 2px solid #60a5fa; border-radius: 6px; font-weight: bold; font-size: 11pt; }")
            else:
                btn.setChecked(False)
                btn.setStyleSheet("QPushButton { background-color: #0f111a; color: #94a3b8; border: 1px solid #3b4261; border-radius: 6px; font-size: 11pt; } QPushButton:hover { background-color: #282e4a; color: #e2e8f0; border-color: #60a5fa; }")

class ChipItem(QFrame):
    removed = pyqtSignal(str)
    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.text = text
        self.setStyleSheet("""
            ChipItem { background-color: #282e4a; border: 1px solid #3b4266; border-radius: 14px; padding: 2px 8px; }
            QLabel { color: #e2e8f0; font-family: 'Inter', 'Segoe UI', system-ui, sans-serif; font-size: 9pt; font-weight: 500; }
            QPushButton { background-color: transparent; color: #94a3b8; border: none; font-weight: bold; font-size: 10pt; padding: 0 4px; }
            QPushButton:hover { color: #ef4444; }
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
    selected = pyqtSignal(str)
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
        self._render_thumbnail(style_key)

        lbl_title = QLabel(title)
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_title.setStyleSheet("font-weight: bold; font-size: 8.5pt; color: #e2e8f0;")

        layout.addWidget(self.thumbnail)
        layout.addWidget(lbl_title)
        self._update_style()

    def _render_thumbnail(self, key: str):
        # Nuevas miniaturas adaptadas a los estilos sobrios/académicos solicitados
        art = {
            'sidebar_logo': '<rect width="15" height="40" fill="#1a4f76"/><circle cx="7.5" cy="20" r="4" fill="#ffffff"/><rect x="25" y="15" width="25" height="4" fill="#333"/><rect x="30" y="22" width="15" height="2" fill="#666"/>',
            'academica_clasica': '<rect x="5" y="5" width="50" height="30" fill="none" stroke="#333"/><rect x="25" y="8" width="10" height="4" fill="#666"/><rect x="15" y="18" width="30" height="4" fill="#111"/><rect x="20" y="28" width="20" height="2" fill="#666"/>',
            'corporativa': '<rect x="10" y="10" width="3" height="20" fill="#2563eb"/><rect x="15" y="15" width="30" height="4" fill="#111"/><rect x="15" y="25" width="20" height="2" fill="#666"/>',
            'bloque_color': '<rect width="60" height="15" fill="#1e293b"/><rect x="10" y="5" width="8" height="4" fill="#fff"/><rect x="10" y="20" width="30" height="4" fill="#111"/><rect x="10" y="30" width="20" height="2" fill="#666"/>',
            'marco_fino': '<rect x="2" y="2" width="56" height="36" fill="none" stroke="#9ca3af"/><rect x="25" y="8" width="10" height="4" fill="#666"/><rect x="15" y="18" width="30" height="3" fill="#111"/><rect x="20" y="30" width="20" height="2" fill="#666"/>',
        }.get(key, '<rect width="60" height="40" fill="#f7f7f5"/><rect x="7" y="8" width="3" height="24" fill="#4f7f79"/>')
        
        svg_icon = f'''<svg width="60" height="40" viewBox="0 0 60 40">{art}</svg>'''
            
        from PyQt6.QtGui import QPixmap
        pixmap = QPixmap()
        pixmap.loadFromData(svg_icon.encode('utf-8'))
        self.thumbnail.setPixmap(pixmap)

    def set_active(self, active: bool):
        self.is_active = active
        self._update_style()

    def _update_style(self):
        if self.is_active:
            self.setStyleSheet("LayoutCard { background-color: #1e293b; border: 2px solid #3b82f6; border-radius: 8px; }")
        else:
            self.setStyleSheet("LayoutCard { background-color: #161927; border: 1px solid #2a2e45; border-radius: 8px; } LayoutCard:hover { background-color: #1e2235; border-color: #3b82f6; }")

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.selected.emit(self.style_key)

class CoverDialog(QDialog):
    def __init__(self, parent=None, initial_data: Optional[Dict] = None):
        super().__init__(parent)
        self.setWindowTitle("📖 Configurar Portada del Documento")
        self.resize(620, 720)
        self.setModal(True)
        self.selected_style = "sidebar_logo"
        self.logo_position = "top-left"
        self.setStyleSheet("""
            QDialog { background-color: #0f111a; color: #e2e8f0; font-family: 'Inter', 'Segoe UI', system-ui, sans-serif; }
            QLabel { color: #94a3b8; font-family: 'Inter', 'Segoe UI', system-ui, sans-serif; font-size: 9.5pt; font-weight: 500; }
            QLineEdit { background-color: #161927; color: #f8fafc; border: 1px solid #2a2e45; border-radius: 6px; padding: 8px 12px; font-family: 'Inter', 'Segoe UI', system-ui, sans-serif; font-size: 9.5pt; }
            QLineEdit:focus { border: 1px solid #3b82f6; background-color: #1a1d2e; }
            QComboBox { background-color: #161927; color: #f8fafc; border: 1px solid #2a2e45; border-radius: 6px; padding: 6px 10px; font-family: 'Inter', 'Segoe UI', system-ui, sans-serif; font-size: 9.5pt; }
            QComboBox:hover { border-color: #3b82f6; }
            QComboBox::drop-down { border: none; width: 20px; }
            QComboBox QAbstractItemView { background-color: #161927; color: #f8fafc; selection-background-color: #2563eb; border: 1px solid #3b4261; }
            QScrollBar:vertical { background-color: #0f111a; width: 8px; border: none; }
            QScrollBar::handle:vertical { background-color: #2a2e45; border-radius: 4px; min-height: 30px; }
            QScrollBar::handle:vertical:hover { background-color: #3b4261; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """)
        self._init_ui()
        if initial_data: self.set_cover_data(initial_data)

    def _create_card(self, title_with_icon: str) -> tuple[QFrame, QVBoxLayout]:
        card = QFrame()
        card.setStyleSheet("QFrame { background-color: #161927; border: 1px solid #2a2e45; border-radius: 10px; }")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(14, 12, 14, 14)
        layout.setSpacing(10)
        header = QLabel(title_with_icon)
        header.setStyleSheet("font-size: 11pt; font-weight: bold; color: #f1f5f9; border: none;")
        layout.addWidget(header)
        return card, layout

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        scroll_content = QWidget()
        content_layout = QVBoxLayout(scroll_content)
        content_layout.setSpacing(12)
        content_layout.setContentsMargins(0, 0, 4, 0)

        style_card, style_layout = self._create_card("🎨 Estilo de Portada (Académicas y Profesionales)")
        grid_styles = QGridLayout()
        grid_styles.setSpacing(8)

        self.style_cards = {}
        # Aquí insertamos las 5 nuevas portadas limpias
        styles_info = [
            ("sidebar_logo", "Banda Izquierda", "Barra gruesa con logo centrado verticalmente"),
            ("academica_clasica", "Académica Clásica", "Estilo tesis tradicional y solemne"),
            ("corporativa", "Corporativa", "Moderna, limpia, alineación izquierda"),
            ("bloque_color", "Bloque Superior", "Cabecera destacada en color oscuro"),
            ("marco_fino", "Elegancia", "Marco minimalista de página entera"),
        ]

        for i, (s_key, s_title, s_desc) in enumerate(styles_info):
            card = LayoutCard(s_key, s_title, s_desc)
            card.selected.connect(self._on_style_selected)
            row, col = divmod(i, 2)
            grid_styles.addWidget(card, row, col)
            self.style_cards[s_key] = card

        style_layout.addLayout(grid_styles)
        content_layout.addWidget(style_card)

        template_card, template_layout = self._create_card("🗂 Plantillas guardadas")
        template_row = QHBoxLayout()
        self.template_selector = QComboBox()
        self.template_selector.addItem("Seleccionar plantilla…", None)
        self._load_templates_into_selector()
        btn_apply_template = QPushButton("Aplicar")
        btn_delete_template = QPushButton("Eliminar")
        btn_save_template = QPushButton("Guardar actual")
        btn_apply_template.clicked.connect(self._apply_template)
        btn_delete_template.clicked.connect(self._delete_template)
        btn_save_template.clicked.connect(self._save_template)
        template_row.addWidget(self.template_selector, 1)
        template_row.addWidget(btn_apply_template); template_row.addWidget(btn_delete_template); template_row.addWidget(btn_save_template)
        template_layout.addLayout(template_row)
        content_layout.addWidget(template_card)

        info_card, info_layout = self._create_card("📌 Información Principal")
        info_layout.addWidget(QLabel("Título del Documento *: "))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Ej: Trabajo Práctico Nº 2 - Sistemas Operativos")
        info_layout.addWidget(self.title_input)
        info_layout.addWidget(QLabel("Subtítulo (opcional):"))
        self.subtitle_input = QLineEdit()
        self.subtitle_input.setPlaceholderText("Ej: Gestión de Memoria y Paginación")
        info_layout.addWidget(self.subtitle_input)
        info_layout.addWidget(QLabel("Materia / Asignatura (opcional):"))
        self.materia_input = QLineEdit()
        self.materia_input.setPlaceholderText("Ej: Sistemas Operativos I - Lic. en Sistemas")
        info_layout.addWidget(self.materia_input)
        content_layout.addWidget(info_card)

        logo_card, logo_layout = self._create_card("🖼 Logo de la Facultad")
        logo_h_layout = QHBoxLayout()
        logo_h_layout.setSpacing(20)
        left_logo_layout = QVBoxLayout()
        self.toggle_logo = ToggleSwitch("Incluir logo de la facultad en portada")
        self.toggle_logo.toggled.connect(self._on_logo_toggled)
        left_logo_layout.addWidget(self.toggle_logo)
        lbl_desc = QLabel("Nota: En el diseño 'Banda Izquierda', el logo siempre se centra automáticamente dentro de la barra azul de la izquierda. El selector a continuación se usa para el resto de los estilos:")
        lbl_desc.setWordWrap(True)
        lbl_desc.setStyleSheet("font-size: 8.5pt; color: #64748b;")
        left_logo_layout.addWidget(lbl_desc)
        logo_h_layout.addLayout(left_logo_layout, stretch=1)
        self.diagram = LogoPositionDiagram()
        self.diagram.position_changed.connect(self._on_logo_position_changed)
        logo_h_layout.addWidget(self.diagram, alignment=Qt.AlignmentFlag.AlignCenter)
        logo_layout.addLayout(logo_h_layout)
        content_layout.addWidget(logo_card)

        int_card, int_layout = self._create_card("👥 Integrantes / Autores")
        add_int_h = QHBoxLayout()
        self.int_input = QLineEdit()
        self.int_input.setPlaceholderText("Escribí un nombre y presioná Enter...")
        self.int_input.returnPressed.connect(self._add_integrante)
        btn_add_int = QPushButton("+ Agregar")
        btn_add_int.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add_int.setStyleSheet("QPushButton { background-color: #1e293b; color: #3b82f6; border: 1px solid #3b82f6; border-radius: 6px; padding: 7px 14px; font-weight: bold; } QPushButton:hover { background-color: #2563eb; color: #ffffff; }")
        btn_add_int.clicked.connect(self._add_integrante)
        add_int_h.addWidget(self.int_input)
        add_int_h.addWidget(btn_add_int)
        int_layout.addLayout(add_int_h)
        self.int_chips = ChipListWidget()
        int_layout.addWidget(self.int_chips)
        content_layout.addWidget(int_card)

        prof_card, prof_layout = self._create_card("👨‍🏫 Profesores / Docentes")
        add_prof_h = QHBoxLayout()
        self.prof_input = QLineEdit()
        self.prof_input.setPlaceholderText("Nombre del profesor / docente...")
        self.prof_input.returnPressed.connect(self._add_profesor)
        btn_add_prof = QPushButton("+ Agregar")
        btn_add_prof.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_add_prof.setStyleSheet("QPushButton { background-color: #1e293b; color: #3b82f6; border: 1px solid #3b82f6; border-radius: 6px; padding: 7px 14px; font-weight: bold; } QPushButton:hover { background-color: #2563eb; color: #ffffff; }")
        btn_add_prof.clicked.connect(self._add_profesor)
        add_prof_h.addWidget(self.prof_input)
        add_prof_h.addWidget(btn_add_prof)
        prof_layout.addLayout(add_prof_h)
        self.prof_chips = ChipListWidget()
        prof_layout.addWidget(self.prof_chips)
        content_layout.addWidget(prof_card)

        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        btn_bar = QHBoxLayout()
        btn_bar.setContentsMargins(4, 8, 4, 4)
        btn_clear = QPushButton("🗑 Quitar Portada")
        btn_clear.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_clear.setStyleSheet("QPushButton { background-color: #451a1a; color: #fca5a5; border: 1px solid #7f1d1d; border-radius: 6px; padding: 8px 16px; font-weight: 500; } QPushButton:hover { background-color: #7f1d1d; color: #ffffff; }")
        btn_clear.clicked.connect(self._clear_and_close)
        btn_bar.addWidget(btn_clear)
        btn_bar.addStretch()
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancel.setStyleSheet("QPushButton { background-color: #1e293b; color: #94a3b8; border: 1px solid #334155; border-radius: 6px; padding: 8px 16px; font-weight: 500; } QPushButton:hover { background-color: #334155; color: #e2e8f0; }")
        btn_cancel.clicked.connect(self.reject)
        btn_bar.addWidget(btn_cancel)
        btn_save = QPushButton("💾 Guardar Portada")
        btn_save.setDefault(True)
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.setStyleSheet("QPushButton { background-color: #2563eb; color: #ffffff; border: 1px solid #3b82f6; border-radius: 6px; padding: 8px 20px; font-weight: bold; } QPushButton:hover { background-color: #1d4ed8; }")
        btn_save.clicked.connect(self._on_save)
        btn_bar.addWidget(btn_save)

        main_layout.addLayout(btn_bar)

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
        from PyQt6.QtWidgets import QInputDialog
        name, ok = QInputDialog.getText(self, 'Guardar plantilla', 'Nombre de la plantilla:')
        if not ok or not name.strip(): return
        templates = self._read_templates(); templates[name.strip()] = self.get_cover_data(); self._write_templates(templates)
        self.template_selector.clear(); self.template_selector.addItem('Seleccionar plantilla…', None); self._load_templates_into_selector()

    def _apply_template(self):
        name = self.template_selector.currentData()
        if name and name in self._read_templates(): self.set_cover_data(self._read_templates()[name])

    def _delete_template(self):
        name = self.template_selector.currentData()
        if not name: return
        templates = self._read_templates(); templates.pop(name, None); self._write_templates(templates)
        self.template_selector.clear(); self.template_selector.addItem('Seleccionar plantilla…', None); self._load_templates_into_selector()

    def _on_logo_toggled(self, checked: bool):
        self.diagram.setEnabled(checked)
        effect = QGraphicsOpacityEffect(self.diagram)
        effect.setOpacity(1.0 if checked else 0.4)
        self.diagram.setGraphicsEffect(effect)

    def _on_logo_position_changed(self, pos_key: str):
        self.logo_position = pos_key

    def _add_integrante(self):
        text = self.int_input.text().strip()
        if text: self.int_chips.add_item(text); self.int_input.clear()

    def _add_profesor(self):
        text = self.prof_input.text().strip()
        if text: self.prof_chips.add_item(text); self.prof_input.clear()

    def _clear_and_close(self):
        self.title_input.clear(); self.subtitle_input.clear(); self.materia_input.clear()
        self.toggle_logo.setChecked(False)
        self.int_chips.clear(); self.prof_chips.clear()
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
        self.diagram.set_position(pos)
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