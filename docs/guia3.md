# Guía Práctica N° 3: Gestión de Memoria y Memoria Virtual

**Materia:** Sistemas Operativos  
**Tema:** Particionamiento Dinámico, Paginación, Traducción de Direcciones y Fragmentación  
**Tipo de Documento:** Guía Práctica de Ejercicios de Examen con Respuestas Detalladas  
**Fecha:** Agosto 2026  

---

# 📝 Enunciados de los Ejercicios Prácticos

---

## 🧱 Bloque A: Algoritmos de Ubicación (Particionamiento Dinámico)

### Ejercicio 1: Asignación con Primer Ajuste (First-fit)

Un sistema operativo utiliza **particionamiento dinámico** y dispone de la siguiente configuración de **bloques libres** en orden físico de memoria:

* **Bloque 1 ($B_1$):** $100\text{ KB}$
* **Bloque 2 ($B_2$):** $500\text{ KB}$
* **Bloque 3 ($B_3$):** $200\text{ KB}$
* **Bloque 4 ($B_4$):** $300\text{ KB}$
* **Bloque 5 ($B_5$):** $600\text{ KB}$

Llegan de forma secuencial las siguientes solicitudes de memoria de procesos:

1. **$P_1$:** $150\text{ KB}$
2. **$P_2$:** $250\text{ KB}$
3. **$P_3$:** $90\text{ KB}$
4. **$P_4$:** $450\text{ KB}$

**Se pide:**

- **a)** Muestre cómo queda asignada la memoria aplicando el algoritmo de ==Primer Ajuste (First-fit)==(celeste).
- **b)** Indique el tamaño de los huecos resultantes en cada bloque.
- **c)** Calcule la memoria libre total restante al finalizar todas las asignaciones.

---

### Ejercicio 2: Asignación con Mejor Ajuste (Best-fit)

Considerando la misma configuración inicial del Ejercicio 1:
* **Bloques libres:** $B_1 = 100\text{ KB}$, $B_2 = 500\text{ KB}$, $B_3 = 200\text{ KB}$, $B_4 = 300\text{ KB}$, $B_5 = 600\text{ KB}$.
* **Peticiones secuenciales:** $P_1 = 150\text{ KB}$, $P_2 = 250\text{ KB}$, $P_3 = 90\text{ KB}$, $P_4 = 450\text{ KB}$.

**Se pide:**

- **a)** Muestre cómo queda asignada la memoria aplicando el algoritmo de ==Mejor Ajuste (Best-fit)==(verde).
- **b)** Detalle el tamaño de los residuos generados en cada uno de los bloques.
- **c)** Indique qué bloque de memoria física permanece intacto (sin ninguna asignación).

---

### Ejercicio 3: Asignación con Peor Ajuste (Worst-fit) y Fragmentación Externa

Considerando la misma configuración inicial del Ejercicio 1:
* **Bloques libres:** $B_1 = 100\text{ KB}$, $B_2 = 500\text{ KB}$, $B_3 = 200\text{ KB}$, $B_4 = 300\text{ KB}$, $B_5 = 600\text{ KB}$.
* **Peticiones secuenciales:** $P_1 = 150\text{ KB}$, $P_2 = 250\text{ KB}$, $P_3 = 90\text{ KB}$, $P_4 = 450\text{ KB}$.

**Se pide:**

- **a)** Desarrolle la asignación paso a paso aplicando el algoritmo de ==Peor Ajuste (Worst-fit)==(naranja).
- **b)** Explique qué ocurre al intentar asignar el proceso $P_4$ ($450\text{ KB}$).
- **c)** Justifique técnicamente por qué este caso evidencia el problema de la ==fragmentación externa==(rojo).

---

### Ejercicio 4: Preservación de Bloques con Best-fit

Un sistema con particionamiento dinámico cuenta con cuatro bloques libres en orden físico:

* **Bloque 1 ($B_1$):** $50\text{ KB}$
* **Bloque 2 ($B_2$):** $150\text{ KB}$
* **Bloque 3 ($B_3$):** $300\text{ KB}$
* **Bloque 4 ($B_4$):** $100\text{ KB}$

