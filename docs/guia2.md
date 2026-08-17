¡De una! Para que entrenes fuerte de cara al parcial con ejercicios idénticos a los de la guía oficial del profesor, preparé **4 ejercicios prácticos** basados estrictamente en las guías y exámenes que subiste.

Primero te presento los enunciados para que intentes resolverlos vos solo, y **al final tenés toda la resolución detallada paso a paso** para que puedas verificar tus resultados.

---

# 📝 Enunciados: Ejercicios Prácticos de Parcial

## Ejercicio 1: Asignación Dinámica de Memoria

Un sistema operativo utiliza **particionamiento dinámico** y cuenta con la siguiente configuración de **bloques libres** en orden físico de memoria:

- **Bloque 1 (B1):** 100 KB
- **Bloque 2 (B2):** 200 KB
- **Bloque 3 (B3):** 500 KB
- **Bloque 4 (B4):** 150 KB
- **Bloque 5 (B5):** 300 KB

Llegan de forma secuencial las siguientes peticiones de memoria de procesos:

1. **P1:** 120 KB
2. **P2:** 250 KB
3. **P3:** 90 KB
4. **P4:** 180 KB

**Se pide:**

- **a)** Muestre cómo queda asignada la memoria aplicando el algoritmo de **Primer Ajuste (First-fit)**. Indique el tamaño de los huecos resultantes y la memoria libre total restante.
- **b)** Realice el mismo procedimiento aplicando **Mejor Ajuste (Best-fit)**.
- **c)** Realice el mismo procedimiento aplicando **Peor Ajuste (Worst-fit)**.
- **d)** Indique qué algoritmo deja el **mayor hueco libre disponible** al finalizar toda la asignación.

---

## Ejercicio 2: Dimensionamiento de Páginas y Tablas

Un sistema informático utiliza un esquema de **direccionamiento de 32 bits**. Para dar soporte a un proceso promedio cuyo tamaño en memoria es de **16 MB**, se evalúan tres alternativas de **tamaño de página**:

- **Alternativa A:** 1 KB
- **Alternativa B:** 8 KB
- **Alternativa C:** 64 KB

**Se pide:**

- **a)** Calcule la **cantidad de páginas** requeridas para el proceso promedio en cada una de las tres alternativas.
- **b)** Sabiendo que cada entrada de la tabla de páginas ocupa **4 bytes**, calcule el **tamaño de la tabla de páginas** (en KB o bytes) del proceso para cada alternativa.
- **c)** Justifique cuál de las alternativas elegiría basándose en:
  - La menor fragmentación interna.
  - La menor sobrecarga de espacio para las tablas de páginas.

---

## Ejercicio 3: Traducción de Direcciones Lógicas a Físicas

Un procesador genera **direcciones lógicas de 32 bits** en un sistema con un **tamaño de página de 4 KB** (4.096 bytes) y entradas de tabla de páginas de **4 bytes**.

La **tabla de páginas** activa para el proceso en ejecución es la siguiente:

| Página | Marco (Frame) | Bit de Presencia (Residente) |
| :---: | :---: | :---: |
| **0** | 3 | 1 |
| **1** | 8 | 1 |
| **2** | 1 | 1 |
| **3** | 6 | 0 |
| **4** | 12 | 1 |

**Se pide:**

- **a)** Traduzca las siguientes direcciones lógicas a sus correspondientes **direcciones físicas** reales (muestre el desarrollo matemático):
  - `Dirección I: (0, 1500)`
  - `Dirección II: (1, 4000)`
  - `Dirección III: (4, 2000)`
- **b)** Explique detalladamente qué ocurre a nivel de hardware (MMU) y de sistema operativo al intentar acceder a la dirección lógica **`(3, 500)`**.
- **c)** Calcule la **dirección física inicial** correspondiente al **Marco 8**.

---

## Ejercicio 4: Límites Arquitectónicos del Sistema de Memoria

Un sistema operativo maneja **direcciones lógicas de 32 bits**, un **tamaño de página de 4 KB** (2¹² = 4.096 bytes) y entradas de tabla de páginas de **4 bytes**.

**Se pide:**

- **a)** Calcule el **número máximo de páginas** que puede gestionar un proceso en este sistema.
- **b)** Calcule el **tamaño total de la tabla de páginas** (en MB) requerida si un programa decidiera mapear la totalidad de su espacio de direcciones lógicas de 32 bits.
- **c)** Si el sistema operativo se actualiza para usar un **tamaño de página de 16 KB** (2¹⁴ = 16.384 bytes), calcule la **nueva cantidad máxima de páginas** y el **nuevo tamaño de tabla máximo** (en MB).

