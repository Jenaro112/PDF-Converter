from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings, QWebEnginePage
from PySide6.QtCore import QUrl
import json
import os

from utils.logger import logger

class CustomWebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        logger.js_console(str(level), lineNumber, message)

class PreviewPanel(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.custom_page = CustomWebEnginePage(self)
        self.setPage(self.custom_page)
        
        self.settings().setAttribute(
            QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True
        )
        self.settings().setAttribute(
            QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True
        )

        self._shell_loaded: bool = False
        self._pending_content: str | None = None
        self.loadFinished.connect(self._on_load_finished)

    def reset_scroll(self):
        """Resetea la posición de scroll a 0 (utilizado al abrir un archivo nuevo)."""
        if self._shell_loaded:
            self.page().runJavaScript("window.scrollTo(0, 0);")

    def load_shell(self, html: str, base_path: str = None):
        """
        Carga el shell HTML completo (CSS, JS, fonts) via setHtml().
        Se usa solo al inicio, cambio de tema, o cambio de configuración de página.
        """
        self._shell_loaded = False
        self._pending_content = None
        b_path = os.getcwd() if base_path is None else base_path
        base_url = QUrl.fromLocalFile(os.path.join(b_path, ""))
        self.setHtml(html, base_url)

    def update_content(self, body_html: str):
        """
        Actualiza solo el contenido del documento via JavaScript.
        No recarga la página, preserva scroll y estado de la página.
        """
        if not self._shell_loaded:
            self._pending_content = body_html
            return
        # Usar JSON.dumps para escapar de forma segura el HTML como string JS
        escaped = json.dumps(body_html)
        js = f'if(window.updateContent) window.updateContent({escaped});'
        self.page().runJavaScript(js)

    def set_html(self, html: str, base_path: str = None):
        """
        Compatibilidad: carga HTML completo (equivale a load_shell).
        """
        self.load_shell(html, base_path)

    def _on_load_finished(self, success: bool):
        if success:
            self._shell_loaded = True
            if self._pending_content is not None:
                self.update_content(self._pending_content)
                self._pending_content = None