Llegan en orden las siguientes peticiones:

1. **$P_1$:** $80\text{ KB}$
2. **$P_2$:** $110\text{ KB}$
3. **$P_3$:** $40\text{ KB}$

**Se pide:**

- **a)** Asigne cada proceso utilizando el algoritmo de ==Mejor Ajuste (Best-fit)==(verde).
- **b)** Indique el tamaño de los huecos resultantes y si algún bloque quedó completamente intacto.

---

### Ejercicio 5: Evolución de Residuos con Worst-fit

Un sistema dispone de los siguientes cinco bloques libres:

* **Bloque 1 ($B_1$):** $80\text{ KB}$
* **Bloque 2 ($B_2$):** $200\text{ KB}$
* **Bloque 3 ($B_3$):** $400\text{ KB}$
* **Bloque 4 ($B_4$):** $150\text{ KB}$
* **Bloque 5 ($B_5$):** $300\text{ KB}$

Llegan secuencialmente tres peticiones:

1. **$P_1$:** $120\text{ KB}$
2. **$P_2$:** $180\text{ KB}$
3. **$P_3$:** $70\text{ KB}$

**Se pide:**

- **a)** Aplique el algoritmo de ==Peor Ajuste (Worst-fit)==(naranja) para ubicar los tres procesos.
- **b)** Detalle el tamaño final de cada uno de los 5 bloques al terminar la asignación.

<!-- PAGEBREAK -->

## 🧮 Bloque B: Paginación y Traducción de Direcciones

### Ejercicio 6: Traducción Lógica a Física (Páginas de 4 KB)

Un sistema de memoria virtual utiliza **direcciones lógicas de $32\text{ bits}$** y un **tamaño de página de $4\text{ KB}$** ($4096\text{ bytes}$).

La tabla de páginas activa para el proceso en ejecución es la siguiente:

| Página ($p$) | Marco / Frame ($f$) | Bit de Presencia (Residente) |
| :---: | :---: | :---: |
| **$0$** | $5$ | $1$ |
| **$1$** | $3$ | $1$ |
| **$2$** | $8$ | $1$ |
| **$3$** | $2$ | $0$ |
| **$4$** | $10$ | $1$ |

**Se pide:**

Traduzca las siguientes direcciones lógicas expresadas como $(p, d)$ a sus correspondientes direcciones físicas reales, mostrando la fórmula y el cálculo matemático:

- **a)** Dirección I: $(0, 2000)$
- **b)** Dirección II: $(2, 500)$
- **c)** Dirección III: $(1, 3900)$

---

### Ejercicio 7: Detección y Tratamiento de Fallo de Página

Tomando como base la tabla de páginas del **Ejercicio 6**:

**Se pide:**

- **a)** Indique qué ocurre cuando el proceso intenta acceder a la dirección lógica **$(3, 1200)$**.
- **b)** Describa de manera ordenada la secuencia de acciones que ejecutan el hardware (MMU) y el Sistema Operativo (Kernel) para resolver el ==Fallo de Página (Page Fault)==(rojo).

---

### Ejercicio 8: Traducción con Páginas de 2 KB y Bit de Validez

Un procesador trabaja con páginas de **$2\text{ KB}$** ($2048\text{ bytes}$). La tabla de páginas del proceso activo es:

* **Página 0:** Marco $4$ (Bit de presencia $= 1$)
* **Página 1:** Marco $1$ (Bit de presencia $= 1$)
* **Página 2:** Marco $6$ (Bit de presencia $= 0$)

**Se pide:**

- **a)** Traduzca a dirección física la referencia $(0, 100)$.
- **b)** Traduzca a dirección física la referencia $(1, 2000)$.
- **c)** Explique qué ocurre al intentar traducir la referencia $(2, 1500)$.

---

### Ejercicio 9: Dirección Física Base de Marcos

En un sistema con un tamaño de página de **$4\text{ KB}$** ($4096\text{ bytes}$), la memoria física se divide en marcos contiguos indexados desde $0$.

