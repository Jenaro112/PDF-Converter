# 📄 PDF Converter — Editor Markdown & Exportador IDE

**PDF Converter** es una aplicación de escritorio moderna desarrollada en **Python (PyQt6)** que permite redactar, editar, importar, previsualizar en tiempo real y exportar documentos **Markdown (.md)** y **Microsoft Word (.docx)** a **PDF de alta fidelidad** con calidad de imprenta.

Diseñado con un enfoque de arquitectura limpia (**MVC + Facade**) y optimizado para una excelente experiencia de usuario (UX/UI) tanto en **Windows** como en **macOS**.

---

## ✨ Características Principales

- 🎨 **Interfaz Dark Mode Premium & Cross-Platform**: Entorno gráfico moderno con estilos desacoplados y soporte nativo completo para Windows y macOS.
- ⚡ **Vista Previa A4 en Tiempo Real**: Visualización en vivo paginada (`QWebEngineView`) con preservación inteligente de scroll mientras editás.
- 📐 **Diagramas Mermaid con Alineación Perfecta**: Integración con `mmdc`, motor Flexbox centrado y post-procesado matemático SVG para que cajas y textos encajen perfectamente.
- 🧮 **Fórmulas Matemáticas KaTeX**: Soporte completo para ecuaciones inline (`$...$`) y en bloque (`$$...$$`).
- 🎨 **6 Temas Visuales Exclusivos**:
  - ✦ *Minimalista Moderno*
  - 📜 *Académico Clásico*
  - 🏛 *Institucional*
  - 📰 *Editorial Moderno*
  - ⚙️ *Técnico Claro*
  - 🎨 *Cuadernillo Pastel*
- 📖 **Generador Configurable de Portadas**:
  - Formulario modal interactivo.
  - 5 estilos de portada (Banda Izquierda, Académica Clásica, Corporativa, Bloque Superior, Elegancia).
  - Configuración de logo institucional, título, subtítulo, materia, autores y docentes.
- 🖍 **Resaltado Pastel de Texto**: Marcación dinámica en vivo (`==texto==(color)`) con selector visual de paleta pastel y colores personalizados.
- 🔄 **Soporte Bidireccional DOCX**: Importación automática de archivos `.docx` a Markdown estructurado y exportación a Word mediante Pandoc.
- 📤 **Motor de Exportación PDF Lossless (Facade)**:
  - **Puppeteer (Node.js)** como motor principal con renderizado vectorial perfecto y numeración dinámica de páginas.
  - **WeasyPrint** como fallback transparente.
- 📑 **Control de Saltos de Página**: Manejo manual y limpio mediante `<!-- PAGEBREAK -->`.
- 💾 **Recuperación Automática (Autosave)**: Snapshots automáticos de respaldo cada 45 segundos para prevenir pérdida de datos.
- 🖼 **Gestión Inteligente de Imágenes**: Pegado directo de imágenes desde el portapapeles con guardado automático en `<documento>_img/` y limpieza de imágenes huérfanas.

---

## 🏗 Arquitectura del Sistema (MVC + Facade)

El proyecto está estructurado bajo el patrón de diseño **Model-View-Controller (MVC)** desacoplado, utilizando una **Facade** para abstraer el motor de exportación a PDF.

```text
PDF-Converter/
├── assets/                       # Recursos estáticos (Logos, fuentes)
├── docs/                         # Documentación de soporte y guías
├── src/
│   ├── main.py                   # Punto de entrada de la aplicación
│   ├── facade/
│   │   └── pdf_exporter.py       # Facade de exportación PDF (Puppeteer / WeasyPrint)
│   ├── mvc/
│   │   ├── controllers/
│   │   │   └── app_controller.py # Controlador principal, hilos de renderizado y lógica de estado
│   │   ├── models/
│   │   │   ├── document.py       # Procesador Markdown, Mermaid, Pygments y HTML
│   │   │   ├── docx_converter.py # Conversor bidireccional DOCX (Pandoc)
│   │   │   ├── recovery.py       # Gestor de snapshots y recuperación de emergencia
│   │   │   └── theme_manager.py  # Definición y variables CSS de los 6 temas
│   │   └── views/
│   │       ├── main_window.py    # Ventana principal, Toolbar, Splitter y paneles
│   │       ├── editor_panel.py   # Editor de código Markdown con números de línea (Gutter)
│   │       ├── preview_panel.py  # Panel QWebEngineView con preservación de scroll
│   │       ├── cover_dialog.py   # Modal interactivo de configuración de portadas
│   │       └── markdown_highlighter.py # Resaltador de sintaxis Markdown en vivo
│   └── scripts/
│       └── pdf.mjs               # Script ejecutable de Puppeteer para conversión PDF
├── tests_y_ejemplos/             # Archivos Markdown y PDF de prueba
├── .env.example                  # Variables de entorno de plantilla
├── package.json                  # Dependencias de Node.js (Puppeteer)
└── requirements.txt              # Dependencias de Python
```

---

## 🚀 Requisitos e Instalación

### Prerrequisitos

1. **Python 3.10+**
2. **Node.js 18+** (necesario para la generación de PDF vía Puppeteer)
3. *(Opcional)* **Pandoc**: Necesario para la importación y exportación de archivos `.docx`.
   - Windows: `winget install --id JohnMacFarlane.Pandoc` o `choco install pandoc`
   - macOS: `brew install pandoc`

---

### Pasos de Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/Jenaro112/PDF-Converter.git
   cd PDF-Converter
   ```

2. **Crear y activar un entorno virtual Python**:
   - **Windows**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **macOS / Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Instalar dependencias de Python**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Instalar dependencias de Node.js (Puppeteer)**:
   ```bash
   npm install
   ```

---

## 💻 Uso de la Aplicación

Para iniciar el editor:

```bash
python src/main.py
```

### Atajos de Teclado (Shortcuts)

| Acción | macOS | Windows / Linux |
| :--- | :--- | :--- |
| **Buscar / Reemplazar** | `⌘ + F` | `Ctrl + F` |
| **Negrita** | `⌘ + B` | `Ctrl + B` |
| **Cursiva** | `⌘ + I` | `Ctrl + I` |
| **Insertar Enlace** | `⌘ + K` | `Ctrl + K` |
| **Resaltar Texto** | `⌘ + Shift + H` | `Ctrl + Shift + H` |
| **Guardar Documento** | `⌘ + S` | `Ctrl + S` |

---

## 🛠 Tecnologías Utilizadas

- **Lenguaje**: Python 3.10+
- **GUI Framework**: PyQt6 / PyQt6-WebEngine
- **Procesamiento Markdown**: `markdown`, `pymdown-extensions`, `pygments`
- **Generación PDF**: Node.js + Puppeteer (con WeasyPrint como fallback)
- **Conversión DOCX**: Pandoc
- **Iconografía y Estilos**: CSS3 personalizado inyectado dinámicamente

---

## 📄 Licencia

Este proyecto fue desarrollado bajo la licencia MIT.
