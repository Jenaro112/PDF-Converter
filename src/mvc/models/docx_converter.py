import os
import re
import subprocess
import platform
import shutil
from pathlib import Path
from typing import Optional

_IS_WINDOWS = platform.system() == 'Windows'


class DocxConverter:
    """
    Maneja la conversión automática de archivos .docx a .md usando Pandoc,
    la validación de resolución de imágenes, y la limpieza de temporales.
    """

    # Resolución mínima recomendada (en píxeles por lado)
    LOW_RES_THRESHOLD = 150  # Imágenes menores a 150px en cualquier dimensión

    @staticmethod
    def is_pandoc_available() -> bool:
        """Verifica si Pandoc está instalado y accesible."""
        try:
            result = subprocess.run(
                ["pandoc", "--version"],
                capture_output=True, text=True,
                shell=_IS_WINDOWS
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False

    @staticmethod
    def detect_file_type(input_path: str) -> str:
        """
        Detecta el tipo de archivo por extensión.
        Returns: 'docx', 'md', o 'unknown'
        """
        ext = Path(input_path).suffix.lower()
        if ext == '.docx':
            return 'docx'
        elif ext == '.md':
            return 'md'
        return 'unknown'

    def convert_docx_to_md(self, docx_path: str) -> tuple[bool, str, str]:
        """
        Convierte un .docx a .md extrayendo imágenes y estructurando encabezados y saltos.

        Args:
            docx_path: Ruta absoluta al archivo .docx

        Returns:
            (éxito, ruta_md_temporal, ruta_carpeta_media)
        """
        docx_path = os.path.abspath(docx_path)
        if not os.path.exists(docx_path):
            return False, "", ""

        base_name = Path(docx_path).stem
        parent_dir = str(Path(docx_path).parent)
        media_dir = os.path.join(parent_dir, f"media_{base_name}")
        temp_md = os.path.join(parent_dir, f"_temp_{base_name}.md")

        pandoc_success = False
        if self.is_pandoc_available():
            try:
                result = subprocess.run(
                    [
                        "pandoc",
                        docx_path,
                        "-o", temp_md,
                        f"--extract-media=media_{base_name}",
                        "--wrap=none"
                    ],
                    capture_output=True, text=True,
                    cwd=parent_dir,
                    shell=_IS_WINDOWS  # En Windows, pandoc puede necesitar shell=True
                )
                if result.returncode == 0 and os.path.exists(temp_md):
                    pandoc_success = True
                else:
                    print(f"[Pandoc Error] {result.stderr}")
            except Exception as e:
                print(f"[Pandoc Exception] {e}")

        # Fallback a Mammoth / python-docx si Pandoc falló o no está instalado
        if not pandoc_success:
            print("[DocxConverter] Probando fallback de conversión con Mammoth / python-docx...")
            converted_text = self._convert_with_fallback(docx_path, temp_md, media_dir)
            if not converted_text:
                return False, "", ""
        else:
            with open(temp_md, "r", encoding="utf-8") as f:
                converted_text = f.read()

        # Post-procesado obligatorio: mapear encabezados, inferir si no existen e insertar ---PAGEBREAK--- antes de H1/H2
        final_md = self.post_process_docx_markdown(converted_text)

        # Sobrescribir temp_md con el Markdown estructurado procesado
        with open(temp_md, "w", encoding="utf-8") as f:
            f.write(final_md)

        return True, temp_md, media_dir

    def _convert_with_fallback(self, docx_path: str, temp_md: str, media_dir: str) -> Optional[str]:
        """Intenta convertir usando mammoth o python-docx si Pandoc no está disponible."""
        # 1. Probar Mammoth
        try:
            import mammoth
            with open(docx_path, "rb") as docx_file:
                result = mammoth.convert_to_markdown(docx_file)
                return result.value
        except ImportError:
            pass

        # 2. Probar python-docx
        try:
            import docx
            doc = docx.Document(docx_path)
            lines = []
            for p in doc.paragraphs:
                text = p.text.strip()
                if not text:
                    continue
                style_name = (p.style.name if p.style else "").lower()
                if "heading 1" in style_name or "título 1" in style_name:
                    lines.append(f"# {text}")
                elif "heading 2" in style_name or "título 2" in style_name:
                    lines.append(f"## {text}")
                elif "heading 3" in style_name or "título 3" in style_name:
                    lines.append(f"### {text}")
                elif "heading" in style_name or "título" in style_name:
                    lines.append(f"## {text}")
                else:
                    lines.append(text)
            return "\n\n".join(lines)
        except ImportError:
            pass

        print("[Error] No se encontró Pandoc, Mammoth ni python-docx para convertir el archivo .docx")
        return None

    @staticmethod
    def post_process_docx_markdown(md_text: str) -> str:
        """
        Post-procesa el Markdown generado desde un .docx:
        1. Limpia atributos de Pandoc ({...}).
        2. Detecta e infiere encabezados si el .docx no usaba estilos de Word.
        3. NO inserta saltos de página automáticos (los saltos son 100% manuales).
        """
        if not md_text:
            return ""

        # 1. Limpiar atributos de Pandoc/Word ({width=...}, {.underline}, etc.)
        md_text = re.sub(r'(!\[[^\]]*\]\([^)]*\))\s*\{[^}]*\}', r'\1', md_text)
        md_text = re.sub(r'\[([^\]]*)\]\{[^}]*\}', r'\1', md_text)
        md_text = re.sub(r'^(#{1,6}\s+.*?)\s*\{[^}]*\}\s*$', r'\1', md_text, flags=re.MULTILINE)
        md_text = re.sub(r'^\s*\{[^}]*\}\s*$', '', md_text, flags=re.MULTILINE)

        # 2. Fallback: Si no hay encabezados # o ## en el documento, inferir patrones comunes
        has_headings = bool(re.search(r'^\s*#{1,3}\s+\S+', md_text, re.MULTILINE))
        if not has_headings:
            print("[DocxConverter] No se detectaron estilos Heading en el .docx. Aplicando inferencia de títulos...")
            lines = md_text.split('\n')
            new_lines = []
            for line in lines:
                stripped = line.strip()
                # Detectar líneas en negrita solas como títulos: **Punto 1** -> ## Punto 1
                m_bold = re.match(r'^\*\*(.*?)\*\*$', stripped)
                if m_bold and len(m_bold.group(1).strip()) < 80:
                    title_text = m_bold.group(1).strip()
                    new_lines.append(f"\n## {title_text}\n")
                    continue

                # Detectar patrones numéricos o palabras clave: Punto 1, Capítulo 1, Ejercicio 1, etc.
                m_pattern = re.match(r'^(Punto|Capítulo|Sección|Unidad|Ejercicio|Parte|Tema)\s+\d+[:\.\s].*$', stripped, re.IGNORECASE)
                if m_pattern and len(stripped) < 100:
                    new_lines.append(f"\n# {stripped}\n")
                    continue

                new_lines.append(line)
            md_text = '\n'.join(new_lines)

        # Limpiar saltos de línea repetidos excesivos
        result_text = re.sub(r'\n{3,}', '\n\n', md_text)

        return result_text.strip()

    def detect_and_prepare(self, input_path: str) -> tuple[bool, str, Optional[str]]:
        """
        Detecta el tipo de archivo y prepara el .md para el pipeline.

        Args:
            input_path: Ruta al archivo de entrada (.md o .docx)

        Returns:
            (éxito, ruta_md, ruta_media_o_None)
            - Si es .md: retorna la ruta directa, media=None
            - Si es .docx: convierte y retorna la ruta temporal, media=carpeta
        """
        file_type = self.detect_file_type(input_path)

        if file_type == 'md':
            return True, os.path.abspath(input_path), None

        elif file_type == 'docx':
            return self.convert_docx_to_md(input_path)

        else:
            print(f"[Error] Tipo de archivo no soportado: {Path(input_path).suffix}")
            return False, "", None

    def validate_images(self, md_text: str, base_dir: str) -> list[str]:
        """
        Escanea las imágenes referenciadas en el Markdown y genera
        warnings para imágenes de baja resolución.

        Usa PIL/Pillow si está disponible, si no, omite la validación
        sin bloquear el pipeline.

        Args:
            md_text: Contenido del archivo Markdown
            base_dir: Directorio base para resolver rutas relativas

        Returns:
            Lista de mensajes de advertencia
        """
        warnings = []

        # Buscar referencias a imágenes: ![alt](path)
        image_refs = re.findall(r'!\[.*?\]\(([^)]+)\)', md_text)
        # También buscar <img src="...">
        image_refs += re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', md_text)

        try:
            from PIL import Image
            has_pil = True
        except ImportError:
            has_pil = False

        for ref in image_refs:
            # Ignorar URLs web y data URIs
            if ref.startswith(('http://', 'https://', 'data:')):
                continue

            # Resolver ruta absoluta
            if ref.startswith('file://'):
                img_path = ref.replace('file://', '')
            elif os.path.isabs(ref):
                img_path = ref
            else:
                img_path = os.path.normpath(os.path.join(base_dir, ref))

            if not os.path.exists(img_path):
                warnings.append(f"⚠️ Imagen no encontrada: {ref}")
                continue

            if not has_pil:
                continue

            try:
                with Image.open(img_path) as img:
                    w, h = img.size
                    if w < self.LOW_RES_THRESHOLD or h < self.LOW_RES_THRESHOLD:
                        warnings.append(
                            f"⚠️ Imagen de baja resolución detectada ({w}x{h}): "
                            f"{os.path.basename(img_path)}. "
                            f"Se recomienda usar una versión original."
                        )
            except Exception:
                # No bloquear por errores de lectura de imagen
                pass

        return warnings

    @staticmethod
    def cleanup_temp_files(temp_md: Optional[str], media_dir: Optional[str]):
        """
        Limpia archivos temporales generados por la conversión.

        Args:
            temp_md: Ruta al .md temporal (None = no borrar)
            media_dir: Ruta a la carpeta media (None = no borrar)
        """
        if temp_md and os.path.exists(temp_md):
            try:
                os.remove(temp_md)
            except OSError:
                pass

        if media_dir and os.path.isdir(media_dir):
            try:
                shutil.rmtree(media_dir)
            except OSError:
                pass