---
---

# 🔑 Resolución Detallada Paso a Paso

Aquí tenés los procedimientos matemáticos y lógicos explicados de manera directa para que auto-evalúes tu rendimiento.

## 📌 Solución del Ejercicio 1 (Asignación en KB)

- **Memoria inicial libre total:** `100 + 200 + 500 + 150 + 300 = 1250 KB`
- **Memoria solicitada por procesos:** `120 + 250 + 90 + 180 = 640 KB`
- **Memoria libre total restante al final (igual para todos):** `1250 - 640 = 610 KB`

### a) Primer Ajuste (First-fit)

- **P1 (120 KB):** Recorre desde el inicio. El primer bloque que sirve es **B2 (200 KB)**.
  - *Asignación:* Se ubica en B2.
  - *Residuo:* B2 queda con `200 - 120 = 80 KB` libres.
- **P2 (250 KB):** Recorre desde el inicio. El primer bloque que sirve es **B3 (500 KB)**.
  - *Asignación:* Se ubica en B3.
  - *Residuo:* B3 queda con `500 - 250 = 250 KB` libres.
- **P3 (90 KB):** Recorre desde el inicio. El primer bloque que sirve es **B1 (100 KB)**.
  - *Asignación:* Se ubica en B1.
  - *Residuo:* B1 queda con `100 - 90 = 10 KB` libres.
- **P4 (180 KB):** Recorre desde el inicio. No cabe en B1 (10 KB) ni en B2 (80 KB). Cabe en el residuo de **B3 (250 KB)**.
  - *Asignación:* Se ubica en el residuo de B3.
  - *Residuo:* B3 queda con `250 - 180 = 70 KB` libres.
- **Resultados de First-fit:**
  - *Tamaño de los huecos resultantes:* B1: **10 KB**, B2: **80 KB**, B3: **70 KB**, B4: **150 KB** (intacto), B5: **300 KB** (intacto).
  - *Memoria libre total:* `10 + 80 + 70 + 150 + 300 = 610 KB`.

### b) Mejor Ajuste (Best-fit)

- **P1 (120 KB):** Busca el hueco más cercano a su tamaño. El mejor es **B4 (150 KB)**.
  - *Asignación:* Se ubica en B4.
  - *Residuo:* B4 queda con `150 - 120 = 30 KB` libres.
- **P2 (250 KB):** El bloque libre más ajustado es **B5 (300 KB)**.
  - *Asignación:* Se ubica en B5.
  - *Residuo:* B5 queda con `300 - 250 = 50 KB` libres.
- **P3 (90 KB):** El bloque libre más ajustado es **B1 (100 KB)**.
  - *Asignación:* Se ubica en B1.
  - *Residuo:* B1 queda con `100 - 90 = 10 KB` libres.
- **P4 (180 KB):** El bloque libre más ajustado disponible es **B2 (200 KB)**.
  - *Asignación:* Se ubica en B2.
  - *Residuo:* B2 queda con `200 - 180 = 20 KB` libres.
- **Resultados de Best-fit:**
  - *Tamaño de los huecos resultantes:* B1: **10 KB**, B2: **20 KB**, B3: **500 KB** (intacto), B4: **30 KB**, B5: **50 KB**.
  - *Memoria libre total:* `10 + 20 + 500 + 30 + 50 = 610 KB`.

### c) Peor Ajuste (Worst-fit)

- **P1 (120 KB):** Elige el bloque más grande disponible, que es **B3 (500 KB)**.
  - *Asignación:* Se ubica en B3.
  - *Residuo:* B3 queda con `500 - 120 = 380 KB` libres.
- **P2 (250 KB):** El bloque libre más grande disponible ahora es el residuo de **B3 (380 KB)**.
  - *Asignación:* Se ubica en el residuo de B3.
  - *Residuo:* B3 queda con `380 - 250 = 130 KB` libres.
- **P3 (90 KB):** El bloque libre más grande disponible es **B5 (300 KB)**.
  - *Asignación:* Se ubica en B5.
  - *Residuo:* B5 queda con `300 - 90 = 210 KB` libres.
- **P4 (180 KB):** El bloque libre más grande disponible ahora es el residuo de **B5 (210 KB)**.
  - *Asignación:* Se ubica en el residuo de B5.
  - *Residuo:* B5 queda con `210 - 180 = 30 KB` libres.
- **Resultados de Worst-fit:**
  - *Tamaño de los huecos resultantes:* B1: **100 KB** (intacto), B2: **200 KB** (intacto), B3: **130 KB**, B4: **150 KB** (intacto), B5: **30 KB**.
  - *Memoria libre total:* `100 + 200 + 130 + 150 + 30 = 610 KB`.

