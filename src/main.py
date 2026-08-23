import sys
import os
import signal
import platform

# Bootstrap automático del entorno virtual del proyecto (.venv)
# Garantiza compatibilidad 100% en macOS (Unix) y Windows
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Detectar el ejecutable de Python del venv según el SO
if sys.platform == "win32":
    _venv_python = os.path.join(_project_root, ".venv", "Scripts", "python.exe")
else:
    _venv_python = os.path.join(_project_root, ".venv", "bin", "python")

# Si se ejecuta con un Python distinto al del venv, relanzar dentro del venv
if os.path.exists(_venv_python):
    _curr_exe = os.path.realpath(sys.executable)
    _target_exe = os.path.realpath(_venv_python)
    if _curr_exe != _target_exe and os.environ.get("_PDF_CONVERTER_REEXEC") != "1":
        os.environ["_PDF_CONVERTER_REEXEC"] = "1"
        os.environ["VIRTUAL_ENV"] = os.path.join(_project_root, ".venv")
        # En macOS/Linux, quitar cualquier flag hidden de plugins Qt si existiera
        if sys.platform == "darwin":
            try:
                import subprocess
                subprocess.run(
                    ["chflags", "-R", "nohidden", os.path.join(_project_root, ".venv", "lib")],
                    capture_output=True,
                    timeout=2
                )
            except Exception:
                pass
        os.execv(_venv_python, [_venv_python] + sys.argv)

# Asegurar que el directorio src/ esté en sys.path
_src_dir = os.path.dirname(os.path.abspath(__file__))
if _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)

# Configuración determinista y multiplataforma de plugins de Qt (macOS y Windows)
import PySide6
from PySide6.QtCore import QCoreApplication

_pyside_dir = os.path.dirname(PySide6.__file__)
_qt_plugins = os.path.join(_pyside_dir, "Qt", "plugins")
if os.path.exists(_qt_plugins):
    # En macOS, iCloud Drive o Finder a veces marcan los dylibs en .venv con el flag UF_HIDDEN (0x8000).
    # Qt QDir::Files descarta archivos con UF_HIDDEN. Limpiamos el flag instantáneamente (<1ms) con os.chflags.
    if hasattr(os, "chflags"):
        for _root, _, _files in os.walk(_qt_plugins):
            for _fname in _files:
                _fpath = os.path.join(_root, _fname)
                try:
                    _st = os.stat(_fpath)
                    if _st.st_flags & 0x8000:
                        os.chflags(_fpath, _st.st_flags & ~0x8000)
                except OSError:
                    pass

    os.environ["QT_PLUGIN_PATH"] = _qt_plugins
    _platforms = os.path.join(_qt_plugins, "platforms")
    if os.path.exists(_platforms):
        os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = _platforms
    QCoreApplication.addLibraryPath(_qt_plugins)

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont, QFontDatabase
from mvc.controllers.app_controller import AppController
from utils.logger import logger
from desing.design_tokens import DEFAULT_THEME

def main():
    logger.banner()
    # Manejar Ctrl+C y cierre de ventana limpiamente sin mensajes de interrupción
    # SIGINT funciona en todas las plataformas
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    
    # Cargar fuentes personalizadas desde assets/fonts
    fonts_dir = os.path.join(_project_root, 'assets', 'fonts')
    if os.path.isdir(fonts_dir):
        for fname in os.listdir(fonts_dir):
            if fname.lower().endswith(('.ttf', '.otf', '.woff2')):
                fpath = os.path.join(fonts_dir, fname)
                font_id = QFontDatabase.addApplicationFont(fpath)
                if font_id != -1:
                    families = QFontDatabase.applicationFontFamilies(font_id)
                    logger.debug("Fuentes", f"Cargada: {fname} → {families}")

    # Aplicar tipografía Inter globalmente
    font = QFont("Inter", 10)
    app.setFont(font)

    # Cargar QSS global
    qss_path = os.path.join(_src_dir, 'styles.qss')
    if os.path.exists(qss_path):
        with open(qss_path, encoding='utf-8') as f:
            app.setStyleSheet(f.read())

    controller = AppController()
    controller.run()
    exit_code = app.exec()
    controller.shutdown()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