**Se pide:**

Calcule la **dirección física inicial** (dirección base o límite inferior) correspondiente a cada uno de los siguientes marcos:

- **a)** Marco $3$
- **b)** Marco $7$
- **c)** Marco $9$
- **d)** Marco $15$

---

### Ejercicio 10: Traducción con Páginas de 8 KB

Un sistema operativo utiliza un tamaño de página de **$8\text{ KB}$** ($8192\text{ bytes}$). La tabla de páginas asigna la **Página 2** al **Marco 9** (con Bit de presencia $= 1$).

**Se pide:**

- **a)** Calcule la dirección física correspondiente a la dirección lógica **$(2, 4000)$**.

<!-- PAGEBREAK -->

## 📐 Bloque C: Dimensionamiento de Tablas, Límites y Fragmentación

### Ejercicio 11: Dimensionamiento de Tabla de Páginas

Un proceso en ejecución ocupa **$30\text{ MB}$** ($31.457.280\text{ bytes}$) en memoria. El sistema operativo emplea entradas de tabla de páginas (PTE) de **$4\text{ bytes}$** cada una.

**Se pide:**

Para cada una de las tres alternativas de tamaño de página, calcule la **cantidad de páginas** del proceso y el **tamaño total de su tabla de páginas** (en $\text{KB}$):

- **a)** Alternativa A: Tamaño de página $= 2\text{ KB}$ ($2048\text{ bytes}$).
- **b)** Alternativa B: Tamaño de página $= 4\text{ KB}$ ($4096\text{ bytes}$).
- **c)** Alternativa C: Tamaño de página $= 16\text{ KB}$ ($16.384\text{ bytes}$).

---

### Ejercicio 12: Límites de Direccionamiento en 32 Bits (Páginas de 4 KB)

Un sistema informático utiliza **direcciones lógicas de $32\text{ bits}$**, páginas de **$4\text{ KB}$** ($2^{12}\text{ bytes}$) y entradas de tabla de **$4\text{ bytes}$**.

**Se pide:**

- **a)** Calcule la **cantidad máxima de páginas** que puede llegar a direccionar un proceso.
- **b)** Calcule el **tamaño total de la tabla de páginas** (en $\text{MB}$) si el programa decidiera mapear todo su espacio de direcciones lógicas de $32\text{ bits}$.

---

### Ejercicio 13: Límites de Direccionamiento en 32 Bits (Páginas de 16 KB)

Se rediseña el sistema del Ejercicio 12 adoptando un **tamaño de página de $16\text{ KB}$** ($2^{14}\text{ bytes}$).

**Se pide:**

- **a)** Determine la **nueva cantidad máxima de páginas** direccionables por proceso.
- **b)** Calcule el **nuevo tamaño total máximo de la tabla de páginas** (en $\text{MB}$).
- **c)** Compare ambos resultados y explique la ventaja arquitectónica respecto al consumo de memoria.

---

### Ejercicio 14: Cálculo de Páginas y Fragmentación Interna

Un proceso cuyo tamaño es de **$15{,}5\text{ KB}$** ($15.872\text{ bytes}$) se ejecuta en un sistema con un tamaño de página de **$4\text{ KB}$** ($4096\text{ bytes}$).

**Se pide:**

- **a)** Calcule cuántas páginas/marcos requiere el sistema operativo para alojar al proceso.
- **b)** Calcule de forma exacta el desperdicio de memoria generado por ==fragmentación interna==(rosa) en el último marco asignado (en $\text{bytes}$).

---

### Ejercicio 15: Evaluación y Comparativa de Decisiones de Diseño

Un sistema operativo debe alojar un proceso promedio de **$10\text{ MB}$** ($10.240\text{ KB}$). El diseñador del SO evalúa tres alternativas de tamaño de página: **$1\text{ KB}$**, **$4\text{ KB}$** y **$16\text{ KB}$**. Las entradas de tabla de páginas ocupan $4\text{ bytes}$.

**Se pide:**

