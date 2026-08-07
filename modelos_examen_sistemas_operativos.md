# Modelos de Examen Parcial y Resoluciones

**Materia:** Sistemas Operativos  
**Carrera:** Licenciatura en Sistemas  
**Institución:** Universidad Autónoma de Entre Ríos (UADER)  
**Alumno:** Jenaro Galdini  
**Fecha:** Agosto 2026  

---

<!-- TOC -->

---

<!-- PAGEBREAK -->

# 📝 MODELOS DE EXAMEN

## 📋 Modelo de Examen Nº 1

### Parte 1: Preguntas Teóricas

#### 1. Filosofía del Software
* ¿Qué diferencia filosófica existe entre el Software Libre (Free Software) y el Código Abierto (Open Source)?
* ¿Qué asegura la cláusula legal conocida como Copyleft en las licencias de software?

#### 2. Procesos e Hilos
* Explique la diferencia fundamental entre un Proceso y un Hilo (Thread) en términos de asignación de recursos y espacio de dirección de memoria.
* ¿Por qué el cambio de contexto entre hilos es significativamente más rápido que entre procesos?

#### 3. Concurrencia
* Defina los conceptos de Condición de Carrera (Race Condition) y Deadlock (Interbloqueo).
* ¿Cuál es la diferencia principal entre Deadlock e Inanición (Starvation)?

#### 4. Gestión de Memoria
* Explique en qué se diferencian la Paginación y la Segmentación según la división que hacen del programa y de la memoria física.
* Indique qué tipo de fragmentación (interna o externa) puede generar cada uno de estos esquemas.

---

### Parte 2: Ejercicio Práctico (Diagrama de Gantt)

Considere un sistema con **1 CPU, 1 Disco y 1 Impresora**. Se ejecutan dos procesos ($P_1$ y $P_2$) representados en la siguiente traza de ejecución:

> **Simbología:** `C` = CPU | `D` = Disco | `I` = Impresora | `L` = Cola de Listos

| Instante | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **P1** | C | C | D | D | L | L | C | I | C | | |
| **P2** | | L | L | C | C | C | D | L | L | C | C |

*(Nota: $P_1$ llega en $t=0$ y finaliza en $t=9$. $P_2$ llega en $t=1$ y finaliza en $t=11$).*

**Consignas:**
a) Calcule el tiempo de retorno de cada proceso y el tiempo medio de retorno ($\bar{T}_R$).  
b) Calcule el tiempo de espera de cada proceso y el tiempo medio de espera ($\bar{T}_E$).  
c) Calcule el porcentaje de utilización de la CPU (entre $t=0$ y $t=11$).  
d) Describa la secuencia de transiciones de estados por las que pasa el proceso $P_1$ desde su llegada hasta su finalización.  

---
<!-- PAGEBREAK -->

## 📋 Modelo de Examen Nº 2

### Parte 1: Preguntas Teóricas

#### 1. Definición de Sistema Operativo
* De acuerdo a lo expresado por Richard Stallman, ¿qué es un sistema operativo, qué hace y qué elementos mínimos lo componen?
* Explique brevemente la diferencia de arquitectura entre un Kernel Monolítico y un Microkernel (HURD).

#### 2. Estados de un Proceso
* Describa brevemente qué ocurre con el proceso y sus recursos en los estados Listo (Ready) y Espera/Bloqueado (Wait/Blocked).
* Al transferir el control al SO por una interrupción, ¿por qué se utiliza una pila del sistema (pila de núcleo) distinta a la pila de usuario del proceso?

#### 3. Suspensión e Intercambio
* ¿Qué es el intercambio de procesos o Swapping y en qué condiciones físicas del sistema el planificador decide implementarlo?
* Cuando un proceso pasa a un estado Suspendido, ¿dónde se ubica físicamente su imagen de memoria y qué estructura conserva el SO en la RAM?

#### 4. Memoria Virtual
* ¿Qué es el Conjunto Residente de un proceso en un esquema de memoria virtual y qué beneficio de gestión trae al sistema operativo?
* Defina el concepto de Thrashing (Hiperpaginación) y explique cuál es su causa principal.

