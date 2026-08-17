# Trabajo Práctico N° 9: Planificación, Estimación y Modelos Económicos

**Materia:** Ingeniería en Sistemas II  
**Tema:** Mantenimiento, Programas, Estimación Sistémica, Rayleigh, Backlog, ROV y Finanzas de Software  
**Fecha:** Agosto 2026  

---

<!-- TOC -->

<!-- PAGEBREAK -->

## 1. Mantenimiento Continuo vs. Gestión como Proyecto

El ==mantenimiento continuo==(celeste) es una actividad operativa recurrente y permanente, por lo que estrictamente **no cumple** con la definición de un proyecto, el cual exige ser un esfuerzo temporario con principio y fin claros para crear un resultado único. 

Sin embargo, puede estructurarse y gestionarse como un proyecto incorporando las siguientes dimensiones:

* **Temporalidad y Acotación:** Agrupar tareas en paquetes de trabajo discretos —por ejemplo: *releases*, sprints, versiones— con fechas rígidas de inicio y finalización.
* **Objetivos SMART:** Definir metas Específicas, Medibles, Alcanzables, Realistas y Temporales —ejemplo: *"reducir en un 15% los defectos críticos reportados en el próximo trimestre"*—.
* **Recursos Dedicados:** Asignar un presupuesto acotado y un equipo de trabajo exclusivo durante dicho ciclo.

---

## 2. Estructuración de Iniciativas como Programas

Ciertas iniciativas complejas se estructuran como ==programas==(amarillo), es decir, un grupo coordinado de proyectos vinculados, en lugar de proyectos individuales debido a:

* **Escala y Complejidad:** El tamaño de la iniciativa supera la capacidad de control y seguimiento de un plan de proyecto único.
* **Interdependencia:** Permite coordinar proyectos que comparten recursos, dependencias tecnológicas y riesgos, obteniendo beneficios estratégicos que no se lograrían de forma aislada.
* **Enfoque de Ciclo de Vida:** Los proyectos son temporarios y transaccionales, mientras que los programas gestionan la ==evolución estratégica a largo plazo==(verde) de un producto o portafolio.

---

## 3. Fijación Arbitraria de Tiempo, Recursos y Requerimientos

En el ==modelo sistémico==(violeta) de ingeniería de software, las variables de proyecto no son independientes; están vinculadas por ecuaciones tecnológicas y organizacionales, como $E = \pi \cdot S^{\alpha}$ y $\tau = \kappa \cdot E^{\beta}$. 

> ==**Riesgo de Parálisis por Retrabajo:**==(rojo) Si se fijan arbitrariamente el Alcance, el Tiempo y los Recursos por *conveniencia comercial*, el sistema colapsa inevitablemente.

Los efectos directos son:

* **Degradación de la Calidad:** Al bloquear alcance, esfuerzo y plazos, la tensión del sistema se deriva hacia una acumulación descontrolada de ==Deuda Técnica==(naranja), provocando retrabajo y congelamiento del desarrollo.
* **Zona Imposible de Boehm:** Si se comprime el calendario más allá del límite práctico del 20% al 25%, agregar personal solo incrementa la carga de comunicación y reduce la productividad neta, conocido como la Ley de Brooks.
* **Fracaso del Proyecto:** Las estadísticas muestran que más del 70% de los proyectos con planificación no realista sufren retrasos severos o cancelaciones.

---

## 4. Ecuaciones Empíricas y Curvas de Esfuerzo vs. Tiempo Calendario

Se analizaron las ecuaciones empíricas de estimación:

$$E = 8 \cdot S^{0.95}$$

$$t_d = 2.4 \cdot E^{0.33}$$

Donde $E$ representa el Esfuerzo en Personas-Mes, abreviado PM, $S$ el tamaño del software en miles de líneas de código o unidades de tamaño, y $t_d$ el Tiempo Calendario en meses.

* **Curva de Esfuerzo:** Muestra un crecimiento con el tamaño del software en el intervalo $S \in [1000, 10000]$ unidades, alcanzando hasta ==$4,772$ PM==(naranja) para $10,000$ unidades.
* **Curva de Tiempo Calendario:** Evaluada en el intervalo $E \in [10, 5000]$ PM, evidencia rendimientos decrecientes al intentar acelerar el cronograma únicamente incrementando el esfuerzo dedicado.

<!-- PAGEBREAK -->