- **a)** Ordene las tres alternativas de menor a mayor según la **fragmentación interna esperada**, justificando la respuesta.
- **b)** Ordene las tres alternativas de menor a mayor según el **espacio ocupado por la tabla de páginas**, justificando numéricamente el cálculo para cada caso.

<!-- PAGEBREAK -->

# 🔑 Resoluciones Detalladas Paso a Paso

---

## 📌 Resoluciones: Bloque A (Particionamiento Dinámico)

### Solución del Ejercicio 1 (Primer Ajuste / First-fit)

* **Capacidad inicial total:**
  $$\text{Total Libre} = 100 + 500 + 200 + 300 + 600 = \mathbf{1700\text{ KB}}$$

#### a) Proceso de Asignación Paso a Paso:
* **$P_1$ ($150\text{ KB}$):** Comienza la búsqueda desde $B_1$.
  * En $B_1$ ($100\text{ KB}$) no entra.
  * Entra en **$B_2$ ($500\text{ KB}$)**.
  * *Residuo:* $500\text{ KB} - 150\text{ KB} = 350\text{ KB}$.
* **$P_2$ ($250\text{ KB}$):** Comienza la búsqueda desde el inicio.
  * En $B_1$ ($100\text{ KB}$) no entra.
  * Entra en el residuo de **$B_2$ ($350\text{ KB}$)**.
  * *Residuo:* $350\text{ KB} - 250\text{ KB} = 100\text{ KB}$.
* **$P_3$ ($90\text{ KB}$):** Comienza la búsqueda desde el inicio.
  * Entra en **$B_1$ ($100\text{ KB}$)**.
  * *Residuo:* $100\text{ KB} - 90\text{ KB} = 10\text{ KB}$.
* **$P_4$ ($450\text{ KB}$):** Comienza la búsqueda desde el inicio.
  * No entra en $B_1$ ($10\text{ KB}$), ni en $B_2$ ($100\text{ KB}$), ni en $B_3$ ($200\text{ KB}$), ni en $B_4$ ($300\text{ KB}$).
  * Entra en **$B_5$ ($600\text{ KB}$)**.
  * *Residuo:* $600\text{ KB} - 450\text{ KB} = 150\text{ KB}$.

#### b) Tamaño de los huecos resultantes:
* $B_1 = \mathbf{10\text{ KB}}$
* $B_2 = \mathbf{100\text{ KB}}$
* $B_3 = \mathbf{200\text{ KB}}$ *(intacto)*
* $B_4 = \mathbf{300\text{ KB}}$ *(intacto)*
* $B_5 = \mathbf{150\text{ KB}}$

#### c) Memoria libre total restante:
$$\text{Memoria Libre Total} = 10 + 100 + 200 + 300 + 150 = \mathbf{760\text{ KB}}$$

---

### Solución del Ejercicio 2 (Mejor Ajuste / Best-fit)

#### a) Proceso de Asignación Paso a Paso:
* **$P_1$ ($150\text{ KB}$):** Bloques viables: $B_3(200), B_4(300), B_2(500), B_5(600)$.
  * El más ajustado es **$B_3$ ($200\text{ KB}$)**.
  * *Residuo:* $200\text{ KB} - 150\text{ KB} = \mathbf{50\text{ KB}}$.
* **$P_2$ ($250\text{ KB}$):** Bloques viables: $B_4(300), B_2(500), B_5(600)$.
  * El más ajustado es **$B_4$ ($300\text{ KB}$)**.
  * *Residuo:* $300\text{ KB} - 250\text{ KB} = \mathbf{50\text{ KB}}$.
* **$P_3$ ($90\text{ KB}$):** Bloques viables: $B_1(100), B_2(500), B_5(600)$.
  * El más ajustado es **$B_1$ ($100\text{ KB}$)**.
  * *Residuo:* $100\text{ KB} - 90\text{ KB} = \mathbf{10\text{ KB}}$.