---

### Parte 2: Ejercicio Práctico (Diagrama de Gantt)

Considere un sistema con **1 CPU, 1 Disco y 1 Impresora**. Se ejecutan dos procesos ($P_1$ y $P_2$) representados en la siguiente traza de ejecución:

> **Simbología:** `C` = CPU | `D` = Disco | `I` = Impresora | `L` = Cola de Listos

| Instante | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **P1** | C | L | C | D | D | L | C | C | |
| **P2** | | C | L | C | C | I | L | L | C |

*(Nota: $P_1$ llega en $t=0$ y finaliza en $t=8$. $P_2$ llega en $t=1$ y finaliza en $t=9$).*

**Consignas:**
a) Calcule el tiempo de retorno de cada proceso y el tiempo medio de retorno ($\bar{T}_R$).  
b) Calcule el tiempo de espera de cada proceso y el tiempo medio de espera ($\bar{T}_E$).  
c) Calcule el porcentaje de utilización de la CPU (entre $t=0$ y $t=9$).  
d) Describa la secuencia de transiciones de estados por las que pasa el proceso $P_2$ desde su llegada hasta su finalización.  

---
<!-- PAGEBREAK -->

## 📋 Modelo de Examen Nº 3

### Parte 1: Preguntas Teóricas

#### 1. Modelos de Desarrollo
* Explique la analogía de Eric Raymond sobre La Catedral y el Bazar en el desarrollo de software.
* ¿Qué riesgos se corren al permitir que una empresa monopolice o "pervierta" los estándares abiertos?

#### 2. Estructuras de Control del SO
* ¿Qué es el BCP (Bloque de Control de Proceso), por qué tiene una estructura de tamaño estático y qué tipo de información almacena?
* Mencione las cuatro tablas de control principales que gestiona el SO para administrar los recursos del sistema.

#### 3. Particionamiento de Memoria
* Explique la diferencia entre el Particionamiento Fijo y el Particionamiento Dinámico en la memoria principal.
* ¿Qué problema de fragmentación resuelve la Compactación en el particionamiento dinámico y en qué consiste dicha técnica?

#### 4. Reemplazo de Páginas
* Explique brevemente la idea básica de funcionamiento de los siguientes algoritmos de reemplazo de páginas en memoria virtual:
  * FIFO (First-In, First-Out)
  * LRU (Least Recently Used)
  * Algoritmo del Reloj (Clock)
* ¿Por qué el SO requiere implementar una política de Bloqueo de Marcos de Página?

---

### Parte 2: Ejercicio Práctico (Diagrama de Gantt)

Considere un sistema con **1 CPU y 1 Disco**. Se ejecutan dos procesos ($P_1$ y $P_2$) representados en la siguiente traza de ejecución:

> **Simbología:** `C` = CPU | `D` = Disco | `L` = Cola de Listos

| Instante | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **P1** | C | C | D | L | C | L | C | |
| **P2** | | L | C | C | L | C | L | C |

*(Nota: $P_1$ llega en $t=0$ y finaliza en $t=7$. $P_2$ llega en $t=1$ y finaliza en $t=8$).*

**Consignas:**
a) Calcule el tiempo de retorno de cada proceso y el tiempo medio de retorno ($\bar{T}_R$).  
b) Calcule el tiempo de espera de cada proceso y el tiempo medio de espera ($\bar{T}_E$).  
c) Calcule el porcentaje de utilización de la CPU (entre $t=0$ y $t=8$).  
d) Describa la secuencia de transiciones de estados por las que pasa el proceso $P_1$ desde su llegada hasta su finalización.  

---
<!-- PAGEBREAK -->

# 🔑 RESOLUCIÓN DE LOS EXÁMENES

## 📌 Respuestas: Modelo de Examen Nº 1

### Parte 1: Teoría