## 5. Priorización de Backlog y Orientación al Valor

Dada una capacidad disponible de ==15 Story Points==(celeste), en adelante SP, para un periodo de 6 semanas —3 sprints de 2 semanas—, se evaluó el backlog según el ratio de eficiencia de valor, es decir Hits sobre SP:

| Ítem | Story Points SP | Valor Hits/mes | Eficiencia Hits/SP | Prioridad |
| :---: | :---: | :---: | :---: | :---: |
| **F** | 2 | 2,179 | **1,089.5** | 1° |
| **C** | 8 | 6,602 | **825.3** | 2° |
| **G** | 13 | 8,030 | **617.7** | 3° |
| **B** | 3 | 1,762 | **587.3** | 4° |
| **A** | 2 | 1,104 | **552.0** | 5° |
| **D** | 5 | 1,565 | **313.0** | 6° |

### 5.1 Alcance Recomendado para 6 Semanas y 15 SP
Mediante optimización, Knapsack Algorithm, el alcance óptimo comprende la combinación de **F, C, B, A**:
* **Consumo total:** $2 + 8 + 3 + 2 = \mathbf{15\text{ SP}}$, 100% de la capacidad.
* **Valor entregado:** $\mathbf{11,647\text{ Hits/mes}}$, Valor Máximo Posible.
* *Quedan fuera:* G de 13 SP y D de 5 SP.

### 5.2 Reducción de Presupuesto a 3 Semanas
* **Con 1 Sprint Completo de 5 SP:** Se seleccionan **F de 2 SP** y **B de 3 SP** $\rightarrow$ **3,941 Hits**.
* **Con Proporcional Teórico para 7 SP:** Se seleccionan **F de 2 SP**, **B de 3 SP** y **A de 2 SP** $\rightarrow$ **5,045 Hits**, quedando fuera C de 8 SP por restricción de tamaño.

### 5.3 Extensión del Equipo a 3.5 Sprints
Dado que las entregas funcionales se realizan al finalizar cada sprint de 2 semanas, el alcance entregable en 7 semanas se mantiene en ==15 SP== correspondientes a los Sprints 1, 2 y 3. Los 2 SP remanentes del sprint incompleto no alcanzan para incorporar los ítems pendientes D o G debido a la granularidad del backlog.

### 5.4 Dependencia Técnica Crítica - Función 'D'
Si el Líder Técnico exige incluir la función **D de 5 SP** por arquitectura base como Must Have:
* **Items seleccionados:** **D de 5 SP** + **C de 8 SP** + **F de 2 SP** = **15 SP**.
* **Valor entregado:** $\mathbf{10,346\text{ Hits/mes}}$.
* **Costo de Oportunidad:** Pérdida de $1,301\text{ Hits/mes}$, lo que representa un -11.17% de valor al usuario, por desplazar B y A.

### 5.5 Impacto de la Deuda Técnica de 1 SP por Sprint
Si la deuda técnica consume $1\text{ SP/sprint}$, la velocidad neta baja a $4\text{ SP/sprint}$, sumando $12\text{ SP}$ totales en 6 semanas:
* **Alcance resultante:** **F de 2 SP** + **C de 8 SP** + **A de 2 SP** = **12 SP**.
* **Valor entregado:** $\mathbf{9,885\text{ Hits/mes}}$.
* **Consecuencia:** Se elimina el ítem **B de 3 SP**, evidenciando cómo la deuda técnica reduce la capacidad operativa y destruye valor económico directo.

<!-- PAGEBREAK -->

## 6. Perspectiva de Negocio para Desarrolladores

> **"What Do Software Developers Need to Know about Business" — Harrison**
> 
> * **Concepto Principal:** Los ingenieros no pueden trabajar aislados de las metas económicas de la empresa; el desarrollo de software es fundamentalmente la asignación de capital escaso. Cada decisión arquitectónica impacta de forma directa en los estados financieros, como OpEx y CapEx.
> * **Relevancia:** Fundamenta la necesidad de planificar el alcance alineando el valor percibido por los *stakeholders* con el costo real de ejecución técnica.

---

## 7. Consistencia Subjetiva en Estimaciones Ágiles

