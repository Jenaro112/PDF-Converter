# 📘 Guía de Fórmulas y Procedimientos: Sistemas Operativos

---

## 1. Planificación de Procesos (Round Robin y FCFS)

Este tipo de ejercicios requiere simular la ejecución concurrente de múltiples procesos, manejando los estados de CPU y los dispositivos de Entrada/Salida (E/S).

### ⚙️ Algoritmos Utilizados

* **Round Robin (RR):** Asigna a cada proceso un tiempo máximo continuo de CPU llamado <span style="color: #2563eb; font-weight: bold;">Quantum ($q$)</span>. Si el proceso no termina su ráfaga en ese tiempo, es desalojado y vuelve al final de la cola de **Listos**.
* **FCFS (First-Come, First-Served):** Para los dispositivos de E/S (Disco, Impresora, etc.), el primer proceso que llega a la cola del dispositivo es el primero en ser atendido.

> [!IMPORTANT]
> **Resolución de Empates:** Si varios procesos llegan al mismo tiempo a una misma cola, tiene prioridad el proceso que posea el **mayor número de identificación** (ej: $P_3 > P_1$).

---

### 📐 Fórmulas Principales

#### 1. Tiempo de Retorno ($T_R$)
Es el tiempo total transcurrido desde que un proceso llega al sistema hasta que finaliza por completo.
$$T_R = t_{\text{fin}} - t_{\text{llegada}}$$

#### 2. Tiempo Medio de Retorno ($\bar{T}_R$)
Es el promedio de los tiempos de retorno de todos los $n$ procesos del sistema.
$$\bar{T}_R = \frac{\sum_{i=1}^{n} T_R(i)}{n}$$

#### 3. Tiempo de Espera ($T_E$)
Es el tiempo neto que el proceso pasa esperando en la **cola de listos** (no incluye el tiempo invertido ejecutando en CPU ni el tiempo bloqueado en E/S). 

$$T_E = T_R - \text{Ráfagas totales de CPU} - \text{Ráfagas totales de E/S}$$

> [!NOTE]
> En el diagrama de tiempos, $T_E$ también se puede calcular sumando de forma directa la cantidad de instantes en estado de Listo (**"L"**).

#### 4. Tiempo Medio de Espera ($\bar{T}_E$)
$$\bar{T}_E = \frac{\sum_{i=1}^{n} T_E(i)}{n}$$

#### 5. Porcentaje de Utilización de CPU
Se evalúa sobre un intervalo $[0; T_{\text{total}})$, contando el número de unidades de tiempo (ut) en las que la CPU estuvo ejecutando algún proceso.
$$\text{Utilización de CPU} = \left( \frac{\text{ut ocupadas}}{\text{ut totales}} \right) \times 100\%$$

#### 6. Tiempo Ocioso de Dispositivos
Un dispositivo de E/S está ocioso en el intervalo $[0; T_{\text{total}})$ durante el tiempo en que ningún proceso requiere su uso.
$$\text{Tiempo Ocioso} = T_{\text{total}} - \sum \text{ut de ráfagas en el dispositivo}$$

<!-- PAGEBREAK -->

## 2. Asignación de Memoria Contigua

En estos problemas, el Sistema Operativo debe ubicar los procesos entrantes en los huecos (espacios de memoria libre) disponibles en la RAM.

### 🧠 Algoritmos de Búsqueda

* <span style="color: #2563eb; font-weight: bold;">Primer Ajuste (First Fit):</span> Recorre la lista de huecos libres desde el principio y asigna el proceso al **primer** hueco que sea lo suficientemente grande.
* <span style="color: #059669; font-weight: bold;">Mejor Ajuste (Best Fit):</span> Revisa **toda** la lista de huecos y asigna el proceso al hueco que deje la **menor** porción sobrante (el más ajustado al tamaño del proceso).
* <span style="color: #d97706; font-weight: bold;">Peor Ajuste (Worst Fit):</span> Revisa **toda** la lista de huecos y asigna el proceso al hueco **más grande** disponible, dejando el mayor espacio sobrante posible.

---

### 📐 Procedimiento Matemático

Al intentar ubicar un proceso de tamaño $P$ en un hueco de tamaño $H$:
* Si $P = H$, el hueco se ocupa por completo y desaparece de la lista de libres.
* Si $P < H$, el proceso ocupa $P$ y se crea un nuevo hueco con el espacio restante:
$$\text{Nuevo Hueco} = H - P$$

#### Cálculo de Memoria Libre Total
Se obtiene sumando los tamaños de todos los huecos libres que quedan al finalizar la asignación de los procesos.
$$\text{Memoria Libre Total} = \sum_{i=1}^{k} \text{Hueco}_i$$

<!-- PAGEBREAK -->

## 3. Dimensionamiento y Paginación

### 💡 Conceptos Clave
En los esquemas de memoria virtual paginada:
* La memoria lógica (espacio de dirección del proceso) se divide en **Páginas**.
* La memoria física (RAM) se divide en **Marcos** (o marcos de página).

> [!NOTE]
> Las Páginas y los Marcos tienen **exactamente el mismo tamaño**.

---

### 📐 Fórmulas de Cálculo

#### 1. Cantidad de Páginas de un Proceso
Conociendo el tamaño del proceso y el tamaño de página:
$$\text{Cantidad de Páginas} = \left\lceil \frac{\text{Tamaño del Proceso}}{\text{Tamaño de Página}} \right\rceil$$

> [!NOTE]
> La función techo $\lceil x \rceil$ redondea **siempre hacia arriba** al entero más cercano, ya que incluso un único byte sobrante requiere una página completa.

#### 2. Relación Tamaño de Página vs. Fragmentación Interna