#### 1. Filosofía del Software
* **Diferencia filosófica:** El Software Libre (impulsado por Richard Stallman) posee un enfoque **ético y social** centrado en garantizar la libertad de los usuarios para ejecutar, estudiar, modificar y redistribuir el código. El Código Abierto (propuesto por Eric Raymond y Linus Torvalds) adopta un enfoque **práctico y técnico/comercial**, destacando los beneficios metodológicos del modelo de desarrollo (calidad, corrección rápida de errores y estabilidad).
* **Copyleft:** Es una regla legal implementada a través de licencias (como la GNU GPL) que utiliza los derechos de autor para otorgar libertades al usuario con la condición estricta de que cualquier versión derivada o modificada conserve exactas y mismas libertades (prohibiendo su privatización).

#### 2. Procesos e Hilos
* **Diferencia fundamental:** Un Proceso es la unidad básica de **asignación de recursos** e independencia; posee su propio espacio de direcciones virtuales, tablas de páginas y Bloque de Control de Proceso (BCP). Un Hilo (Thread) es la unidad básica de **ejecución de CPU**; vive dentro de un proceso y comparte con los demás hilos de ese mismo proceso el espacio de direcciones, el código, los datos globales y los recursos E/S, conservando únicamente su propio contador de programa (PC), registros y pila.
* **Cambio de contexto:** Es significativamente más rápido entre hilos de un mismo proceso porque no requiere cambiar las tablas de páginas en el hardware de la MMU (Memory Management Unit) ni invalidar la memoria caché TLB (Translation Lookaside Buffer).

#### 3. Concurrencia
* **Condición de Carrera:** Ocurre cuando dos o más procesos/hilos acceden y manipulan datos compartidos simultáneamente, haciendo que el resultado final dependa del orden arbitrario en que la CPU ejecuta sus instrucciones.
* **Deadlock vs. Inanición:** En un Deadlock (Interbloqueo), dos o más procesos están bloqueados mutuamente esperando un recurso que el otro posee, alcanzando una **espera pasiva permanente** donde ningún proceso avanza. En la Inanición (Starvation), el sistema en su conjunto continúa funcionando y procesando trabajo, pero un proceso en particular es postergado de forma indefinida por el planificador debido a prioridades o políticas desfavorables.

#### 4. Gestión de Memoria
* **Paginación vs. Segmentación:** La Paginación divide la memoria física y el programa en bloques de **tamaño fijo** (marcos y páginas), de forma transparente para el programador. La Segmentación divide la memoria en bloques de **tamaño variable** reflejando la estructura lógica y funcional del programa (código, datos, pila, funciones).
* **Fragmentación:** La Paginación únicamente produce fragmentación interna (desperdicio en la última página de cada proceso). La Segmentación produce fragmentación externa (huecos libres disjuntos de memoria RAM que resultan insuficientes o dispersos para alojar nuevos segmentos).

---

### Parte 2: Ejercicio Práctico (Gantt 1)

#### a) Tiempos de Retorno ($T_R = t_{\text{fin}} - t_{\text{llegada}}$)
* **Proceso $P_1$:** Finaliza en $t = 9$, llegó en $t = 0 \rightarrow T_R(P_1) = 9 - 0 = 9 \text{ ut}$.
* **Proceso $P_2$:** Finaliza en $t = 11$, llegó en $t = 1 \rightarrow T_R(P_2) = 11 - 1 = 10 \text{ ut}$.

**Tiempo Medio de Retorno ($\bar{T}_R$):**
$$\bar{T}_R = \frac{T_R(P_1) + T_R(P_2)}{2} = \frac{9 + 10}{2} = 9{,}5 \text{ ut}$$

#### b) Tiempos de Espera ($T_E = \text{total de instantes en cola de listos 'L'}$)
* **Proceso $P_1$:** Permanece en `L` durante 2 instantes (instantes 4 y 5) $\rightarrow T_E(P_1) = 2 \text{ ut}$.
* **Proceso $P_2$:** Permanece en `L` durante 4 instantes (instantes 1, 2, 7 y 8) $\rightarrow T_E(P_2) = 4 \text{ ut}$.

