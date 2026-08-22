import os
import platform
import subprocess
from pathlib import Path
from utils.logger import logger

_IS_WINDOWS = platform.system() == 'Windows'

class PdfExporterFacade:
    """
    Facade que abstrae la complejidad de exportar a PDF,
    manejando Puppeteer (Node.js) como motor principal
    y WeasyPrint como fallback transparente.
    """
    def __init__(self, script_dir: Path = None):
        if script_dir is None:
            # Asume que pdf.mjs está en src/scripts/ respecto a este archivo
            self.script_dir = Path(__file__).parent.parent / "scripts"
        else:
            self.script_dir = Path(script_dir)
            
    def export_to_pdf(self, html_path: str, pdf_path: str, footer_text: str = "") -> tuple[bool, str]:
        """
        Intenta exportar el HTML a PDF usando WeasyPrint como motor principal
        para garantizar máxima calidad lossless.
        Si falla o no está disponible, hace fallback a Puppeteer (Node.js).
        
        Args:
            html_path: Ruta absoluta al archivo HTML temporal.
            pdf_path: Ruta absoluta donde guardar el PDF.
            
        Returns:
            Una tupla (exito: bool, motor_utilizado: str|None)
        """
        # Intentar Puppeteer primero (Motor principal con SVG Wrapper para máxima calidad)
        if self._generate_pdf_puppeteer(html_path, pdf_path, footer_text):
            return True, "Puppeteer"
            
        logger.warning("PDF", "Puppeteer no disponible o falló, probando WeasyPrint como fallback…")
        
        # Fallback a WeasyPrint
        if self._generate_pdf_weasyprint(html_path, pdf_path):
            return True, "WeasyPrint"
            
        return False, None

    def _generate_pdf_puppeteer(self, html_path: str, pdf_path: str, footer_text: str = "") -> bool:
        pdf_script = self.script_dir / "pdf.mjs"
        if not pdf_script.exists():
            return False
            
        try:
            result = subprocess.run(
                ["node", str(pdf_script), os.path.abspath(html_path), os.path.abspath(pdf_path), footer_text],
                capture_output=True, text=True,
                shell=_IS_WINDOWS  # En Windows, node puede necesitar shell=True
            )
            if result.returncode != 0:
                logger.error("Puppeteer", f"Error de ejecución: {result.stderr.strip()}")
                return False
            return True
        except Exception as e:
            logger.error("Puppeteer", f"Error al ejecutar Node.js: {e}")
            return False

    def _generate_pdf_weasyprint(self, html_path: str, pdf_path: str) -> bool:
        try:
            from weasyprint import HTML
            import logging
            
            # Configurar el logger de WeasyPrint para ver errores de fuentes y dependencias
            wp_logger = logging.getLogger('weasyprint')
            wp_logger.handlers = [] # Limpiar handlers previos
            wp_logger.addHandler(logging.StreamHandler())
            wp_logger.setLevel(logging.WARNING) # Mostrar advertencias sobre fuentes fallidas
            
            # Usar el directorio de trabajo actual como base_url para que encuentre las imágenes relativas si alguna no se convirtió a URI absoluta.
            # Path.as_uri() genera URIs correctas en Windows (file:///C:/...) y Unix
            base_url = Path(os.getcwd()).as_uri() + '/'
            HTML(filename=html_path, base_url=base_url).write_pdf(pdf_path)
            return True
        except ImportError:
            return False
        except Exception as e:
            logger.error("WeasyPrint", f"Error en WeasyPrint: {e}")
            return False
