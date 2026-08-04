# Documentación Técnica y Contexto del Proyecto: PDF Converter

> **Propósito de este archivo**: Este documento provee el contexto completo del sistema para que cualquier Inteligencia Artificial o desarrollador entienda la arquitectura, el flujo de procesamiento de datos, las decisiones de diseño y las reglas de funcionamiento del proyecto. Debe actualizarse ante cualquier cambio estructural significativo.

---

## 📌 Visión General del Proyecto

**PDF Converter** es una aplicación de escritorio desarrollada en **Python (PyQt6)** que permite redactar, importar, previsualizar en tiempo real y exportar documentos **Markdown (.md)** y **Microsoft Word (.docx)** a **PDF de alta calidad**.

### Características Principales:
* **Entorno Gráfico PyQt6**: Editor de texto Markdown a la izquierda y vista previa interactiva paginada a la derecha (`QWebEngineView`).
* **Alineación Flexbox Centrada + Expansión Simétrica en Mermaid (Fix Definitivo)**:
  * Conversión del contenedor interno `display: table-cell;` de Mermaid a `display: flex !important; align-items: center !important; justify-content: center !important; width: 100% !important; text-align: center !important;`.
  * Post-procesado matemático automático del SVG generado por `mmdc`: se aplica una expansión del 1.6x sobre el ancho `width` de `<foreignObject>` y se recalcula simétricamente su posición `transform="translate(-new_w/2, ...)"`.
  * Garantiza alineación 100% centrada (horizontal y vertical) de todos los textos ("Inicio de Proceso", "¿Hay Memoria Libre?", etc.) dentro de sus respectivas cajas.
  * Embebido de fuentes `.woff2` como Data URIs base64 (`data:font/woff2;base64,...`) dentro del CSS temporal inyectado a `mmdc` (`-C theme.css`).
  * Reglas CSS de `mmdc` delimitadas estrictamente a los selectores `svg, svg *`, impidiendo cualquier filtración hacia las fuentes del documento principal, código o KaTeX.
  * Caché v9 por hash MD5 (`v9:{theme_key}:{mermaid_code}`).
* **Preservación de Estilos de Tabla y Código**:
  * Encabezados de tabla (`th`) estilizados exclusivamente mediante `var(--table-header-bg)` y `var(--table-header-fg)` de cada tema para garantizar alto contraste y legibilidad.
  * Bloques de código e inline code delimitados a `'JetBrains Mono', monospace`.
  * Ecuaciones KaTeX delimitadas a `KaTeX_Main, serif`.
* **Fondo Full-Bleed de Tema + Márgenes Homogéneos de 20mm**:
  * Paginación en tarjetas `.page` A4 (`210mm x 297mm`) con `padding: 20mm` y `background-color: var(--page-bg)` tanto en la vista previa como en el PDF exportado.
  * `@page { size: A4; margin: 0; }` imprime cada tarjeta sin margen blanco exterior, logrando un fondo full-bleed continuo en los 4 lados de todas las páginas.
* **Unicidad Estricta de Salto por Marcador**: Marcadores `<!-- PAGEBREAK -->` aplican exclusivamente `break-after: page !important;`.
* **Depuración y Colapso de Hojas en Blanco**: Eliminación de saltos de página redundantes mediante `_clean_redundant_pagebreaks`.
* **Sincronización Dinámica de Paginación A4**: Medición dinámica de altura exacta tras la carga de fuentes (`document.fonts.ready`).
* **Resaltado Sintáctico Dinámico por Tema (Pygments)**: Bloques de código con coloración por tokens.
* **Preservación de Scroll en Tiempo Real**: Vista previa sincronizada sin salto de scroll al editar.
* **Soporte Completo de DOCX**: Conversión automática de archivos `.docx` a Markdown estructurado.
* **Control de Saltos de Página 100% Manual**: Gobernados por `<!-- PAGEBREAK -->`.
* **Configuración Estructurada de Portada con Logo**: Formulario `CoverDialog` con posición de logo.
* **Resaltado de Texto Pastel con Swatches Visuales (`==texto==(color)`)**: `QIcon` nativos en toolbar.
* **Sistema de 6 Temas CSS Dinámicos (Claros) y Estilos Pygments**: `minimal`, `classic`, `institutional`, `editorial`, `blueprint`, `pastel`.
* **Cuatro portadas cromáticas**: Minimalista, Académica, Tipográfica y Orgánica. Todas incluyen la misma variante opcional de logo institucional.
* **Soporte para Fórmulas Matemáticas**: KaTeX integrado (`$...$` y `$$...$$`).
* **Edición y recuperación**: búsqueda/reemplazo, atajos centralizados para macOS, índice lateral, snapshots de recuperación cada 45 segundos e inserción de imágenes pegadas en una carpeta `<documento>_img/`.
* **Exportación ampliada**: PDF con pie configurable y número de página, y `.docx` mediante Pandoc. Pandoc debe estar instalado (`brew install pandoc`) para conversión DOCX en ambos sentidos.
* **Herramientas de estudio**: índice de resaltados por color y tabla de contenidos activada con `<!-- TOC -->`, cuyos enlaces y páginas se calculan después de la paginación del navegador.

---

## 🏗 Arquitectura del Sistema (Patrón MVC + Facade)

El proyecto sigue una arquitectura **Model-View-Controller (MVC)** desacoplada con el patrón **Facade** para el motor de exportación PDF.

```text
src/
├── main.py                          # Punto de entrada de la aplicación
├── mvc/
│   ├── controllers/
│   │   └── app_controller.py        # Controlador principal, estado de portada e hilos
│   ├── models/
│   │   ├── document.py              # Procesador Markdown, Mermaid con alineación Flexbox centrada, Pygments y CSS
│   │   ├── docx_converter.py        # Conversor de DOCX (Pandoc/Mammoth) y post-procesado
│   │   └── theme_manager.py         # Definición de 6 temas CSS y pygments_style
│   └── views/
│       ├── main_window.py           # Toolbar con QIcon color swatches, Editor y Status
│       ├── cover_dialog.py          # Modal QDialog para portada y posición de logo
│       └── preview_panel.py          # Panel QWebEngineView con preservación de scroll y file://
├── facade/
│   └── pdf_exporter.py              # Facade de exportación PDF (Puppeteer / WeasyPrint)
└── scripts/
    └── pdf.mjs                      # Script ejecutable de Puppeteer (Node.js)
```

---

## 📋 Directivas para la Generación de Prompts e Integración con Otras IA

Cualquier IA que genere código o prompts para este proyecto debe seguir estas directivas estrictamente:

1. **Post-procesado y Centrado Flexbox en Mermaid**: Mantener el reemplazo de `display: table-cell;` por Flexbox centrado en `_process_mermaid_diagrams` junto a `_expand_fo` para garantizar textos completos y 100% centrados.
2. **Aislamiento de CSS en Mermaid**: Las fuentes y estilos para `mmdc` deben inyectarse exclusivamente mediante Data URIs base64 en un archivo `-C css_file` delimitado a `svg, svg *`.
3. **Tablas y Código**: Mantener `th` asignado a `var(--table-header-bg)` y `var(--table-header-fg)` y código delimitado a `'JetBrains Mono'`.
4. **Full-Bleed y Márgenes PDF**: Mantener la paginación `.page` A4 con `padding: 20mm`, `background-color: var(--page-bg)` y `@page { size: A4; margin: 0; }`.

---
*Última actualización: Julio 2026 — v5.6 (Fix Definitivo de Alineación Flexbox Centrada en Mermaid)*
