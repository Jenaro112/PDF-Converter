import tempfile
import os
import traceback
import re
import sys
import platform
import shutil
from typing import Optional
from PySide6.QtCore import QObject, QThread, Signal, Slot, QTimer, QFileSystemWatcher
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QFileDialog, QMessageBox, QDialog

from mvc.models.document import DocumentModel
from mvc.models.theme_manager import ThemeManager
from mvc.models.docx_converter import DocxConverter
from mvc.models.recovery import RecoveryManager
from mvc.views.main_window import MainWindow
from mvc.views.cover_dialog import CoverDialog
from facade.pdf_exporter import PdfExporterFacade
from utils.logger import logger

class RenderWorker(QObject):
    finished = Signal(str)
    content_ready = Signal(str)

    def __init__(self, model: DocumentModel):
        super().__init__()
        self.model = model

    @Slot(dict)
    def render(self, data: dict):
        html = self.model.render_html(
            md_text=data.get('text', ''),
            theme_key=data.get('theme', 'minimal'),
            show_cover=data.get('show_cover', False),
            title=data.get('title', ''),
            subtitle=data.get('subtitle', ''),
            materia=data.get('materia', ''),
            integrantes=data.get('integrantes', ''),
            profesores=data.get('profesores', ''),
            show_logo=data.get('show_logo', False),
            logo_position=data.get('logo_position', 'top-left'),
            cover_style=data.get('cover_style', 'folio'),
            page_config=data.get('page_config', {}),
            is_preview=True
        )
        self.finished.emit(html)

    @Slot(dict)
    def render_content(self, data: dict):
        body_html = self.model.render_preview_content(
            md_text=data.get('text', ''),
            theme_key=data.get('theme', 'minimal'),
            show_cover=data.get('show_cover', False),
            title=data.get('title', ''),
            subtitle=data.get('subtitle', ''),
            materia=data.get('materia', ''),
            integrantes=data.get('integrantes', ''),
            profesores=data.get('profesores', ''),
            show_logo=data.get('show_logo', False),
            logo_position=data.get('logo_position', 'top-left'),
            cover_style=data.get('cover_style', 'folio'),
        )
        self.content_ready.emit(body_html)

