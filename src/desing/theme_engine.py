"""
Motor de temas: aplica tokens de diseño a la interfaz Qt.

Genera hojas de estilo QSS dinámicamente desde los design tokens,
permitiendo cambiar entre Vanguardia Institucional y Ecosistema Moderno.
"""

from src.desing.design_tokens import TEMAS, DEFAULT_THEME


def get_theme(name: str | None = None) -> dict:
    """Devuelve el diccionario de tokens para el tema solicitado."""
    if name is None:
        name = DEFAULT_THEME
    return TEMAS.get(name, TEMAS[DEFAULT_THEME])


def generate_qss(theme: dict) -> str:
    """
    Genera una hoja de estilos Qt (QSS) a partir de los tokens del tema.

    Parameters
    ----------
    theme : dict
        Diccionario con la estructura de TEMA_VANGUARDIA / TEMA_ECOSISTEMA.

    Returns
    -------
    str
        Cadena QSS lista para aplicar con ``widget.setStyleSheet(qss)``.
    """
    fonts = theme["fonts"]
    colors = theme["colors"]

    heading_font = f"'{fonts['heading']}', {fonts['fallback']}"
    body_font = f"'{fonts['body']}', {fonts['fallback']}"

    qss = f"""
    /* ============================================
       TEMA: {theme['name']}
       Generado automáticamente por theme_engine.py
       ============================================ */

    /* --- BASE --- */
    QWidget {{
        background-color: {colors['background']};
        color: {colors['body']};
        font-family: {body_font};
        font-size: 14px;
    }}

    QMainWindow {{
        background-color: {colors['background']};
    }}

    /* --- ENCABEZADOS --- */
    QLabel#heading, QLabel#title {{
        font-family: {heading_font};
        font-weight: 700;
        color: {colors['heading']};
        font-size: 24px;
    }}

    QLabel#subtitle {{
        font-family: {heading_font};
        font-weight: 600;
        color: {colors['heading']};
        font-size: 18px;
    }}

    QLabel#sectionTitle {{
        font-family: {heading_font};
        font-weight: 600;
        color: {colors['heading']};
        font-size: 16px;
        padding-bottom: 4px;
        border-bottom: 2px solid {colors['accent']};
    }}

    /* --- BOTONES PRIMARIOS --- */
    QPushButton {{
        background-color: {colors['accent']};
        color: #FFFFFF;
        font-family: {body_font};
        font-weight: 600;
        font-size: 14px;
        padding: 10px 24px;
        border: none;
        border-radius: 8px;
    }}

    QPushButton:hover {{
        background-color: {colors['accent_hover']};
    }}

    QPushButton:pressed {{
        background-color: {colors['accent_pressed']};
    }}

    QPushButton:disabled {{
        background-color: {colors['disabled_bg']};
        color: {colors['disabled_fg']};
    }}

    /* --- BOTONES SECUNDARIOS --- */
    QPushButton#secondary {{
        background-color: transparent;
        color: {colors['accent']};
        border: 2px solid {colors['accent']};
        border-radius: 8px;
    }}

    QPushButton#secondary:hover {{
        background-color: {colors['muted']};
    }}

    /* --- INPUTS --- */
    QLineEdit, QTextEdit, QPlainTextEdit {{
        background-color: {colors['surface']};
        color: {colors['body']};
        font-family: {body_font};
        font-size: 14px;
        border: 1.5px solid {colors['border']};
        border-radius: 8px;
        padding: 8px 12px;
    }}

    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
        border-color: {colors['accent']};
    }}

    /* --- COMBO BOX --- */
    QComboBox {{
        background-color: {colors['surface']};
        color: {colors['body']};
        font-family: {body_font};
        font-size: 14px;
        border: 1.5px solid {colors['border']};
        border-radius: 8px;
        padding: 8px 12px;
    }}

    QComboBox:hover {{
        border-color: {colors['accent']};
    }}

    QComboBox::drop-down {{
        border: none;
        padding-right: 8px;
    }}

    /* --- SPIN BOX --- */
    QSpinBox, QDoubleSpinBox {{
        background-color: {colors['surface']};
        color: {colors['body']};
        font-family: {body_font};
        border: 1.5px solid {colors['border']};
        border-radius: 8px;
        padding: 6px 10px;
    }}

    /* --- CHECK BOX / RADIO --- */
    QCheckBox, QRadioButton {{
        color: {colors['body']};
        font-family: {body_font};
        font-size: 14px;
        spacing: 8px;
    }}

    QCheckBox::indicator:checked, QRadioButton::indicator:checked {{
        background-color: {colors['accent']};
        border: 2px solid {colors['accent']};
        border-radius: 3px;
    }}

    /* --- TABS --- */
    QTabWidget::pane {{
        border: 1px solid {colors['border']};
        border-radius: 8px;
        background-color: {colors['surface']};
    }}

    QTabBar::tab {{
        background-color: {colors['muted']};
        color: {colors['body']};
        font-family: {body_font};
        font-weight: 600;
        font-size: 13px;
        padding: 10px 20px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        margin-right: 2px;
    }}

    QTabBar::tab:selected {{
        background-color: {colors['surface']};
        color: {colors['heading']};
        border-bottom: 2px solid {colors['accent']};
    }}

    QTabBar::tab:hover:!selected {{
        background-color: {colors['border']};
    }}

    /* --- PROGRESS BAR --- */
    QProgressBar {{
        background-color: {colors['border']};
        border: none;
        border-radius: 6px;
        height: 10px;
        text-align: center;
        font-size: 0px;
    }}

    QProgressBar::chunk {{
        background-color: {colors['accent']};
        border-radius: 6px;
    }}

    /* --- SCROLL BARS --- */
    QScrollBar:vertical {{
        background-color: {colors['muted']};
        width: 10px;
        border-radius: 5px;
    }}

    QScrollBar::handle:vertical {{
        background-color: {colors['disabled_bg']};
        border-radius: 5px;
        min-height: 30px;
    }}

    QScrollBar::handle:vertical:hover {{
        background-color: {colors['accent']};
    }}

    QScrollBar::add-line, QScrollBar::sub-line {{
        height: 0px;
    }}

    QScrollBar:horizontal {{
        background-color: {colors['muted']};
        height: 10px;
        border-radius: 5px;
    }}

    QScrollBar::handle:horizontal {{
        background-color: {colors['disabled_bg']};
        border-radius: 5px;
        min-width: 30px;
    }}

    /* --- TOOLTIPS --- */
    QToolTip {{
        background-color: {colors['heading']};
        color: {colors['background']};
        font-family: {body_font};
        font-size: 12px;
        border: none;
        border-radius: 6px;
        padding: 6px 10px;
    }}

    /* --- STATUS BAR --- */
    QStatusBar {{
        background-color: {colors['muted']};
        color: {colors['body']};
        font-family: {body_font};
        font-size: 12px;
        border-top: 1px solid {colors['border']};
    }}

    /* --- GROUP BOX --- */
    QGroupBox {{
        font-family: {heading_font};
        font-weight: 600;
        font-size: 15px;
        color: {colors['heading']};
        border: 1.5px solid {colors['border']};
        border-radius: 10px;
        margin-top: 16px;
        padding-top: 20px;
    }}

    QGroupBox::title {{
        subcontrol-origin: margin;
        left: 16px;
        padding: 0 8px;
        background-color: {colors['background']};
    }}

    /* --- MENU --- */
    QMenuBar {{
        background-color: {colors['surface']};
        color: {colors['body']};
        font-family: {body_font};
        font-size: 13px;
        border-bottom: 1px solid {colors['border']};
    }}

    QMenuBar::item:selected {{
        background-color: {colors['muted']};
        color: {colors['accent']};
        border-radius: 4px;
    }}

    QMenu {{
        background-color: {colors['surface']};
        color: {colors['body']};
        border: 1px solid {colors['border']};
        border-radius: 8px;
        padding: 4px;
    }}

    QMenu::item:selected {{
        background-color: {colors['muted']};
        color: {colors['accent']};
        border-radius: 4px;
    }}
    """
    return qss.strip()


def apply_theme(widget, theme_name: str | None = None) -> None:
    """Atajo: obtiene el tema y aplica el QSS al widget."""
    theme = get_theme(theme_name)
    qss = generate_qss(theme)
    widget.setStyleSheet(qss)