**Tiempo Medio de Espera ($\bar{T}_E$):**
$$\bar{T}_E = \frac{T_E(P_1) + T_E(P_2)}{2} = \frac{2 + 4}{2} = 3{,}0 \text{ ut}$$

#### c) Porcentaje de Utilización de la CPU (entre $t=0$ y $t=11$)
* **Tiempo total del sistema:** $11 \text{ ut}$ (desde $t=0$ a $t=11$).
* **Instantes con CPU ocupada ('C'):** $9 \text{ ut}$ (instantes 0, 1, 3, 4, 5, 6, 8, 9 y 10).
* **Instantes con CPU ociosa:** $2 \text{ ut}$ (instantes 2 y 7, donde los procesos están en E/S o listos).

**Porcentaje de Utilización:**
$$\text{Utilización CPU} = \left( \frac{\text{Instantes Ocupados}}{\text{Tiempo Total}} \right) \times 100\% = \left( \frac{9}{11} \right) \times 100\% \approx 81{,}82\%$$

#### d) Secuencia de Transiciones de Estados del Proceso $P_1$
1. **`Nuevo` $\rightarrow$ `Listo`:** En $t=0$, el proceso $P_1$ es admitido en el sistema.
2. **`Listo` $\rightarrow$ `Ejecución`:** En $t=0$, el planificador le asigna la CPU de $t=0$ a $t=2$ (instantes 0 y 1).
3. **`Ejecución` $\rightarrow$ `Bloqueado`:** En $t=2$, $P_1$ solicita acceso al Disco y se bloquea de $t=2$ a $t=4$ (instantes 2 y 3).
4. **`Bloqueado` $\rightarrow$ `Listo`:** En $t=4$, finaliza la E/S de Disco y pasa a la cola de listos de $t=4$ a $t=6$ (instantes 4 y 5).
5. **`Listo` $\rightarrow$ `Ejecución`:** En $t=6$, se le asigna la CPU de $t=6$ a $t=7$ (instante 6).
6. **`Ejecución` $\rightarrow$ `Bloqueado`:** En $t=7$, $P_1$ solicita la Impresora y se bloquea de $t=7$ a $t=8$ (instante 7).
7. **`Bloqueado` $\rightarrow$ `Listo` $\rightarrow$ `Ejecución`:** En $t=8$, concluye la impresión; al estar la CPU libre en ese instante, pasa a listo y es despachado de inmediato a ejecución de $t=8$ a $t=9$ (instante 8).
8. **`Ejecución` $\rightarrow$ `Finalizado`:** En $t=9$, completa sus instrucciones y abandona el sistema.

---
<!-- PAGEBREAK -->

## 📌 Respuestas: Modelo de Examen Nº 2

### Parte 1: Teoría

#### 1. Definición de Sistema Operativo
* **Según Richard Stallman:** Es la capa integral de software encargada de gestionar el hardware y permitir el funcionamiento de los programas de aplicación. Los elementos mínimos que lo componen incluyen el Kernel (núcleo), el compilador, depuradores, editores de texto, formateadores y herramientas de administración.
* **Monolítico vs. Microkernel:** Un Kernel Monolítico ejecuta todos los servicios del SO (planificador, sistemas de archivos, drivers) en un único espacio de direcciones en modo núcleo. Un Microkernel (HURD) reduce el núcleo a las funciones indispensables (comunicación IPC, gestión de memoria básica y hilos) y ejecuta los demás servicios como servidores independientes en modo usuario.

#### 2. Estados de un Proceso
* **Listo vs. Espera/Bloqueado:** En el estado Listo (Ready), el proceso reside en memoria principal con todos sus recursos asignados, aguardando únicamente la asignación de la CPU. En el estado Bloqueado (Blocked), el proceso está a la espera de que ocurra un evento externo o finalice una operación de E/S, por lo que libera la CPU para otros procesos.
* **Pila del Sistema (Pila del Núcleo):** Se utiliza una pila de núcleo separada para garantizar el aislamiento y la seguridad del sistema operativo. Esto evita que código malicioso o errores de programas de usuario (como un *stack overflow*) corrompan las estructuras internas del núcleo durante el tratamiento de interrupciones y llamadas al sistema.

