# Pruebas de Matemáticas y Tablas Complejas

Este documento sirve para verificar cómo renderiza el sistema las fórmulas de LaTeX y las tablas con múltiples columnas y saltos de página.

---

## 1. Fórmulas de LaTeX

### 1.1 Fórmulas en línea (Inline Math)
La famosa identidad de Euler es $e^{i\pi} + 1 = 0$, la cual relaciona cinco de las constantes más importantes.
El límite clásico $\lim_{x \to 0} \frac{\sin x}{x} = 1$ es la base de las derivadas trigonométricas.
También podemos escribir ecuaciones sencillas en línea como $a^2 + b^2 = c^2$ o integrales como $\int_a^b f(x) dx$.

### 1.2 Fórmulas en bloque (Display Math)
La transformada de Fourier continua en bloque:

$$
\hat{f}(\xi) = \int_{-\infty}^{\infty} f(x) e^{-2\pi i x \xi} dx
$$

Ecuaciones de Maxwell en forma diferencial:

$$
\begin{aligned}
\nabla \cdot \mathbf{E} &= \frac{\rho}{\varepsilon_0} \\
\nabla \cdot \mathbf{B} &= 0 \\
\nabla \times \mathbf{E} &= -\frac{\partial \mathbf{B}}{\partial t} \\
\nabla \times \mathbf{B} &= \mu_0 \left(\mathbf{J} + \varepsilon_0 \frac{\partial \mathbf{E}}{\partial t}\right)
\end{aligned}
$$

Y matrices matemáticas complejas:

$$
A = \begin{pmatrix}
a_{11} & a_{12} & \cdots & a_{1n} \\
a_{21} & a_{22} & \cdots & a_{2n} \\
\vdots & \vdots & \ddots & \vdots \\
a_{m1} & a_{m2} & \cdots & a_{mn}
\end{pmatrix}
$$

---

## 2. Tablas de Datos

### 2.1 Tabla con alineación y formato
Esta tabla evalúa cómo se comportan las celdas con alineaciones personalizadas (izquierda, centro, derecha) y estilos tipográficos internos.

| ID | Nombre del Componente | Estado | Versión | Notas Adicionales |
| :--- | :---: | :---: | ---: | :--- |
| **001** | Renderizador PDF | `Estable` | *v1.2.0* | Funciona usando Puppeteer y Weasyprint como fallback. |
| **002** | Motor KaTeX | `Activo` | *v0.16.11* | Soporta renderizado tanto en el servidor como en el cliente. |
| **003** | Interfaz Gráfica | `Pruebas` | *v0.9.5* | Implementada con PyQt6 y WebEngineView. |
| **004** | Parser de Listas | `Fijo` | *v1.0.1* | Ahora respeta sangrías y evita cortes huérfanos. |

### 2.2 Tabla ancha de datos técnicos
Una tabla con múltiples columnas para comprobar que los márgenes laterales se respetan y el texto se ajusta correctamente sin salirse del área imprimible de la hoja A4.

| Variable | Tipo | Valor por Defecto | Rango | Descripción Detallada | Impacto |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `page_height` | `float` | `297.0` | `100.0 - 500.0` | Representa la altura total de la página en milímetros (A4 estándar). | Alto |
| `page_width` | `float` | `210.0` | `100.0 - 500.0` | Representa el ancho total de la página en milímetros (A4 estándar). | Alto |
| `margin_top` | `float` | `22.0` | `0.0 - 50.0` | Margen superior utilizado en las hojas de estilo de impresión. | Medio |
| `margin_bottom`| `float` | `22.0` | `0.0 - 50.0` | Margen inferior utilizado en las hojas de estilo de impresión. | Medio |
| `line_height` | `float` | `1.25` | `1.0 - 2.0` | Altura entre las líneas de los bloques de código y textos. | Bajo |

---

## 3. Listas Anidadas Complejas

* Elemento Nivel 1 (A)
    * Elemento Nivel 2 (A.1)
        * Elemento Nivel 3 (A.1.1)
            * Elemento Nivel 4 (A.1.1.1)
    * Elemento Nivel 2 (A.2)
* Elemento Nivel 1 (B)
    * Elemento Nivel 2 (B.1)
        * Elemento Nivel 3 (B.1.1)
        * Elemento Nivel 3 (B.1.2)