class AppController(QObject):
    _render_request = Signal(dict)
    _content_request = Signal(dict)
    
    def __init__(self):
        super().__init__()
        self.model = DocumentModel()
        self.facade = PdfExporterFacade()
        self.converter = DocxConverter()
        self.recovery = RecoveryManager()
        self.current_file_path: Optional[str] = None
        
        # Estado de archivos temporales para limpieza post-exportación
        self._temp_md_path: Optional[str] = None
        self._temp_media_dir: Optional[str] = None
        
        # Estado de portada modal
        self._cover_data = {
            'show_cover': False,
            'title': '',
            'subtitle': '',
            'materia': '',
            'integrantes': '',
            'profesores': '',
            'integrantes_list': [],
            'profesores_list': [],
            'show_logo': False,
            'logo_position': 'top-left',
            'cover_style': 'folio',
        }
        
        # Estado de página modal
        self._page_data = {
            'numbering_style': '1',
            'header_left': '',
            'header_center': '',
            'header_right': '',
            'footer_left': '',
            'footer_center': '',
            'footer_right': '',
            'header_logo': ''
        }

        theme_choices = ThemeManager.get_theme_choices()
        self.view = MainWindow(theme_choices)
        
        self.debounce_timer = QTimer()
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.timeout.connect(self._trigger_content_update)
        
        self._init_threading()
        self._connect_signals()
        
        self.file_watcher = QFileSystemWatcher(self)
        self.file_watcher.fileChanged.connect(self._on_external_file_changed)
        
        self.autosave_timer = QTimer(self)
        self.autosave_timer.setInterval(45_000)
        self.autosave_timer.timeout.connect(self._autosave)
        self.autosave_timer.start()

    def _init_threading(self):
        self.thread = QThread()
        self.worker = RenderWorker(self.model)
        self.worker.moveToThread(self.thread)
        self._render_request.connect(self.worker.render)
        self._content_request.connect(self.worker.render_content)
        self.worker.finished.connect(self._on_render_finished)
        self.worker.content_ready.connect(self._on_content_finished)
        self.thread.start()

    def _connect_signals(self):
        self.view.text_changed.connect(self._on_text_changed)
        self.view.options_changed.connect(self._on_options_changed)
        self.view.export_requested.connect(self._on_export_requested)
        self.view.file_opened.connect(self._on_file_opened)
        self.view.file_selected_from_explorer.connect(self._on_file_opened)
        self.view.cover_requested.connect(self._on_cover_requested)
        self.view.page_config_requested.connect(self._on_page_config_requested)
        self.view.save_requested.connect(self._save_document)
        self.view.editor.image_pasted.connect(self._on_image_pasted)
        self.view.combine_requested.connect(self._combine_files)
        self.view.format_requested.connect(self._on_format_requested)
        self.view.closed.connect(self.shutdown)

    def shutdown(self):
        if getattr(self, '_is_shutting_down', False):
            return
        self._is_shutting_down = True
        logger.info("App", "Cerrando aplicación y liberando recursos...")
        if hasattr(self, 'thread') and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait(1000)

    def run(self):
        self.view.show()
        self._trigger_full_render()
        
    def _on_text_changed(self, *_):
        self.view.show_status("Escribiendo...")
        self.debounce_timer.start(150)

    def _on_options_changed(self, *_):
        self.view.show_status("Cambiando tema...")
        self._trigger_full_render()

    def _autosave(self):
        text = self.view.editor.toPlainText()
        if text.strip():
            self.recovery.save(self.current_file_path or 'unsaved.md', text)
            self.view.show_status('Recuperación automática actualizada', 1500)

    def _save_document(self):
        path = self.current_file_path
        if not path or not path.lower().endswith('.md'):
            path, _ = QFileDialog.getSaveFileName(self.view, 'Guardar Markdown', '', 'Markdown (*.md)')
        if not path: return
        if not path.lower().endswith('.md'): path += '.md'
        try:
            with open(path, 'w', encoding='utf-8') as handle: handle.write(self.view.editor.toPlainText())
            self.current_file_path = path
            self.recovery.clear(path)
            self._clean_orphan_images(path)
            self.view.show_status(f'Guardado: {os.path.basename(path)}', 3000)
        except OSError as exc:
            QMessageBox.critical(self.view, 'Error al guardar', str(exc))

    def _on_format_requested(self):
        """Formatea el Markdown del editor usando el formateador seguro de DocumentModel."""
        text = self.view.editor.toPlainText()
        if not text.strip():
            self.view.show_status("Nada que formatear", 2000)
            return
        try:
            formatted = self.model.format_markdown(text)
            if formatted == text:
                self.view.show_status("El Markdown ya está bien formateado ✓", 2500)
                return

            # Preservar posición del cursor y habilitar Undo/Redo mediante edit block
            cursor = self.view.editor.textCursor()
            pos = cursor.position()

            cursor.beginEditBlock()
            cursor.select(QTextCursor.SelectionType.Document)
            cursor.insertText(formatted)
            cursor.endEditBlock()

            # Restaurar cursor (ajustar si el texto cambió de longitud)
            new_pos = min(pos, len(formatted))
            cursor.setPosition(new_pos)
            self.view.editor.setTextCursor(cursor)

            self.view.show_status("Markdown formateado ✓", 3000)
            self._trigger_content_update()
        except ImportError:
            QMessageBox.warning(
                self.view, "mdformat no disponible",
                "Instalá mdformat con:\n\npip install mdformat"
            )
        except Exception as exc:
            QMessageBox.critical(
                self.view, "Error al formatear",
                f"No se pudo formatear el Markdown:\n\n{exc}"
            )

    def _on_image_pasted(self, image):
        if not self.current_file_path or not self.current_file_path.lower().endswith('.md'):
            QMessageBox.information(self.view, 'Guardá primero', 'Para pegar imágenes, guardá primero el documento Markdown.')
            return
        base, _ = os.path.splitext(self.current_file_path)
        image_dir = base + '_img'
        os.makedirs(image_dir, exist_ok=True)
        index = 1
        while os.path.exists(os.path.join(image_dir, f'imagen_{index}.png')): index += 1
        image_path = os.path.join(image_dir, f'imagen_{index}.png')
        if image.save(image_path, 'PNG'):
            relative = os.path.relpath(image_path, os.path.dirname(self.current_file_path)).replace(os.sep, '/')
            self.view.editor.textCursor().insertText(f'![]({relative})')
            self.view.show_status('Imagen añadida al documento', 2500)

    def _clean_orphan_images(self, md_path):
        base, _ = os.path.splitext(md_path); image_dir = base + '_img'
        if not os.path.isdir(image_dir): return
        refs = set(re.findall(r'!\[[^]]*\]\(([^)]+)\)', self.view.editor.toPlainText()))
        for filename in os.listdir(image_dir):
            relative = os.path.relpath(os.path.join(image_dir, filename), os.path.dirname(md_path)).replace(os.sep, '/')
            if relative not in refs:
                try: os.remove(os.path.join(image_dir, filename))
                except OSError: pass

    def _show_highlight_index(self):
        groups = {}
        pattern = re.compile(r'==((?:(?!==).)+?)==\(([^)]+)\)', re.DOTALL)
        for text, color in pattern.findall(self.view.editor.toPlainText()): groups.setdefault(color.strip(), []).append(text.replace('\n', ' '))
        if not groups:
            QMessageBox.information(self.view, 'Resaltados', 'No hay texto resaltado en el documento.'); return
        content = '# Resaltados por color\n\n' + '\n\n'.join(
            f'## {color}\n' + '\n'.join(f'- {item}' for item in items)
            for color, items in groups.items()
        )
        QMessageBox.information(self.view, 'Índice de resaltados', content)

    def _combine_files(self):
        paths, _ = QFileDialog.getOpenFileNames(self.view, 'Combinar documentos', '', 'Documentos (*.md *.docx)')
        if not paths: return
        parts = []
        try:
            for path in paths:
                if path.lower().endswith('.md'):
                    with open(path, encoding='utf-8') as handle: parts.append(handle.read())
                else:
                    success, md_path, _ = self.converter.detect_and_prepare(path)
                    if not success: raise RuntimeError(f'No se pudo convertir {os.path.basename(path)}')
                    with open(md_path, encoding='utf-8') as handle: parts.append(handle.read())
            self.current_file_path = None
            self.view.editor.setPlainText('\n\n<!-- PAGEBREAK -->\n\n'.join(parts))
            self.view.show_status(f'{len(parts)} documentos combinados; guardalo como Markdown', 5000)
        except Exception as exc:
            QMessageBox.critical(self.view, 'Error al combinar', str(exc))

    def _on_cover_requested(self):
        try:
            dialog = CoverDialog(self.view, initial_data=self._cover_data)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self._cover_data = dialog.get_cover_data()
                logger.info("Portada", f"Configuración guardada (estilo: [bold cyan]{self._cover_data.get('cover_style', 'folio')}[/])")
                self.view.show_status("Portada actualizada", 2000)
                self._trigger_content_update()
        except Exception as e:
            traceback.print_exc()
            logger.error("Portada", f"Error al configurar la portada: {e}")
            QMessageBox.critical(self.view, "Error", f"Ocurrió un error al configurar la portada:\n{e}")

    def _on_page_config_requested(self):
        try:
            from mvc.views.page_config_dialog import PageConfigDialog
            dialog = PageConfigDialog(self.view, initial_data=self._page_data)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self._page_data = dialog.get_page_config()
                logger.info("Página", f"Configuración guardada (márgenes/encabezados actualizados)")
                self.view.show_status("Configuración de página actualizada", 2000)
                self._trigger_full_render()
        except Exception as e:
            traceback.print_exc()
            logger.error("Página", f"Error al configurar la página: {e}")
            QMessageBox.critical(self.view, "Error", f"Ocurrió un error al configurar la página:\n{e}")

    def _on_external_file_changed(self, path):
        if path == self.current_file_path:
            try:
                # Reload file silently
                with open(path, 'r', encoding='utf-8') as f:
                    new_text = f.read()
                
                # Check if text is actually different to avoid unnecessary UI updates
                if self.view.editor.toPlainText() != new_text:
                    self.view.editor.blockSignals(True) # Prevent infinite loops with debounce
                    
                    # Guardar posición del cursor
                    cursor = self.view.editor.textCursor()
                    pos = cursor.position()
                    
                    self.view.editor.setPlainText(new_text)
                    
                    # Restaurar posición del cursor si es posible
                    if pos <= len(new_text):
                        cursor.setPosition(pos)
                        self.view.editor.setTextCursor(cursor)
                        
                    self.view.editor.blockSignals(False)
                    self.view.show_status("Recargado desde archivo externo", 2000)
                    logger.warning("Vigilante", f"Archivo externo modificado: [underline]{os.path.basename(path)}[/]. Recargando...")
                    self._trigger_content_update()
            except Exception as e:
                logger.error("Vigilante", f"Error al recargar archivo externo: {e}")

    def _trigger_content_update(self):
        if not getattr(self.view.preview, '_shell_loaded', False):
            self._trigger_full_render()
            return
        text = self.view.editor.toPlainText()
        options = self.view.get_current_options()
        options['text'] = text
        options.update(self._cover_data)
        options['page_config'] = self._page_data
        self._content_request.emit(options)

    def _trigger_full_render(self):
        self.view.show_status("Renderizando...")
        text = self.view.editor.toPlainText()
        options = self.view.get_current_options()
        options['text'] = text
        options.update(self._cover_data)
        options['page_config'] = self._page_data
        self._render_request.emit(options)

    def _trigger_render(self):
        self._trigger_content_update()

    @Slot(str)
    def _on_render_finished(self, html: str):
        self.view.set_preview_html(html)

    @Slot(str)
    def _on_content_finished(self, body_html: str):
        self.view.set_preview_content(body_html)

    def _on_file_opened(self, file_path: str):
        """
        Maneja la apertura de archivos .md y .docx.
        Si es .docx, convierte automáticamente a .md con Pandoc.
        Toda la lógica está protegida para evitar crashes.
        """
        try:
            self.view.preview.reset_scroll()
            # Validación: ruta no vacía
            if not file_path or not file_path.strip():
                logger.warning("Archivo", "Ruta vacía, ignorando apertura.")
                return

            logger.info("Archivo", f"Abriendo: [underline]{file_path}[/]")
            self.view.show_status("Abriendo archivo...")

            # Validación: archivo existe
            if not os.path.exists(file_path):
                logger.error("Archivo", f"El archivo no existe: {file_path}")
                QMessageBox.warning(
                    self.view, "Archivo no encontrado",
                    f"El archivo no existe:\n{file_path}"
                )
                self.view.show_status("Archivo no encontrado", 3000)
                return

            # Validación: formato soportado
            file_type = DocxConverter.detect_file_type(file_path)
            logger.info("Archivo", f"Tipo detectado: [bold cyan]{file_type.upper()}[/]")

            if file_type == 'unknown':
                ext = os.path.splitext(file_path)[1]
                logger.error("Archivo", f"Formato no soportado: {ext}")
                QMessageBox.warning(
                    self.view, "Formato no soportado",
                    f"El formato '{ext}' no es soportado.\n\n"
                    "Formatos válidos: .md, .docx"
                )
                self.view.show_status("Formato no soportado", 3000)
                return

            # Validación: archivo no vacío
            if os.path.getsize(file_path) == 0:
                logger.warning("Archivo", "El archivo seleccionado está vacío.")
                QMessageBox.warning(
                    self.view, "Archivo vacío",
                    "El archivo seleccionado está vacío."
                )
                self.view.show_status("Archivo vacío", 3000)
                return

            # Detección y preparación (conversión .docx si es necesario)
            logger.info("Archivo", f"Preparando documento [dim]({os.path.basename(file_path)})[/]...")
            success, md_path, media_dir = self.converter.detect_and_prepare(file_path)

            if not success:
                logger.error("Docx", f"No se pudo convertir el archivo .docx: {os.path.basename(file_path)}")
                QMessageBox.critical(
                    self.view, "Error de conversión DOCX",
                    f"No se pudo convertir el archivo: {os.path.basename(file_path)}\n\n"
                    "Para abrir archivos .docx se recomienda tener Pandoc instalado:\n"
                    + ("choco install pandoc  o  winget install --id JohnMacFarlane.Pandoc" if platform.system() == 'Windows' else "brew install pandoc")
                )
                self.view.show_status("Error al abrir archivo", 3000)
                return

            # Guardar referencias para limpieza posterior
            self._temp_md_path = md_path if media_dir else None
            self._temp_media_dir = media_dir

            # Leer el contenido del .md
            logger.info("Archivo", f"Leyendo contenido Markdown: [dim]{md_path}[/]")
            try:
                with open(md_path, "r", encoding="utf-8") as f:
                    md_text = f.read()
            except UnicodeDecodeError:
                # Intentar con encoding latino como fallback
                with open(md_path, "r", encoding="latin-1") as f:
                    md_text = f.read()
            
            if not md_text.strip():
                logger.warning("Archivo", "El archivo convertido no contiene texto.")
                QMessageBox.warning(
                    self.view, "Archivo vacío",
                    "El archivo convertido no contiene texto."
                )
                self.view.show_status("Archivo vacío", 3000)
                return

            # Cambiar el directorio de trabajo al directorio del .md
            # para que las rutas relativas de imágenes funcionen
            md_dir = os.path.dirname(os.path.abspath(md_path))
            if os.path.isdir(md_dir):
                os.chdir(md_dir)
                logger.debug("Archivo", f"Directorio de trabajo (CWD) cambiado a: [dim]{md_dir}[/]")

            # Validar resolución de imágenes (no crítico, solo warnings)
            try:
                warnings = self.converter.validate_images(md_text, md_dir)
                if warnings:
                    warning_text = "\n".join(warnings)
                    logger.warning("Imágenes", f"⚠️ {len(warnings)} imagen(es) de baja resolución:\n{warning_text}")
                    self.view.show_status(f"⚠️ {len(warnings)} imagen(es) de baja resolución", 5000)
            except Exception as img_err:
                logger.debug("Imágenes", f"Validación de imágenes ignorada: {img_err}")

            # Cargar en el editor
            self.view.editor.setPlainText(md_text)
            self.current_file_path = file_path if file_type == 'md' else None
            
            # Registrar watcher
            if self.current_file_path:
                if self.file_watcher.files():
                    self.file_watcher.removePaths(self.file_watcher.files())
                self.file_watcher.addPath(self.current_file_path)
            recovery = self.recovery.load_if_newer(self.current_file_path or 'unsaved.md')
            if recovery and QMessageBox.question(self.view, 'Recuperar cambios', 'Se encontró una recuperación más reciente. ¿Restaurarla?') == QMessageBox.StandardButton.Yes:
                self.view.editor.setPlainText(recovery['text'])

            source_type = "DOCX (Pandoc)" if media_dir else "Markdown"
            self.view.show_status(
                f"Archivo cargado: {os.path.basename(file_path)} [{source_type}]", 5000
            )
            logger.success("Archivo", f"Cargado exitosamente en el editor [bold green]\\[{source_type}][/]")

        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.error("Archivo", f"ERROR CRÍTICO: {e}")
            try:
                QMessageBox.critical(
                    self.view, "Error al abrir archivo",
                    f"Ocurrió un error inesperado al abrir el archivo.\n\n"
                    f"Detalle: {str(e)}\n\n"
                    f"Puede intentar abrir otro archivo."
                )
            except Exception:
                pass
            self.view.show_status("Error al abrir archivo", 3000)

    def _export_docx(self, target_path: str, text: str):
        """Export through Pandoc when available; it preserves Markdown semantics.

        Pandoc is already the project's DOCX import dependency, so no new Python
        package is introduced.  A clear message is shown rather than silently
        emitting a malformed .docx when it is not installed.
        """
        if not target_path.lower().endswith('.docx'):
            target_path += '.docx'
        pandoc = shutil.which('pandoc')
        if not pandoc:
            QMessageBox.warning(self.view, 'Pandoc no disponible', 'Para exportar Word instalá Pandoc:\n\n' + ('choco install pandoc  o  winget install --id JohnMacFarlane.Pandoc' if platform.system() == 'Windows' else 'brew install pandoc'))
            return
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.md', mode='w', encoding='utf-8') as source:
                source.write(text); source_path = source.name
            import subprocess
            result = subprocess.run([pandoc, source_path, '-o', target_path], capture_output=True, text=True)
            os.remove(source_path)
            if result.returncode:
                raise RuntimeError(result.stderr.strip() or 'Pandoc no pudo generar el archivo.')
            self.view.show_status('Documento Word exportado', 3000)
            QMessageBox.information(self.view, 'Éxito', 'Documento Word exportado correctamente.')
        except Exception as exc:
            QMessageBox.critical(self.view, 'Error al exportar Word', str(exc))

    def _on_export_requested(self):
        try:
            text = self.view.editor.toPlainText()
            if not text.strip():
                QMessageBox.warning(self.view, "Error", "El documento está vacío.")
                return
                
            options = self.view.get_current_options()
            pdf_path, selected_filter = QFileDialog.getSaveFileName(
                self.view, "Exportar documento", "", "PDF (*.pdf);;Word (*.docx)"
            )
            if not pdf_path:
                return
                
            if selected_filter.startswith('Word') or pdf_path.lower().endswith('.docx'):
                self._export_docx(pdf_path, text)
                return
            if not pdf_path.lower().endswith('.pdf'): pdf_path += '.pdf'

            # Construir footer_text desde la configuración de página
            footer_parts = []
            if self._page_data.get('footer_left'):
                footer_parts.append(self._page_data['footer_left'])
            if self._page_data.get('footer_center'):
                footer_parts.append(self._page_data['footer_center'])
            if self._page_data.get('footer_right'):
                footer_parts.append(self._page_data['footer_right'])
            footer_text = ' | '.join(footer_parts)

            self.view.show_status("Generando PDF...")
            logger.info("PDF", f"Iniciando exportación a: [underline]{pdf_path}[/]")
            
            # Generar HTML para exportación (sin scripts de preview)
            html = self.model.render_html(
                md_text=text,
                theme_key=options['theme'],
                show_cover=self._cover_data.get('show_cover', False),
                title=self._cover_data.get('title', ''),
                subtitle=self._cover_data.get('subtitle', ''),
                materia=self._cover_data.get('materia', ''),
                integrantes=self._cover_data.get('integrantes', ''),
                profesores=self._cover_data.get('profesores', ''),
                show_logo=self._cover_data.get('show_logo', False),
                logo_position=self._cover_data.get('logo_position', 'top-left'),
                cover_style=self._cover_data.get('cover_style', 'folio'),
                is_preview=False
            )
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8") as tmp:
                tmp.write(html)
                tmp_path = tmp.name

            try:
                success, engine = self.facade.export_to_pdf(tmp_path, pdf_path, footer_text)
                if success:
                    QMessageBox.information(self.view, "Éxito", f"PDF generado exitosamente usando {engine}.")
                    self.view.show_status("Exportación exitosa", 3000)
                    logger.success("PDF", f"PDF generado exitosamente usando [bold green]{engine}[/]")
                    
                    # Limpiar temporales de conversión .docx si existen
                    if self._temp_md_path or self._temp_media_dir:
                        DocxConverter.cleanup_temp_files(self._temp_md_path, self._temp_media_dir)
                        self._temp_md_path = None
                        self._temp_media_dir = None
                else:
                    logger.error("PDF", "El motor de exportación no pudo generar el PDF.")
                    QMessageBox.critical(self.view, "Error", "No se pudo generar el PDF.")
                    self.view.show_status("Error en exportación", 3000)
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.error("PDF", f"ERROR CRÍTICO al exportar PDF: {e}")
            try:
                QMessageBox.critical(
                    self.view, "Error de exportación",
                    f"Ocurrió un error inesperado al exportar.\n\n"
                    f"Detalle: {str(e)}"
                )
            except Exception:
                pass
            self.view.show_status("Error en exportación", 3000)
