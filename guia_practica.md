# 📝 Guía Práctica de Sistemas Operativos: 10 Ejercicios Resueltos y Variados

---

**Materia:** Sistemas Operativos  
**Carrera:** Licenciatura en Sistemas de Información  
**Institución:** Universidad Autónoma de Entre Ríos (UADER)  
**Alumno:** Jenaro Galdini  
**Fecha:** Agosto 2026  

<!-- TOC -->

<!-- PAGEBREAK -->

## 1. Planificación de Procesos (Ejercicio Adaptado y Corregido)

Un sistema dispone de **1 CPU**, **1 Disco** y **1 Impresora**. Los dispositivos de E/S son exclusivos (no compartidos) y planificados mediante **FCFS**. La CPU utiliza una política **Round Robin** con expulsión y Quantum $q = 2\text{ ut}$.

Se ejecutan tres procesos con la siguiente secuencia de ráfagas:
* **P1:** Llega en $t=0$. Ráfagas: `3 CPU, 2 Disco, 2 CPU, 2 Impresora, 1 CPU`
* **P2:** Llega en $t=1$. Ráfagas: `2 CPU, 1 Disco, 2 CPU, 1 Impresora, 2 CPU`
* **P3:** Llega en $t=2$. Ráfagas: `4 CPU, 2 Disco, 1 CPU`

---

### 📊 Diagrama de Gantt de Ejecución

> **Simbología y Estados:**  
> <span style="background-color: #a7f3d0; color: #064e3b; padding: 2px 8px; border-radius: 4px; font-weight: bold;">C</span> **CPU** &nbsp;|&nbsp; 
> <span style="background-color: #fca5a5; color: #7f1d1d; padding: 2px 8px; border-radius: 4px; font-weight: bold;">D</span> **Disco** &nbsp;|&nbsp; 
> <span style="background-color: #a5b4fc; color: #1e1b4b; padding: 2px 8px; border-radius: 4px; font-weight: bold;">I</span> **Impresora** &nbsp;|&nbsp; 
> <span style="background-color: #fde047; color: #713f12; padding: 2px 8px; border-radius: 4px; font-weight: bold;">L</span> **Cola de Listos**