### d) Mayor hueco libre disponible

- **Mejor Ajuste (Best-fit)** deja el mayor hueco libre individual: el **Bloque 3 con 500 KB** totalmente intacto.

---

## 📌 Solución del Ejercicio 2 (Cálculos de Páginas y Tablas)

- **Tamaño del proceso:** `16 MB = 16 × 1024 KB = 16.384 KB = 16.777.216 bytes`.

### a) Cantidad de páginas del proceso promedio

- **Alternativa A (1 KB):** `16.384 KB / 1 KB = 16.384 páginas`
- **Alternativa B (8 KB):** `16.384 KB / 8 KB = 2.048 páginas`
- **Alternativa C (64 KB):** `16.384 KB / 64 KB = 256 páginas`

### b) Tamaño de la Tabla de Páginas (Cantidad de páginas × 4 bytes)

- **Alternativa A:** `16.384 entradas × 4 bytes = 65.536 bytes = 64 KB`
- **Alternativa B:** `2.048 entradas × 4 bytes = 8.192 bytes = 8 KB`
- **Alternativa C:** `256 entradas × 4 bytes = 1.024 bytes = 1 KB`

### c) Justificación de Selección

- **Menor fragmentación interna:** Elegiría la **Alternativa A (1 KB)**, porque las páginas de tamaño pequeño minimizan el desperdicio de memoria en el último marco asignado al proceso.
- **Menor sobrecarga de espacio:** Elegiría la **Alternativa C (64 KB)**, ya que a mayor tamaño de página se reduce drásticamente el número de entradas necesarias en la tabla de páginas, minimizando el espacio físico de la RAM consumido por estas tablas.

---

## 📌 Solución del Ejercicio 3 (Traducción Física)

- **Tamaño de página:** `4 KB = 4.096 bytes`.
- **Fórmula general:** `Dirección Física = (Marco × 4096) + Desplazamiento`

### a) Traducciones:

- **`Dirección I: (0, 1500)`**
  - La página 0 está en el Marco 3 con Bit de Presencia 1.
  - `Dir. Física = (3 × 4096) + 1500 = 12288 + 1500 = 13.788`
- **`Dirección II: (1, 4000)`**
  - La página 1 está en el Marco 8 con Bit de Presencia 1.
  - `Dir. Física = (8 × 4096) + 4000 = 32768 + 4000 = 36.768`
- **`Dirección III: (4, 2000)`**
  - La página 4 está en el Marco 12 con Bit de Presencia 1.
  - `Dir. Física = (12 × 4096) + 2000 = 49152 + 2000 = 51.152`

### b) Acceso a `(3, 500)`:

- Al intentar acceder a la Página 3, el hardware (MMU) lee la tabla y detecta que el **Bit de Presencia es 0** (no residente en RAM).
- Esto provoca una excepción de hardware llamada **Fallo de Página (Page Fault)**.
- La CPU se interrumpe y transfiere el control al sistema operativo, el cual debe pausar el proceso, buscar la Página 3 en el disco (región de swap), cargarla en un marco libre de la RAM, actualizar la tabla mapeando la página al marco y seteando el bit de presencia en 1, para finalmente reanudar la instrucción del procesador.

### c) Dirección física inicial del Marco 8:

- `Dirección Física Inicial = 8 × 4096 = 32.768`

---

## 📌 Solución del Ejercicio 4 (Límites de Arquitectura)

### a) Número máximo de páginas de un proceso:

- Espacio de direcciones de 32 bits `= 2³² bytes = 4.294.967.296 bytes (4 GB)`
- Tamaño de página `= 4 KB = 2¹² bytes = 4.096 bytes`
- `Máximo de páginas = 2³² / 2¹² = 2²⁰ = 1.048.576 páginas`

### b) Tamaño de la tabla para todo el espacio lógico de 32 bits:

- `Tamaño tabla = 1.048.576 entradas × 4 bytes = 4.194.304 bytes = 4 MB`

### c) Con tamaño de página de 16 KB (2¹⁴ bytes):

- `Nuevo máximo de páginas = 2³² / 2¹⁴ = 2¹⁸ = 262.144 páginas`
- `Nuevo tamaño de tabla máximo = 262.144 entradas × 4 bytes = 1.048.576 bytes = 1 MB`

---

📊 ¿Querés que simulemos un ejercicio de examen de **algoritmos de reemplazo de páginas** (usando FIFO, LRU o Clock) para completar la preparación práctica?