* **$P_4$ ($450\text{ KB}$):** Bloques viables: $B_2(500), B_5(600)$.
  * El más ajustado es **$B_2$ ($500\text{ KB}$)**.
  * *Residuo:* $500\text{ KB} - 450\text{ KB} = \mathbf{50\text{ KB}}$.

#### b) Detalle de los huecos resultantes:
* $B_1 = \mathbf{10\text{ KB}}$, $B_2 = \mathbf{50\text{ KB}}$, $B_3 = \mathbf{50\text{ KB}}$, $B_4 = \mathbf{50\text{ KB}}$, $B_5 = \mathbf{600\text{ KB}}$.
* $\text{Memoria Libre Total} = 10 + 50 + 50 + 50 + 600 = \mathbf{760\text{ KB}}$.

#### c) Bloque intacto:
El **Bloque 5 ($B_5$ de $600\text{ KB}$)** permanece totalmente intacto.

---

### Solución del Ejercicio 3 (Peor Ajuste / Worst-fit)

#### a) Proceso de Asignación Paso a Paso:
* **$P_1$ ($150\text{ KB}$):** Selecciona el mayor bloque: **$B_5$ ($600\text{ KB}$)**.
  * *Residuo:* $600\text{ KB} - 150\text{ KB} = 450\text{ KB}$.
* **$P_2$ ($250\text{ KB}$):** El mayor hueco disponible es **$B_2$ ($500\text{ KB}$)**.
  * *Residuo:* $500\text{ KB} - 250\text{ KB} = 250\text{ KB}$.
* **$P_3$ ($90\text{ KB}$):** Huecos disponibles: $B_1(100), B_2(250), B_3(200), B_4(300), B_5(450)$.
  * El mayor disponible es **$B_5$ ($450\text{ KB}$)**.
  * *Residuo:* $450\text{ KB} - 90\text{ KB} = 360\text{ KB}$.

#### b) y c) Situación del Proceso $P_4$ y Justificación:
* Al llegar **$P_4$ ($450\text{ KB}$)**, los huecos individuales disponibles en memoria son:
  $$B_1 = 100\text{ KB}, \quad B_2 = 250\text{ KB}, \quad B_3 = 200\text{ KB}, \quad B_4 = 300\text{ KB}, \quad B_5 = 360\text{ KB}$$
* El mayor hueco individual es de $360\text{ KB}$, que es estrictamente menor a los $450\text{ KB}$ contiguos que necesita $P_4$.
* **Conclusión:** Aunque la suma total de memoria libre es de $100 + 250 + 200 + 300 + 360 = \mathbf{1210\text{ KB}}$, **el proceso $P_4$ no puede ser asignado y queda bloqueado**. Este fenómeno representa un caso clásico de ==fragmentación externa==(rojo), donde la memoria está disponible pero dispersa en bloques pequeños no contiguos.

<!-- PAGEBREAK -->

### Solución del Ejercicio 4 (Best-fit)

#### a) Asignaciones:
* **$P_1$ ($80\text{ KB}$):** Se asigna en **$B_4$ ($100\text{ KB}$)**. Residuo: $100 - 80 = \mathbf{20\text{ KB}}$.
* **$P_2$ ($110\text{ KB}$):** Se asigna en **$B_2$ ($150\text{ KB}$)**. Residuo: $150 - 110 = \mathbf{40\text{ KB}}$.
* **$P_3$ ($40\text{ KB}$):** Huecos libres: $50\text{ KB}$, $40\text{ KB}$ (en $B_2$), $300\text{ KB}$, $20\text{ KB}$ (en $B_4$). El más ajustado es el residuo de **$B_2$ ($40\text{ KB}$)**. Residuo: $40 - 40 = \mathbf{0\text{ KB}}$.

#### b) Estado final:
* $B_1 = \mathbf{50\text{ KB}}$ *(intacto)*
* $B_2 = \mathbf{0\text{ KB}}$ *(completamente ocupado)*
* $B_3 = \mathbf{300\text{ KB}}$ *(intacto)*
* $B_4 = \mathbf{20\text{ KB}}$
* ==**Bloques intactos:** $B_1$ ($50\text{ KB}$) y $B_3$ ($300\text{ KB}$)==(verde).