> **"Subjective Consistency" — Colla**
> 
> * **Concepto Principal:** Las estimaciones ágiles, como Story Points o Planning Poker, son subjetivas por naturaleza. Aunque la exactitud absoluta es inalcanzable, si el equipo mantiene una **consistencia subjetiva**, asignando el mismo esfuerzo relativo a tareas equivalentes a lo largo del tiempo, la métrica converge y se estabiliza.
> * **Relevancia:** Valida científicamente el uso de métricas de velocidad y estimación relativa como insumo confiable para presupuestos y planificación sin caer en los sesgos de la estimación en horas individuales.

---

## 8. Calibración y Simulación con el Modelo PNR - Putnam-Norden-Rayleigh

La distribución temporal del personal viene dada por el modelo PNR:

$$p(t) = 2 K a t \cdot e^{-a t^2}$$

A partir de los datos históricos, con $t \in [1..9]$ meses y $p \in [8..11]$ personas, se obtuvieron por mínimos cuadrados los parámetros calibrados:

$$\mathbf{K = 192.15\text{ PM}} \quad \text{y} \quad \mathbf{a = 0.02847} \quad \text{con } R^2 = 0.9434$$

* **8.1 Proyecto de 72 PM:** Mantiene la forma funcional de la curva Rayleigh, reduciendo el pico máximo de personal a $p_{\text{max}} \approx 10$ personas en el mes 3.
* **8.2 Cuadruplicación de la Tasa de Crecimiento con $a = 0.11388$:**
  * El pico de personal se alcanza en la **mitad del tiempo**, es decir $t = 1.5$ meses.
  * El personal máximo requerido se **duplica**, llegando a $p_{\text{max}} \approx 19.5$ personas.
  * *Evaluación Técnica:* Aunque el modelo matemático genera la curva, en la práctica el proyecto colapsará al intentar ingresar a la ==Zona Imposible de Boehm==(rojo). Forzar la asimilación del equipo en la mitad del tiempo dispara exponencialmente los costos de coordinación y la tasa de defectos.

<!-- PAGEBREAK -->

## 9. Modelos Estáticos de Estimación LOC vs. Esfuerzo

Se evaluaron los modelos de regresión sobre los datos de líneas de código LOC y esfuerzo PM:

| Modelo | Ecuación Calibrada | Coeficiente $R^2$ | Estimación $\text{LOC}=9100$ | Estimación $\text{LOC}=200$ |
| :--- | :--- | :---: | :---: | :---: |
| **Lineal** | $E = 0.002939 \cdot \text{LOC} - 3.2667$ | **$0.9726$** | **$23.48$ PM** | **$-2.68$ PM** |
| **Exponencial** | $E = 1.9440 \cdot e^{0.000290 \cdot \text{LOC}}$ | $0.9058$ | **$27.18$ PM** | **$2.06$ PM** |

### Análisis de Resultados
* **Selección del Modelo:** El **modelo lineal** representa con mayor fidelidad la muestra histórica por tener un $R^2$ superior, $0.9726$ vs. $0.9058$.
* **Evaluación del Lineal:** ==Mejor ajuste global==(verde), pero falla en valores muy bajos.
* **Evaluación del Exponencial:** Comportamiento asintótico físicamente consistente.
* **Anomalía en $\text{LOC} = 200$:** El resultado negativo, $-2.68$ PM, del modelo lineal evidencia el peligro de la ==extrapolación extrema==(rojo) fuera del rango de calibración de $1,000$ a $10,000$ LOC. En proyectos pequeños existen costos fijos de gestión no capturados por el término independiente negativo.

---

## 10. Descomposición en Etapas y Opciones Reales - ROV

Dividir un proyecto en fases incrementales incrementa significativamente su valor financiero mediante la teoría de ==Real Options Valuation==(violeta):

* **Opción de Abandono:** Permite cancelar el proyecto ante resultados desfavorables en etapas tempranas, acotando la pérdida máxima y evitando la falacia del costo hundido.
* **Opción de Pivotar / Escalado:** Permite ajustar el alcance y redirigir el backlog a medida que se reduce la incertidumbre técnica y de mercado.
* *Impacto Financiero:* La flexibilidad operativa de las etapas genera un incremento de valor neto de entre **15% y 40%** en comparación con proyectos monolíticos.

---

## 11. Criterio de Devengado vs. Flujo de Caja Real

La contabilidad tradicional utiliza el ==criterio de devengado==(celeste), es decir, reconoce ingresos y gastos al momento de generarse el derecho u obligación. 

