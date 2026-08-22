"""
Módulo de registro (Logger) con formato visual elegante y colores mediante Rich.
Proporciona niveles de log (INFO, SUCCESS, WARNING, ERROR, DEBUG) con iconos,
marcas de tiempo y categorías coloreadas para una experiencia en terminal profesional.
"""

import sys
import os
from datetime import datetime

try:
    from rich.console import Console
    from rich.theme import Theme
    from rich.panel import Panel
    _RICH_AVAILABLE = True
except ImportError:
    _RICH_AVAILABLE = False

# Asegurar soporte de codificación UTF-8 en terminales de Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

_CUSTOM_THEME = Theme({
    "time": "dim cyan",
    "cat.app": "bold bright_cyan",
    "cat.file": "bold bright_magenta",
    "cat.pdf": "bold bright_green",
    "cat.cover": "bold bright_blue",
    "cat.page": "bold bright_blue",
    "cat.watcher": "bold bright_yellow",
    "cat.js": "dim yellow",
    "cat.pandoc": "bold bright_cyan",
    "cat.engine": "bold purple",
    "path": "underline cyan",
}) if _RICH_AVAILABLE else None

_CONSOLE = Console(theme=_CUSTOM_THEME, color_system="auto") if _RICH_AVAILABLE else None


class Logger:
    """Logger principal de la aplicación con soporte para colores Rich."""

    @staticmethod
    def _timestamp() -> str:
        return datetime.now().strftime("%H:%M:%S")

    @classmethod
    def banner(cls):
        """Muestra el banner inicial de PDF-Converter en terminal."""
        if not _RICH_AVAILABLE:
            print("=== PDF-Converter ===")
            return
        
        _CONSOLE.print(Panel(
            "[bold bright_cyan]PDF-Converter[/] [dim]│[/] [green]Live Markdown & DOCX to PDF[/]\n"
            "[dim]Renderizado Incremental & KaTeX & Mermaid Activo[/]",
            border_style="bright_blue",
            expand=False,
            padding=(0, 2)
        ))

    @classmethod
    def info(cls, category: str, message: str):
        """Log informativo (azul/cyan)."""
        cat = category.upper()
        now = cls._timestamp()
        if _RICH_AVAILABLE:
            _CONSOLE.print(f"[dim cyan][{now}][/] [cyan]ℹ[/] [bold cyan]\\[{cat}][/] {message}")
        else:
            print(f"[{now}] [INFO] [{cat}] {message}")

    @classmethod
    def success(cls, category: str, message: str):
        """Log de éxito (verde brillante con tilde)."""
        cat = category.upper()
        now = cls._timestamp()
        if _RICH_AVAILABLE:
            _CONSOLE.print(f"[dim cyan][{now}][/] [bold bright_green]✔[/] [bold bright_green]\\[{cat}][/] [bold green]{message}[/]")
        else:
            print(f"[{now}] [OK] [{cat}] {message}")

    @classmethod
    def warning(cls, category: str, message: str):
        """Log de advertencia (amarillo brillante con alerta)."""
        cat = category.upper()
        now = cls._timestamp()
        if _RICH_AVAILABLE:
            _CONSOLE.print(f"[dim cyan][{now}][/] [bold bright_yellow]⚠[/] [bold bright_yellow]\\[{cat}][/] [bright_yellow]{message}[/]")
        else:
            print(f"[{now}] [WARN] [{cat}] {message}")

    @classmethod
    def error(cls, category: str, message: str):
        """Log de error (rojo brillante con cruz)."""
        cat = category.upper()
        now = cls._timestamp()
        if _RICH_AVAILABLE:
            _CONSOLE.print(f"[dim cyan][{now}][/] [bold bright_red]✖[/] [bold bright_red]\\[{cat}][/] [bold red]{message}[/]")
        else:
            print(f"[{now}] [ERROR] [{cat}] {message}")

    @classmethod
    def debug(cls, category: str, message: str):
        """Log de depuración / secundario (atenuado)."""
        cat = category.upper()
        now = cls._timestamp()
        if _RICH_AVAILABLE:
            _CONSOLE.print(f"[dim white][{now}][/] [dim]•[/] [dim]\\[{cat}][/] [dim]{message}[/]")
        else:
            print(f"[{now}] [DEBUG] [{cat}] {message}")

    @classmethod
    def js_console(cls, level: str, line: int, message: str):
        """
        Registra mensajes provenientes de la consola JavaScript del motor Chromium,
        filtrando advertencias internas de SVG inofensivas.
        """
        # Filtrar advertencias internas inofensivas de Chromium/SVG
        ignored_patterns = [
            'Expected number, "translate(undefined, NaN)"',
            "translate(undefined, NaN)",
            "<g> attribute transform",
            "Error Mermaid update: [object Object]",
        ]
        for ign in ignored_patterns:
            if ign in message:
                return

        now = cls._timestamp()
        msg_clean = message.replace("[", "\\[").replace("]", "\\]")
        if _RICH_AVAILABLE:
            _CONSOLE.print(f"[dim cyan][{now}][/] [dim yellow]⚡[/] [dim yellow]\\[JS:L{line}][/] [dim yellow]{msg_clean}[/]")
        else:
            print(f"[{now}] [JS:L{line}] {message}")


logger = Logger