---

### Solución del Ejercicio 5 (Worst-fit)

#### a) Asignaciones:
* **$P_1$ ($120\text{ KB}$):** Se asigna en el mayor bloque, **$B_3$ ($400\text{ KB}$)**. Residuo: $400 - 120 = \mathbf{280\text{ KB}}$.
* **$P_2$ ($180\text{ KB}$):** El mayor disponible es **$B_5$ ($300\text{ KB}$)**. Residuo: $300 - 180 = \mathbf{120\text{ KB}}$.
* **$P_3$ ($70\text{ KB}$):** Huecos: $B_1(80), B_2(200), B_3(280), B_4(150), B_5(120)$. El mayor es **$B_3$ ($280\text{ KB}$)**. Residuo: $280 - 70 = \mathbf{210\text{ KB}}$.

#### b) Tamaño final de los 5 bloques:
* **Bloque 1 ($B_1$):** $\mathbf{80\text{ KB}}$ *(intacto)*
* **Bloque 2 ($B_2$):** $\mathbf{200\text{ KB}}$ *(intacto)*
* **Bloque 3 ($B_3$):** $\mathbf{210\text{ KB}}$ *(residuo)*
* **Bloque 4 ($B_4$):** $\mathbf{150\text{ KB}}$ *(intacto)*
* **Bloque 5 ($B_5$):** $\mathbf{120\text{ KB}}$ *(residuo)*

---
---

## 📌 Resoluciones: Bloque B (Paginación y Traducción de Direcciones)

> **Ecuación Fundamental de Traducción:**
> $$\text{Dirección Física} = (\text{Marco} \times \text{Tamaño de Página}) + \text{Desplazamiento}$$

### Solución del Ejercicio 6 (Traducción 4 KB)

* Tamaño de página: $4\text{ KB} = 4096\text{ bytes}$.

#### a) Dirección I: $(0, 2000)$
* La Página $0$ mapea al Marco $5$ (Bit Presencia = $1$).
$$\text{Dir. Física} = (5 \times 4096) + 2000 = 20.480 + 2000 = \mathbf{22.480}$$

#### b) Dirección II: $(2, 500)$
* La Página $2$ mapea al Marco $8$ (Bit Presencia = $1$).
$$\text{Dir. Física} = (8 \times 4096) + 500 = 32.768 + 500 = \mathbf{33.268}$$

#### c) Dirección III: $(1, 3900)$
* La Página $1$ mapea al Marco $3$ (Bit Presencia = $1$).
$$\text{Dir. Física} = (3 \times 4096) + 3900 = 12.288 + 3900 = \mathbf{16.188}$$

---

### Solución del Ejercicio 7 (Fallo de Página / Page Fault)

#### a) Evento inicial:
Al acceder a $(3, 1200)$, la MMU lee la entrada $3$ de la tabla y detecta que el **Bit de Presencia es $0$** (página no residente en memoria física). Se genera una excepción de ==Fallo de Página (Page Fault)==(rojo).

#### b) Secuencia de Resolución del Kernel:
1. **Interrupción:** La MMU interrumpe el procesador y transfiere el control a la rutina de tratamiento de fallos del Sistema Operativo.
2. **Localización:** El SO busca la dirección de bloque de la Página $3$ en el almacenamiento secundario (*área de swap* / disco).
3. **Asignación de Marco:** El SO busca un marco libre en la RAM. Si no hay ninguno disponible, ejecuta un algoritmo de reemplazo de páginas (como LRU o FIFO) para liberar un marco.
4. **Transferencia E/S:** Se transfiere el contenido de la página desde el disco hacia el marco físico asignado.
5. **Actualización de Tabla:** El SO escribe el número de marco en la entrada $3$ y setea el **Bit de Presencia en $1$**.
6. **Reanudación:** El SO restaura el contexto del proceso y reinicia la instrucción de CPU interrumpida, que ahora se ejecutará con éxito.

<!-- PAGEBREAK -->