#### 3. Suspensión e Intercambio
* **Swapping:** Es el mecanismo mediante el cual el SO desplaza temporalmente la imagen de un proceso desde la memoria RAM hacia un espacio secundario en disco (área de intercambio/swap). Se implementa cuando la memoria física está saturada y existen procesos bloqueados consumiendo RAM.
* **Ubicación e Información:** La imagen completa del espacio de direcciones del proceso pasa al disco, pero el SO conserva el BCP (Bloque de Control de Proceso) en la memoria RAM para mantener la trazabilidad y estado del proceso.

#### 4. Memoria Virtual
* **Conjunto Residente:** Es el subconjunto de páginas de un proceso que se encuentran efectivamente cargadas en marcos de la memoria RAM en un instante dado. Permite maximizar el grado de multiprogramación sin necesidad de cargar la totalidad del programa en memoria.
* **Thrashing (Hiperpaginación):** Es una condición crítica donde la CPU dedica la mayor parte del tiempo al intercambio (*swapping*) de páginas entre la RAM y el disco en lugar de ejecutar instrucciones útiles. Ocurre cuando la suma de los conjuntos residentes de los procesos activos supera la capacidad total de la memoria RAM disponible.

---

### Parte 2: Ejercicio Práctico (Gantt 2)

#### a) Tiempos de Retorno ($T_R = t_{\text{fin}} - t_{\text{llegada}}$)
* **Proceso $P_1$:** Finaliza en $t = 8$, llegó en $t = 0 \rightarrow T_R(P_1) = 8 - 0 = 8 \text{ ut}$.
* **Proceso $P_2$:** Finaliza en $t = 9$, llegó en $t = 1 \rightarrow T_R(P_2) = 9 - 1 = 8 \text{ ut}$.

**Tiempo Medio de Retorno ($\bar{T}_R$):**
$$\bar{T}_R = \frac{T_R(P_1) + T_R(P_2)}{2} = \frac{8 + 8}{2} = 8{,}0 \text{ ut}$$

#### b) Tiempos de Espera ($T_E = \text{total de instantes en cola de listos 'L'}$)
* **Proceso $P_1$:** Permanece en `L` durante 2 instantes (instantes 1 y 5) $\rightarrow T_E(P_1) = 2 \text{ ut}$.
* **Proceso $P_2$:** Permanece en `L` durante 3 instantes (instantes 2, 6 y 7) $\rightarrow T_E(P_2) = 3 \text{ ut}$.

**Tiempo Medio de Espera ($\bar{T}_E$):**
$$\bar{T}_E = \frac{T_E(P_1) + T_E(P_2)}{2} = \frac{2 + 3}{2} = 2{,}5 \text{ ut}$$

#### c) Porcentaje de Utilización de la CPU (entre $t=0$ y $t=9$)
* **Tiempo total del sistema:** $9 \text{ ut}$ (desde $t=0$ a $t=9$).
* **Instantes con CPU ocupada ('C'):** $8 \text{ ut}$ (instantes 0, 1, 2, 3, 4, 6, 7 y 8).
* **Instantes con CPU ociosa:** $1 \text{ ut}$ (instante 5, donde $P_1$ está en listos y $P_2$ en la Impresora).

**Porcentaje de Utilización:**
$$\text{Utilización CPU} = \left( \frac{\text{Instantes Ocupados}}{\text{Tiempo Total}} \right) \times 100\% = \left( \frac{8}{9} \right) \times 100\% \approx 88{,}89\%$$