<table style="width: 100%; table-layout: fixed; border-collapse: collapse; font-size: 10px; text-align: center; margin: 12px 0;">
  <thead>
    <tr style="background-color: #f3f4f6;">
      <th style="border: 1px solid #d1d5db; padding: 3px; width: 7%; font-weight: bold;">P / t</th>
      <th style="border: 1px solid #d1d5db; padding: 3px;">0</th>
      <th style="border: 1px solid #d1d5db; padding: 3px;">1</th>
      <th style="border: 1px solid #d1d5db; padding: 3px;">2</th>
      <th style="border: 1px solid #d1d5db; padding: 3px;">3</th>
      <th style="border: 1px solid #d1d5db; padding: 3px;">4</th>
      <th style="border: 1px solid #d1d5db; padding: 3px;">5</th>
      <th style="border: 1px solid #d1d5db; padding: 3px;">6</th>
      <th style="border: 1px solid #d1d5db; padding: 3px;">7</th>
      <th style="border: 1px solid #d1d5db; padding: 3px;">8</th>
      <th style="border: 1px solid #d1d5db; padding: 3px;">9</th>
      <th style="border: 1px solid #d1d5db; padding: 3px;">10</th>
      <th style="border: 1px solid #d1d5db; padding: 3px;">11</th>
      <th style="border: 1px solid #d1d5db; padding: 3px;">12</th>
      <th style="border: 1px solid #d1d5db; padding: 3px;">13</th>
      <th style="border: 1px solid #d1d5db; padding: 3px;">14</th>
      <th style="border: 1px solid #d1d5db; padding: 3px;">15</th>
      <th style="border: 1px solid #d1d5db; padding: 3px;">16</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #d1d5db; padding: 4px; font-weight: bold; background-color: #dbeafe; color: #1e40af;">P1</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #a7f3d0; color: #064e3b; font-weight: bold;">C</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #a7f3d0; color: #064e3b; font-weight: bold;">C</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #fde047; color: #713f12; font-weight: bold;">L</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #fde047; color: #713f12; font-weight: bold;">L</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #a7f3d0; color: #064e3b; font-weight: bold;">C</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #fca5a5; color: #7f1d1d; font-weight: bold;">D</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #fca5a5; color: #7f1d1d; font-weight: bold;">D</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #fde047; color: #713f12; font-weight: bold;">L</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #fde047; color: #713f12; font-weight: bold;">L</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #fde047; color: #713f12; font-weight: bold;">L</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #fde047; color: #713f12; font-weight: bold;">L</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #a7f3d0; color: #064e3b; font-weight: bold;">C</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #a7f3d0; color: #064e3b; font-weight: bold;">C</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #a5b4fc; color: #1e1b4b; font-weight: bold;">I</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #a5b4fc; color: #1e1b4b; font-weight: bold;">I</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #fde047; color: #713f12; font-weight: bold;">L</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #a7f3d0; color: #064e3b; font-weight: bold;">C</td>
    </tr>
    <tr>
      <td style="border: 1px solid #d1d5db; padding: 4px; font-weight: bold; background-color: #fef3c7; color: #92400e;">P2</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #f9fafb;"></td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #fde047; color: #713f12; font-weight: bold;">L</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #a7f3d0; color: #064e3b; font-weight: bold;">C</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #a7f3d0; color: #064e3b; font-weight: bold;">C</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #fca5a5; color: #7f1d1d; font-weight: bold;">D</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #fde047; color: #713f12; font-weight: bold;">L</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #fde047; color: #713f12; font-weight: bold;">L</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #a7f3d0; color: #064e3b; font-weight: bold;">C</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #a7f3d0; color: #064e3b; font-weight: bold;">C</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #a5b4fc; color: #1e1b4b; font-weight: bold;">I</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #fde047; color: #713f12; font-weight: bold;">L</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #fde047; color: #713f12; font-weight: bold;">L</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #fde047; color: #713f12; font-weight: bold;">L</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #a7f3d0; color: #064e3b; font-weight: bold;">C</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #a7f3d0; color: #064e3b; font-weight: bold;">C</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #f9fafb;"></td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #f9fafb;"></td>
    </tr>
    <tr>
      <td style="border: 1px solid #d1d5db; padding: 4px; font-weight: bold; background-color: #dcfce7; color: #166534;">P3</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #f9fafb;"></td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #f9fafb;"></td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #fde047; color: #713f12; font-weight: bold;">L</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #fde047; color: #713f12; font-weight: bold;">L</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #fde047; color: #713f12; font-weight: bold;">L</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #a7f3d0; color: #064e3b; font-weight: bold;">C</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #a7f3d0; color: #064e3b; font-weight: bold;">C</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #fde047; color: #713f12; font-weight: bold;">L</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #fde047; color: #713f12; font-weight: bold;">L</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #a7f3d0; color: #064e3b; font-weight: bold;">C</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #a7f3d0; color: #064e3b; font-weight: bold;">C</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #fca5a5; color: #7f1d1d; font-weight: bold;">D</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #fca5a5; color: #7f1d1d; font-weight: bold;">D</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #fde047; color: #713f12; font-weight: bold;">L</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #fde047; color: #713f12; font-weight: bold;">L</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #a7f3d0; color: #064e3b; font-weight: bold;">C</td>
      <td style="border: 1px solid #d1d5db; padding: 3px; background-color: #f9fafb;"></td>
    </tr>
  </tbody>
</table>

> [!NOTE]
> **Tiempos de finalización:** $P_1$ finaliza en $t=17$, $P_2$ finaliza en $t=15$ y $P_3$ finaliza en $t=16$.

---

### ❓ Consignas

a) **Calcule el tiempo medio de retorno ($\bar{T}_R$).**  
b) **Calcule el tiempo medio de espera ($\bar{T}_E$).**  
c) **Calcule el porcentaje de utilización de CPU en el intervalo $[0; 17)$.**  
d) **Describa textualmente el diagrama de estados por los que pasa el proceso P2 desde su llegada.**

<!-- PAGEBREAK -->

## 2. Planificación de Procesos: Construcción de Gantt

Se tiene un sistema con **1 CPU** y **1 Disco**. Se utiliza planificación **Round Robin** con $q = 3\text{ ut}$ para la CPU y **FCFS** para el Disco.

Llegan los siguientes procesos:
* **P1:** Llega en $t=0$. Ráfagas: `4 CPU, 2 Disco, 2 CPU`.
* **P2:** Llega en $t=1$. Ráfagas: `2 CPU, 3 Disco, 1 CPU`.
* **P3:** Llega en $t=2$. Ráfagas: `5 CPU`.

---

### ❓ Consignas

a) **Construya la tabla de traza de ejecución (Diagrama de Gantt).**  
b) **Calcule el Tiempo de Retorno para P3 ($T_R(P_3)$).**  
c) **Determine el tiempo ocioso del Disco en el intervalo $[0; 15)$.**

<!-- PAGEBREAK -->

## 3. Asignación de Memoria: Primer y Mejor Ajuste