### Solución del Ejercicio 8 (Traducción 2 KB)

* Tamaño de página: $2\text{ KB} = 2048\text{ bytes}$.

- **a) Dirección $(0, 100)$:**  
  La Página $0$ reside en el Marco $4$.  
  $$\text{Dir. Física} = (4 \times 2048) + 100 = 8192 + 100 = \mathbf{8292}$$

- **b) Dirección $(1, 2000)$:**  
  La Página $1$ reside en el Marco $1$.  
  $$\text{Dir. Física} = (1 \times 2048) + 2000 = 2048 + 2000 = \mathbf{4048}$$

- **c) Dirección $(2, 1500)$:**  
  La Página $2$ tiene Bit de Presencia $= 0$.  
  ==**Resultado:** Se genera un **Fallo de Página (Page Fault)**. No se puede calcular la dirección física en forma directa hasta que el sistema operativo cargue la página desde el disco a la memoria RAM.==(rojo)

---

### Solución del Ejercicio 9 (Dirección Física Base de Marcos)

$$\text{Dirección Base} = \text{Número de Marco} \times 4096\text{ bytes}$$

- **a) Marco 3:** $3 \times 4096 = \mathbf{12.288}$
- **b) Marco 7:** $7 \times 4096 = \mathbf{28.672}$
- **c) Marco 9:** $9 \times 4096 = \mathbf{36.864}$
- **d) Marco 15:** $15 \times 4096 = \mathbf{61.440}$

---

### Solución del Ejercicio 10 (Traducción 8 KB)

* Tamaño de página: $8\text{ KB} = 8192\text{ bytes}$.
* Página $2 \to$ Marco $9$.
$$\text{Dirección Física} = (9 \times 8192) + 4000 = 73.728 + 4000 = \mathbf{77.728}$$

---
---

## 📌 Resoluciones: Bloque C (Dimensionamiento, Límites y Fragmentación)

### Solución del Ejercicio 11 (Dimensionamiento de Tablas)

* Proceso: $30\text{ MB} = 30 \times 1024\text{ KB} = 30.720\text{ KB} = 31.457.280\text{ bytes}$.
* Entrada de tabla: $4\text{ bytes}$.

#### a) Alternativa 2 KB ($2048\text{ bytes}$):
$$\text{Cantidad de Páginas} = \frac{31.457.280\text{ bytes}}{2048\text{ bytes}} = 15.360\text{ páginas}$$
$$\text{Tamaño Tabla} = 15.360 \times 4\text{ bytes} = 61.440\text{ bytes} = \mathbf{60\text{ KB}}$$

#### b) Alternativa 4 KB ($4096\text{ bytes}$):
$$\text{Cantidad de Páginas} = \frac{31.457.280\text{ bytes}}{4096\text{ bytes}} = 7.680\text{ páginas}$$
$$\text{Tamaño Tabla} = 7.680 \times 4\text{ bytes} = 30.720\text{ bytes} = \mathbf{30\text{ KB}}$$

#### c) Alternativa 16 KB ($16.384\text{ bytes}$):
$$\text{Cantidad de Páginas} = \frac{31.457.280\text{ bytes}}{16.384\text{ bytes}} = 1.920\text{ páginas}$$
$$\text{Tamaño Tabla} = 1.920 \times 4\text{ bytes} = 7.680\text{ bytes} = \mathbf{7{,}5\text{ KB}}$$

<!-- PAGEBREAK -->

### Solución del Ejercicio 12 (Límites Arquitectónicos con 4 KB)

* Espacio lógico de $32\text{ bits} \implies 2^{32}\text{ bytes} = 4.294.967.296\text{ bytes} = 4\text{ GB}$.
* Tamaño de página: $4\text{ KB} = 2^{12}\text{ bytes} = 4096\text{ bytes}$.

#### a) Número máximo de páginas:
$$N_{\text{máx}} = \frac{2^{32}\text{ bytes}}{2^{12}\text{ bytes}} = 2^{20} = \mathbf{1.048.576\text{ páginas}}$$