#### d) Secuencia de Transiciones de Estados del Proceso $P_2$
1. **`Nuevo` $\rightarrow$ `Listo`:** En $t=1$, el proceso $P_2$ ingresa al sistema.
2. **`Listo` $\rightarrow$ `Ejecución`:** En $t=1$, se le asigna la CPU de $t=1$ a $t=2$ (instante 1).
3. **`Ejecución` $\rightarrow$ `Listo`:** En $t=2$, es desalojado por el planificador (retoma $P_1$) y aguarda en la cola de listos de $t=2$ a $t=3$ (instante 2).
4. **`Listo` $\rightarrow$ `Ejecución`:** En $t=3$, retoma la CPU de $t=3$ a $t=5$ (instantes 3 y 4).
5. **`Ejecución` $\rightarrow$ `Bloqueado`:** En $t=5$, solicita la Impresora y se bloquea de $t=5$ a $t=6$ (instante 5).
6. **`Bloqueado` $\rightarrow$ `Listo`:** En $t=6$, finaliza la E/S de la Impresora y espera en la cola de listos de $t=6$ a $t=8$ (instantes 6 y 7).
7. **`Listo` $\rightarrow$ `Ejecución`:** En $t=8$, se le asigna la CPU de $t=8$ a $t=9$ (instante 8).
8. **`Ejecución` $\rightarrow$ `Finalizado`:** En $t=9$, concluye sus instrucciones y abandona el sistema.

---
<!-- PAGEBREAK -->

## 📌 Respuestas: Modelo de Examen Nº 3

### Parte 1: Teoría

#### 1. Modelos de Desarrollo
* **La Catedral y el Bazar:** Eric Raymond contrapone dos filosofías de desarrollo de software: la Catedral, que representa un desarrollo cerrado, centralizado, jerárquico y con entregas distanciadas entre sí; y el Bazar, que representa un desarrollo público, descentralizado, con constantes actualizaciones y una revisión comunitaria masiva de código (*"Dado un número suficiente de ojos, todos los errores son superficiales"*).
* **Riesgos del monopolio:** Que una entidad controle o altere estándares abiertos (*Adopt, Extend, Extinguish*) genera dependencia forzada (*lock-in*), inhibe la innovación, atenta contra la interoperabilidad e impone costos arbitrarios a usuarios y desarrolladores.

#### 2. Estructuras de Control del SO
* **BCP (Bloque de Control de Proceso):** Es la estructura de datos fundamental del SO que representa a un proceso en memoria. Posee un tamaño estático para permitir un acceso, indexación y cambio de contexto eficiente por parte del sistema operativo. Almacena la identificación (PID), estado, registros de CPU, contador de programa (PC), prioridades y límites de memoria.
* **Cuatro tablas de control principales:**
  1. **Tabla de Procesos:** Administra el estado y los BCPs de todos los procesos.
  2. **Tabla de Memoria:** Gestiona marcos, páginas y particiones asignadas y libres.
  3. **Tabla de E/S:** Controla los dispositivos, canales y peticiones pendientes.
  4. **Tabla de Archivos:** Administra los archivos abiertos, descriptores y permisos.

#### 3. Particionamiento de Memoria
* **Particionamiento Fijo vs. Dinámico:** El Particionamiento Fijo divide la memoria en regiones estáticas creadas durante la inicialización del sistema. El Particionamiento Dinámico crea particiones bajo demanda en tiempo de ejecución con el tamaño exacto solicitado por el proceso.
* **Compactación:** Resuelve la fragmentación externa en el particionamiento dinámico mediante el desplazamiento continuo en memoria de los procesos activos para agrupar todos los bloques libres dispersos en una única región contigua de RAM.

#### 4. Reemplazo de Páginas
* **Algoritmos de Reemplazo:**
  * FIFO: Expulsa la página que lleva más tiempo cargada en la memoria RAM, independientemente de la frecuencia de su uso.
  * LRU: Expulsa la página que no ha sido referenciada ni utilizada durante el período de tiempo más prolongado.
  * Algoritmo del Reloj (Clock): Implementación circular eficiente de LRU mediante un puntero y un "bit de uso"; si el bit es 1, le otorga una segunda oportunidad (pone el bit en 0 y avanza), y si es 0, la selecciona para reemplazo.
