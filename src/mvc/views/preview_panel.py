from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEnginePage
from PyQt6.QtCore import QUrl
import os

class CustomWebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print(f"[JS Console] Line {lineNumber}: {message}")

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

        self._saved_scroll_y: float = 0.0
        self.loadFinished.connect(self._on_load_finished)

    def reset_scroll(self):
        """Resetea la posición de scroll a 0 (utilizado al abrir un archivo nuevo)."""
        self._saved_scroll_y = 0.0

    def set_html(self, html: str, base_path: str = None):
        """
        Renderiza HTML en el preview preservando la posición de scroll actual.
        """
        b_path = os.getcwd() if base_path is None else base_path
        base_url = QUrl.fromLocalFile(os.path.join(b_path, ""))

        def _on_scroll_captured(val):
            if isinstance(val, (int, float)) and val > 0:
                self._saved_scroll_y = float(val)
            self.setHtml(html, base_url)

        self.page().runJavaScript("window.scrollY", _on_scroll_captured)

    def _on_load_finished(self, success: bool):
        if success and self._saved_scroll_y > 0:
            self.page().runJavaScript(f"window.scrollTo(0, {self._saved_scroll_y});")