#### b) Tamaño total de la tabla de páginas:
$$\text{Tamaño Tabla} = 1.048.576\text{ entradas} \times 4\text{ bytes} = 4.194.304\text{ bytes} = \mathbf{4\text{ MB}}$$

---

### Solución del Ejercicio 13 (Límites Arquitectónicos con 16 KB)

* Tamaño de página: $16\text{ KB} = 2^{14}\text{ bytes} = 16.384\text{ bytes}$.

#### a) Nueva cantidad máxima de páginas:
$$N_{\text{máx}} = \frac{2^{32}\text{ bytes}}{2^{14}\text{ bytes}} = 2^{18} = \mathbf{262.144\text{ páginas}}$$

#### b) Nuevo tamaño total de la tabla:
$$\text{Tamaño Tabla} = 262.144\text{ entradas} \times 4\text{ bytes} = 1.048.576\text{ bytes} = \mathbf{1\text{ MB}}$$

#### c) Conclusión:
Al cuadruplicar el tamaño de página (de $4\text{ KB}$ a $16\text{ KB}$), la cantidad de entradas y el espacio ocupado por la tabla se reducen a la cuarta parte (de $4\text{ MB}$ a $1\text{ MB}$), disminuyendo significativamente la sobrecarga en memoria RAM.

---

### Solución del Ejercicio 14 (Páginas y Fragmentación Interna)

* Datos: $\text{Proceso} = 15{,}5\text{ KB} = 15.872\text{ bytes}$, $\text{Página} = 4\text{ KB} = 4096\text{ bytes}$.

#### a) Páginas requeridas:
$$\text{Páginas} = \left\lceil \frac{15{,}5\text{ KB}}{4\text{ KB}} \right\rceil = \lceil 3{,}875 \rceil = \mathbf{4\text{ páginas}}$$
*(Se asignan 4 marcos de memoria física completa).*

#### b) Fragmentación interna:
* Memoria asignada en los 4 marcos: $4 \times 4096\text{ bytes} = 16.384\text{ bytes}$.
* Memoria requerida por el proceso: $15.872\text{ bytes}$.
$$\text{Fragmentación Interna} = 16.384\text{ bytes} - 15.872\text{ bytes} = \mathbf{512\text{ bytes}}$$
> ==**Resultado:** Se desperdician **$512\text{ bytes}$** en el último marco asignado.==(rosa)

---

### Solución del Ejercicio 15 (Comparativa de Decisiones de Diseño)

Proceso de $10\text{ MB} = 10.240\text{ KB}$, entradas de tabla de $4\text{ bytes}$.

#### a) Orden por menor fragmentación interna:
$$\mathbf{1\text{ KB} < 4\text{ KB} < 16\text{ KB}}$$
* **Justificación:** La pérdida por fragmentación interna en el último marco es en promedio igual a $\frac{\text{Tamaño de Página}}{2}$. Cuanto menor es el tamaño de página ($1\text{ KB}$ frente a $16\text{ KB}$), menor es el espacio no utilizado en la última página del proceso.

#### b) Orden por menor sobrecarga de tabla de páginas:
* **Para 16 KB:** $\frac{10.240\text{ KB}}{16\text{ KB}} = 640\text{ entradas} \implies 640 \times 4\text{ B} = \mathbf{2{,}5\text{ KB}}$ de tabla.
* **Para 4 KB:** $\frac{10.240\text{ KB}}{4\text{ KB}} = 2560\text{ entradas} \implies 2560 \times 4\text{ B} = \mathbf{10\text{ KB}}$ de tabla.
* **Para 1 KB:** $\frac{10.240\text{ KB}}{1\text{ KB}} = 10240\text{ entradas} \implies 10240 \times 4\text{ B} = \mathbf{40\text{ KB}}$ de tabla.

$$\mathbf{16\text{ KB} < 4\text{ KB} < 1\text{ KB}}$$
* **Justificación:** A mayor tamaño de página, se necesitan muchas menos entradas en la tabla de páginas, reduciendo el consumo de memoria física ocupada por las estructuras del kernel.