Sin embargo, para la gestión financiera del proyecto esto es insuficiente porque:
* No refleja la dinámica real de liquidez, conocido como criterio del ==percibido==(verde) o *cash flow*.
* Omite el costo de oportunidad del capital y el valor generado por la flexibilidad estratégica.

---

## 12. Promoción Fiscal y Escudo Térmico - Tax Shield

Los regímenes de promoción impositiva que reducen o eximen el impuesto a las ganancias **desalientan el uso del apalancamiento financiero**:

$$\text{Escudo Fiscal} = \text{Intereses de Deuda} \times \text{Alícuota del Impuesto}$$

Al reducirse la alícuota impositiva a valores nulos o mínimos, el beneficio del ==tax shield==(naranja) desaparece, por lo que la empresa preferirá financiarse con capital propio en lugar de asumir endeudamiento sin ventajas fiscales.

---

## 13. Buffers de Contingencia del +5% y Ley de Parkinson

Es técnicamente correcto establecer colchones de contingencia reducidos del +5% frente a incertidumbres estimadas del $\pm 30\%$ debido a:

* **Efecto Portafolio:** En proyectos con múltiples tareas independientes, las variaciones positivas y negativas se compensan estadísticamente.
* **Ley de Parkinson:** Contimpos excesivos provocan que *"el trabajo se expanda hasta llenar todo el tiempo disponible"*, generando ineficiencias.
* **Competitividad:** Margenes desproporcionados encarecen el precio final del proyecto y perjudican su posición en el mercado.

<!-- PAGEBREAK -->

## 14. Esperanza Matemática en Juegos de Azar - Ruleta Europea

Para una ruleta europea con 37 casilleros: 18 rojos, 18 negros y 1 verde:

* $P(\text{Ganar}) = \frac{18}{37} \approx 48.65\%$
* $P(\text{Perder}) = \frac{19}{37} \approx 51.35\%$

Calculando la Esperanza Matemática para una apuesta de $\$1,000$:

$$E(X) = (+\$1,000) \cdot \frac{18}{37} + (-\$1,000) \cdot \frac{19}{37} = -\frac{\$1,000}{37} \approx \mathbf{-\$27.03}$$

> ==**Nota:**==(celeste) En promedio, el jugador pierde **$\$27.03$ por cada $\$1,000$ apostados**, lo que equivale a la ventaja matemática de la casa del $2.70\%$.

---

## 15. Análisis del 'Telar de los Colores' - Esquema Piramidal

En un esquema donde se arriesgan $\$1,000$ con un retorno exitoso del $7\%$, es decir $+\$70$, y pérdida total del $100\%$, o $-\$1,000$:

Buscando el punto de equilibrio financiero donde $E(X) = 0$:

$$E(X) = 70 \cdot P_g - 1000 \cdot (1 - P_g) = 0 \implies 1070 \cdot P_g = 1000 \implies P_g \approx \mathbf{93.46\%}$$

* Se requiere una probabilidad de éxito mínima del **$93.46\%$** solo para no perder dinero.
* Dado que en esquemas piramidales reales la tasa de pérdida supera el $85-90\%$ para los participantes tardíos, la operación posee una esperanza fuertemente ==negativa==(rojo).

---

## 16. Cálculo del Valor Presente 

Dado un Valor Futuro $VF = \$1,000$ a 12 meses, siendo $n=12$, con costo de oportunidad mensual $r = 7\%$, es decir $0.07$:

### Interés Compuesto - Criterio Financiero Estándar
$$V_p = \frac{VF}{(1 + r)^n} = \frac{1000}{(1.07)^{12}} = \frac{1000}{2.252192} \approx \mathbf{\$444.01}$$

### Interés Simple
$$V_p = \frac{VF}{1 + r \cdot n} = \frac{1000}{1 + 0.07 \times 12} = \frac{1000}{1.84} \approx \mathbf{\$543.48}$$

---

## 17. TEA vs. TNA

Con una tasa de oportunidad mensual del $7\%$:

* **Tasa Efectiva Anual - Capitalización Compuesta:**
$$\text{TEA} = (1 + 0.07)^{12} - 1 = 2.252192 - 1 = \mathbf{125.22\%}$$

* **Tasa Nominal Anual - Criterio Simple:**
$$\text{TNA} = 7\% \times 12 = \mathbf{84.00\%}$$