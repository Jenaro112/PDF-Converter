import sys
import signal
from PyQt6.QtWidgets import QApplication
from mvc.controllers.app_controller import AppController

def main():
    # Manejar Ctrl+C y cierre de ventana limpiamente sin mensajes de interrupción
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    controller = AppController()
    controller.run()
    exit_code = app.exec()
    controller.shutdown()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