| Tamaño de Página | Ventajas | Desventajas | Impacto en Fragmentación |
| :--- | :--- | :--- | :--- |
| **Grande** | Tablas de páginas más pequeñas (menos páginas totales). | <span style="color: #dc2626; font-weight: bold;">Mayor fragmentación interna</span> en la última página. | En promedio se desperdicia **$\frac{1}{2}$ página** por proceso. |
| **Pequeño** | <span style="color: #059669; font-weight: bold;">Menor fragmentación interna</span> (aprovechamiento óptimo). | Tablas de páginas muy grandes (mayor consumo de RAM estructural del SO). | Mínimo desperdicio en la última página. |

<!-- PAGEBREAK -->

## 4. Traducción de Direcciones (Memoria Virtual)

La **MMU** (Memory Management Unit) utiliza la **Tabla de Páginas** para traducir una dirección lógica emitida por la CPU a una dirección física en la RAM.

### 📍 Estructura de la Dirección Lógica
Se representa mediante el par $(p, d)$:
* **$p$**: Número de página.
* **$d$**: Desplazamiento (*offset*) dentro de la página.

---

### 📐 Fórmulas y Procedimientos

#### 1. Descomposición de la Dirección Lógica Decimal ($L$)
Dada una dirección lógica escalar $L$:
$$p = \left\lfloor \frac{L}{\text{Tamaño de Página}} \right\rfloor$$
$$d = L \bmod \text{Tamaño de Página}$$

#### 2. Traducción a Dirección Física ($DF$)
Una vez obtenido $p$, se consulta la Tabla de Páginas para obtener el Marco ($m$) correspondiente. Si el bit **Residente** es $1$:
$$DF = (m \times \text{Tamaño de Página}) + d$$

#### 3. Dirección Física Inicial de un Marco
Es la dirección base donde inicia un marco en RAM (desplazamiento $d = 0$):
$$DF_{\text{inicial}} = m \times \text{Tamaño de Página}$$

#### 4. Número Máximo de Páginas del Sistema
Depende del número de bits del bus de direcciones lógicas:
$$\text{Total de Páginas Direccionables} = \frac{2^{\text{Bits de dirección}}}{\text{Tamaño de Página}}$$

#### 5. Tamaño de la Tabla de Páginas
Cada proceso posee su propia tabla de páginas en memoria principal:
$$\text{Tamaño de la Tabla} = \text{Número de Páginas del Proceso} \times \text{Tamaño de Entrada (PTE)}$$

---

### ⚠️ Excepciones y Manejo de Fallos

> [!WARNING]
> **Segmentation Fault (Violación de Segmento):**
> Ocurre cuando el número de página $p$ excede el límite asignado al proceso ($p \ge \text{Páginas totales del proceso}$).

> [!CAUTION]
> **Page Fault (Fallo de Página):**
> Ocurre cuando el bit **Residente es $0$** (la página no se encuentra cargada en RAM). El SO debe interrumpir la ejecución, buscar la página en el Disco (área de Swap) y cargarla en un marco libre de la RAM.

<!-- PAGEBREAK -->

## 5. Ejemplos Prácticos de Aplicación

### 📊 Ejemplo 1: Planificación de Procesos (Cálculo de Tiempos)
Un proceso $P_1$ llega en $t=2$ y finaliza en $t=15$. Durante su estadía acumuló **5 ut** de CPU y **3 ut** bloqueado en disco.

* **Tiempo de Retorno ($T_R$):**  
  $$T_R = 15 - 2 = \mathbf{13\text{ ut}}$$
* **Tiempo de Espera ($T_E$):**  
  $$T_E = 13 - 5 - 3 = \mathbf{5\text{ ut}}$$ *(tiempo en cola de listos)*

---

### 📊 Ejemplo 2: Asignación de Memoria Contigua
Dados los huecos libres en el orden: `80 KB, 250 KB, 400 KB, 150 KB`. Llega un proceso $A$ de **140 KB**.

* <span style="color: #2563eb; font-weight: bold;">Primer Ajuste (First Fit):</span> Evalúa 80 KB (no entra). Evalúa 250 KB (entra).
  * *Nuevo hueco sobrante:* $250 - 140 = \mathbf{110\text{ KB}}$
* <span style="color: #059669; font-weight: bold;">Mejor Ajuste (Best Fit):</span> Busca el hueco $\ge 140\text{ KB}$ que deje la menor sobra. Elige 150 KB.
  * *Nuevo hueco sobrante:* $150 - 140 = \mathbf{10\text{ KB}}$
* <span style="color: #d97706; font-weight: bold;">Peor Ajuste (Worst Fit):</span> Busca el hueco más grande disponible (400 KB).
  * *Nuevo hueco sobrante:* $400 - 140 = \mathbf{260\text{ KB}}$

---

### 📊 Ejemplo 3: Paginación y Cantidad de Páginas
Un proceso ocupa **20 MB** de memoria y el sistema utiliza páginas de **4 KB**.

1. **Convertir MB a KB:** $20 \times 1024 = 20480\text{ KB}$
2. **Calcular Páginas:**
   $$\text{Páginas} = \left\lceil \frac{20480\text{ KB}}{4\text{ KB}} \right\rceil = \mathbf{5120\text{ páginas}}$$

---

### 📊 Ejemplo 4: Traducción de Direcciones
Sistema con tamaño de página de **4 KB** ($4096\text{ bytes}$). La página `3` está residente en el marco `11`. Se consulta la dirección lógica `(3, 2500)`:

* $p = 3$, $d = 2500$, $m = 11$
* **Dirección Física ($DF$):**
  $$DF = (11 \times 4096) + 2500 = 45056 + 2500 = \mathbf{47556}$$

> [!NOTE]
> La dirección base física donde inicia el marco `11` es $11 \times 4096 = 45056$.