Un sistema gestiona su memoria mediante particionamiento dinámico y actualmente posee los siguientes huecos libres (en el orden dado):  
`100 KB, 500 KB, 200 KB, 300 KB, 600 KB`

Llegan secuencialmente los siguientes procesos solicitando memoria:
* <span style="color: #2563eb; font-weight: bold;">PA:</span> 212 KB
* <span style="color: #059669; font-weight: bold;">PB:</span> 417 KB
* <span style="color: #d97706; font-weight: bold;">PC:</span> 112 KB
* <span style="color: #dc2626; font-weight: bold;">PD:</span> 426 KB

---

### ❓ Consignas

a) **Asigne los procesos utilizando el algoritmo Primer Ajuste (First Fit).**  
b) **Asigne los procesos utilizando el algoritmo Mejor Ajuste (Best Fit).**  
c) **Indique cuál de los dos algoritmos logró ubicar a todos los procesos (si alguno lo hizo).**

---

## 4. Asignación de Memoria: Peor Ajuste y Fragmentación Externa

Utilizando la misma lista de huecos iniciales del ejercicio anterior:  
`100 KB, 500 KB, 200 KB, 300 KB, 600 KB`

Llegan los procesos:
* <span style="color: #2563eb; font-weight: bold;">PX:</span> 150 KB
* <span style="color: #059669; font-weight: bold;">PY:</span> 250 KB
* <span style="color: #d97706; font-weight: bold;">PZ:</span> 100 KB

---

### ❓ Consignas

a) **Aplique el algoritmo Peor Ajuste (Worst Fit).**  
b) **Calcule la cantidad de memoria libre total restante al finalizar las asignaciones.**  
c) **Defina conceptualmente qué tipo de fragmentación está sufriendo esta memoria.**

<!-- PAGEBREAK -->

## 5. Paginación: Cálculo de Páginas y Fragmentación Interna

Un sistema operativo implementa memoria virtual paginada con un tamaño de página de **4 KB**.

En el sistema se están por cargar dos procesos:
* **Proceso Alfa:** 18.5 MB
* **Proceso Beta:** 2050 KB

---

### ❓ Consignas

a) **Calcule la cantidad exacta de páginas que requerirá cada proceso.** *(Nota: $1\text{ MB} = 1024\text{ KB}$)*.  
b) **Calcule la fragmentación interna (en bytes o KB) que generará el Proceso Beta en su última página.**

---

## 6. Dimensionamiento de la Tabla de Páginas

Un sistema con arquitectura de **32 bits** utiliza un tamaño de página de **8 KB** ($8192\text{ bytes}$). Cada entrada en la tabla de páginas (PTE) ocupa **4 bytes**.

---

### ❓ Consignas

a) **Determine el número máximo de páginas que puede direccionar teóricamente este sistema.**  
b) **Si un proceso específico ocupa 40 MB, ¿qué tamaño en KB tendrá la tabla de páginas de este proceso en la memoria principal?**

<!-- PAGEBREAK -->

## 7. Traducción de Direcciones Lógicas a Físicas (Éxito)

En un sistema con tamaño de página de **2 KB** ($2048\text{ bytes}$), se tiene la siguiente porción de la Tabla de Páginas de un proceso:

| Página ($p$) | Marco ($m$) | Bit Residente |
| :---: | :---: | :---: |
| **0** | 5 | 1 |
| **1** | 8 | 1 |
| **2** | - | 0 |
| **3** | 2 | 1 |

La CPU emite la dirección lógica decimal: **$L = 6500$**.

---

### ❓ Consignas

a) **Descomponga la dirección lógica en número de página ($p$) y desplazamiento ($d$).**  
b) **Calcule la Dirección Física ($DF$) resultante en formato decimal.**

---

## 8. Traducción de Direcciones: Fallos de Página y Segmentación

Utilizando el mismo sistema y la Tabla de Páginas del Ejercicio 7.

---

### ❓ Consignas

a) **¿Qué sucede si la CPU intenta acceder a la dirección lógica $L = 5000$? Describa el procedimiento que ejecutará el SO.**  
b) **¿Qué sucede si el tamaño total del proceso es de 4 páginas (de la 0 a la 3) y la CPU intenta acceder a la dirección lógica $L = 9500$?**

<!-- PAGEBREAK -->

## 9. Análisis de Utilización de Recursos

Observe la siguiente traza parcial de ejecución de dos procesos en un sistema simple (**1 CPU**, **1 Disco**):