* **Bloqueo de Marcos (Frame Locking):** Es indispensable para evitar que el algoritmo de reemplazo expulse páginas críticas que contienen estructuras del kernel, rutinas de tratamiento de interrupciones o buffers de E/S en pleno procesamiento por hardware.

---

### Parte 2: Ejercicio Práctico (Gantt 3)

#### a) Tiempos de Retorno ($T_R = t_{\text{fin}} - t_{\text{llegada}}$)
* **Proceso $P_1$:** Finaliza en $t = 7$, llegó en $t = 0 \rightarrow T_R(P_1) = 7 - 0 = 7 \text{ ut}$.
* **Proceso $P_2$:** Finaliza en $t = 8$, llegó en $t = 1 \rightarrow T_R(P_2) = 8 - 1 = 7 \text{ ut}$.

**Tiempo Medio de Retorno ($\bar{T}_R$):**
$$\bar{T}_R = \frac{T_R(P_1) + T_R(P_2)}{2} = \frac{7 + 7}{2} = 7{,}0 \text{ ut}$$

#### b) Tiempos de Espera ($T_E = \text{total de instantes en cola de listos 'L'}$)
* **Proceso $P_1$:** Permanece en `L` durante 2 instantes (instantes 3 y 5) $\rightarrow T_E(P_1) = 2 \text{ ut}$.
* **Proceso $P_2$:** Permanece en `L` durante 3 instantes (instantes 1, 4 y 6) $\rightarrow T_E(P_2) = 3 \text{ ut}$.

**Tiempo Medio de Espera ($\bar{T}_E$):**
$$\bar{T}_E = \frac{T_E(P_1) + T_E(P_2)}{2} = \frac{2 + 3}{2} = 2{,}5 \text{ ut}$$

#### c) Porcentaje de Utilización de la CPU (entre $t=0$ y $t=8$)
* **Tiempo total del sistema:** $8 \text{ ut}$ (desde $t=0$ a $t=8$).
* **Instantes con CPU ocupada ('C'):** $8 \text{ ut}$ (instantes 0, 1, 2, 3, 4, 5, 6 y 7).
* **Instantes con CPU ociosa:** $0 \text{ ut}$ (la CPU se mantiene trabajando al 100% de la capacidad).

**Porcentaje de Utilización:**
$$\text{Utilización CPU} = \left( \frac{\text{Instantes Ocupados}}{\text{Tiempo Total}} \right) \times 100\% = \left( \frac{8}{8} \right) \times 100\% = 100\%$$

#### d) Secuencia de Transiciones de Estados del Proceso $P_1$
1. **`Nuevo` $\rightarrow$ `Listo`:** En $t=0$, el proceso $P_1$ es admitido en el sistema.
2. **`Listo` $\rightarrow$ `Ejecución`:** En $t=0$, se le asigna la CPU de $t=0$ a $t=2$ (instantes 0 y 1).
3. **`Ejecución` $\rightarrow$ `Bloqueado`:** En $t=2$, $P_1$ solicita acceso al Disco y se bloquea de $t=2$ a $t=3$ (instante 2).
4. **`Bloqueado` $\rightarrow$ `Listo`:** En $t=3$, finaliza la E/S de Disco y aguarda en la cola de listos de $t=3$ a $t=4$ (instante 3).
5. **`Listo` $\rightarrow$ `Ejecución`:** En $t=4$, retoma la CPU de $t=4$ a $t=5$ (instante 4).
6. **`Ejecución` $\rightarrow$ `Listo`:** En $t=5$, es desalojado por el planificador (para dar paso a $P_2$) de $t=5$ a $t=6$ (instante 5).
7. **`Listo` $\rightarrow$ `Ejecución`:** En $t=6$, retoma la CPU de $t=6$ a $t=7$ (instante 6).
8. **`Ejecución` $\rightarrow$ `Finalizado`:** En $t=7$, concluye sus instrucciones y abandona el sistema.

---
> 💡 *Documento formateado y verificado para generación de PDF mediante el conversor.*
