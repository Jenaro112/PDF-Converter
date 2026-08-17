import sys
import os
import signal
import platform

# Asegurar que el directorio src/ esté en sys.path para que los imports
# funcionen independientemente del directorio de trabajo actual.
_src_dir = os.path.dirname(os.path.abspath(__file__))
if _src_dir not in sys.path:
    sys.path.insert(0, _src_dir)

from PySide6.QtWidgets import QApplication
from mvc.controllers.app_controller import AppController

def main():
    # Manejar Ctrl+C y cierre de ventana limpiamente sin mensajes de interrupción
    # SIGINT funciona en todas las plataformas
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    
    # Aplicar tipografía Inter globalmente
    from PySide6.QtGui import QFont
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