<table style="width: 100%; table-layout: fixed; border-collapse: collapse; font-size: 11px; text-align: center; margin: 12px 0;">
  <thead>
    <tr style="background-color: #f3f4f6;">
      <th style="border: 1px solid #d1d5db; padding: 4px; width: 10%; font-weight: bold;">P / t</th>
      <th style="border: 1px solid #d1d5db; padding: 4px;">0</th>
      <th style="border: 1px solid #d1d5db; padding: 4px;">1</th>
      <th style="border: 1px solid #d1d5db; padding: 4px;">2</th>
      <th style="border: 1px solid #d1d5db; padding: 4px;">3</th>
      <th style="border: 1px solid #d1d5db; padding: 4px;">4</th>
      <th style="border: 1px solid #d1d5db; padding: 4px;">5</th>
      <th style="border: 1px solid #d1d5db; padding: 4px;">6</th>
      <th style="border: 1px solid #d1d5db; padding: 4px;">7</th>
      <th style="border: 1px solid #d1d5db; padding: 4px;">8</th>
      <th style="border: 1px solid #d1d5db; padding: 4px;">9</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #d1d5db; padding: 4px; font-weight: bold; background-color: #dbeafe; color: #1e40af;">P1</td>
      <td style="border: 1px solid #d1d5db; padding: 4px; background-color: #a7f3d0; color: #064e3b; font-weight: bold;">C</td>
      <td style="border: 1px solid #d1d5db; padding: 4px; background-color: #a7f3d0; color: #064e3b; font-weight: bold;">C</td>
      <td style="border: 1px solid #d1d5db; padding: 4px; background-color: #fca5a5; color: #7f1d1d; font-weight: bold;">D</td>
      <td style="border: 1px solid #d1d5db; padding: 4px; background-color: #fca5a5; color: #7f1d1d; font-weight: bold;">D</td>
      <td style="border: 1px solid #d1d5db; padding: 4px; background-color: #fde047; color: #713f12; font-weight: bold;">L</td>
      <td style="border: 1px solid #d1d5db; padding: 4px; background-color: #a7f3d0; color: #064e3b; font-weight: bold;">C</td>
      <td style="border: 1px solid #d1d5db; padding: 4px; background-color: #f9fafb;"></td>
      <td style="border: 1px solid #d1d5db; padding: 4px; background-color: #f9fafb;"></td>
      <td style="border: 1px solid #d1d5db; padding: 4px; background-color: #f9fafb;"></td>
      <td style="border: 1px solid #d1d5db; padding: 4px; background-color: #f9fafb;"></td>
    </tr>
    <tr>
      <td style="border: 1px solid #d1d5db; padding: 4px; font-weight: bold; background-color: #fef3c7; color: #92400e;">P2</td>
      <td style="border: 1px solid #d1d5db; padding: 4px; background-color: #f9fafb;"></td>
      <td style="border: 1px solid #d1d5db; padding: 4px; background-color: #fde047; color: #713f12; font-weight: bold;">L</td>
      <td style="border: 1px solid #d1d5db; padding: 4px; background-color: #a7f3d0; color: #064e3b; font-weight: bold;">C</td>
      <td style="border: 1px solid #d1d5db; padding: 4px; background-color: #fde047; color: #713f12; font-weight: bold;">L</td>
      <td style="border: 1px solid #d1d5db; padding: 4px; background-color: #a7f3d0; color: #064e3b; font-weight: bold;">C</td>
      <td style="border: 1px solid #d1d5db; padding: 4px; background-color: #fca5a5; color: #7f1d1d; font-weight: bold;">D</td>
      <td style="border: 1px solid #d1d5db; padding: 4px; background-color: #fca5a5; color: #7f1d1d; font-weight: bold;">D</td>
      <td style="border: 1px solid #d1d5db; padding: 4px; background-color: #fca5a5; color: #7f1d1d; font-weight: bold;">D</td>
      <td style="border: 1px solid #d1d5db; padding: 4px; background-color: #a7f3d0; color: #064e3b; font-weight: bold;">C</td>
      <td style="border: 1px solid #d1d5db; padding: 4px; background-color: #a7f3d0; color: #064e3b; font-weight: bold;">C</td>
    </tr>
  </tbody>
</table>

---

### ❓ Consignas

a) **Calcule el porcentaje de utilización de la CPU en el intervalo exacto $[0; 10)$.**  
b) **Calcule el tiempo ocioso del Disco en el mismo intervalo $[0; 10)$.**

---

## 10. Diagrama de Transición de Estados

Describa de forma secuencial y detallada todas las transiciones de estado (**Nuevo**, **Listo**, **Ejecución**, **Bloqueado**, **Terminado/Salir**) por las que atraviesa el **Proceso 1 (P1)** del Ejercicio 9, indicando en qué instante ($t$) ocurre cada transición.