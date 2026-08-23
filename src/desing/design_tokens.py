"""
Tokens de diseño para los temas visuales de la aplicación PDF Converter.

Cada diccionario define fuentes, colores y estilos base para un tema.
Solo temas sans-serif institucionales — sin fuentes serif.
"""

# ======================================
# TEMA A – VANGUARDIA INSTITUCIONAL
# (Tech Dark Invertido)
# Fuentes: Cabinet Grotesk + Satoshi
# Paleta: Fondo claro + Azul tech
# ======================================
TEMA_VANGUARDIA = {
    "name": "Vanguardia Institucional",
    "fonts": {
        "heading": "Cabinet Grotesk",
        "body": "Satoshi",
        "fallback": "Inter, Segoe UI, sans-serif",
    },
    "colors": {
        "background": "#F8FAFC",
        "heading": "#1A1B26",
        "body": "#4C4F69",
        "accent": "#7AA2F7",
        "accent_hover": "#6A92E7",
        "accent_pressed": "#5A82D7",
        "border": "#E2E8F0",
        "surface": "#FFFFFF",
        "muted": "#F1F5F9",
        "disabled_bg": "#CBD5E1",
        "disabled_fg": "#94A3B8",
    },
}

# ======================================
# TEMA B – ECOSISTEMA MODERNO
# (Monocromo de Alta Precisión)
# Fuentes: Manrope + Geist
# Paleta: Zinc monocromo
# ======================================
TEMA_ECOSISTEMA = {
    "name": "Ecosistema Moderno",
    "fonts": {
        "heading": "Manrope",
        "body": "Geist",
        "fallback": "Inter, Segoe UI, sans-serif",
    },
    "colors": {
        "background": "#F8FAFC",
        "heading": "#09090B",
        "body": "#52525B",
        "accent": "#18181B",
        "accent_hover": "#27272A",
        "accent_pressed": "#3F3F46",
        "border": "#E4E4E7",
        "surface": "#FFFFFF",
        "muted": "#F4F4F5",
        "disabled_bg": "#D4D4D8",
        "disabled_fg": "#A1A1AA",
    },
}

# ----- Mapa de acceso rápido -----
TEMAS = {
    "vanguardia": TEMA_VANGUARDIA,
    "ecosistema": TEMA_ECOSISTEMA,
}

DEFAULT_THEME = "vanguardia"
