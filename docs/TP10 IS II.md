---
coverConfig:
  showCover: true
  title: Administración de Proyectos (Gestión)
  subtitle: Trabajo Nro. 10
  materia: Ing. de Software II
  coverStyle: academic_elegant
  showLogo: true
  integrantes:
    - Galdini Jenaro
  profesores:
    - Dr. Pedro E. Colla
    - Lic. Lucía Blanc
    - ''
  sigla: ''
  fecha: ''
  showHeader: false
  showFooter: true
activeTheme: minimal
---
# Ejercicio 1

Se requiere invertir \$1000 por mes durante 12 meses. Al final del proyecto (mes 12), el valor presente de los flujos de caja futuros será de \$18.000. La tasa efectiva mensual es del 1% ($r = 0.01$).

### a. Valor Presente Neto (VPN) del proyecto según los planes

Para calcular el VPN, traemos al momento cero tanto los costos mensuales como el ingreso final.

- **VP Costos:** (Anualidad vencida de \$1000 por 12 meses) = \$11.255,08
- **VP Ingresos:** (\$18.000 descontados desde el mes 12) = \$15.974,09

$$ \text{VPN} = \text{VP Ingresos} - \text{VP Costos} = 4.719,01 $$

### b. VPN del proyecto extendido por 3 meses (al mismo costo)

- **VP Costos:** (Anualidad vencida de \$1000 por 15 meses) = \$13.865,05
- **VP Ingresos:** (\$18.000 descontados desde el mes 15) = \$15.504,29

$$ \text{VPN} = \text{VP Ingresos} - \text{VP Costos} = 1.639,24 $$

### c. Rentabilidad en cada uno de los casos

Se calcula como:

$$ \text{Rentabilidad} = \frac{\text{VPN}}{\text{VP de la inversión}} $$
 
 - **Rentabilidad (Caso A - Ideal):** $ \dfrac{4.719,01}{11.255,08} = 41,93\% $
 - **Rentabilidad (Caso B - Retraso):** $ \dfrac{1.639,24}{13.865,05} = 11,82\% $


\newpage


### d. Impacto financiero por un retraso de 6 meses

Un retraso de 6 meses implica 18 meses de costos mensuales y recibir el flujo recién en el mes 18.

- **VP Costos** (18 meses) = \$16.398,27
- **VP Ingresos** (Mes 18) = \$15.048,60

$$ \text{VPN} = -1.349,67 $$

> **Impacto:** El impacto es devastador. El proyecto deja de ser rentable y pasa a generar pérdidas, destruyendo por completo el valor financiero para el inversor.

### e. Conveniencia de un esquema de gestión profesional

Si se agrega un 5% al costo mensual (\$1.050/mes en lugar de \$1000) pero se garantiza terminar en 12 meses:

- **VP Costos** (\$1050 por 12 meses) = \$11.817,83
- **VP Ingresos** (Mes 12) = \$15.974,09

$$ \text{VPN} = 4.156,26 $$

> **Análisis:** Desde una perspectiva puramente financiera, **es altamente conveniente**. Pagar la prima del 5% funciona como un "seguro" que, si bien reduce el VPN ideal (\$4.719), lo protege frente a los retrasos (el VPN cae a \$1.639 con solo 3 meses de demora y da pérdidas con 6 meses).


\newpage


### f. [Desafío] Valor mensual máximo de costos aceptable

Buscamos el costo mensual máximo ($C$) para que un proyecto de 15 meses tenga el mismo VPN que el planeado a 12 meses (\$4.719,01).

- **VPN Deseado** = \$4.719,01
- **VPN** = VP Ingresos (Mes 15) - VP Costos (con cuota $C$ por 15 meses)

$$ 4.719,01 = 15.504,29 - C \times [\text{Factor anualidad 15 meses al } 1\%] $$

Sabiendo que el factor de anualidad es $13,865$:

$$ C \times 13,865 = 10.785,28 \implies C = 777,88 $$

El costo mensual máximo aceptable para compensar el retraso es de **\$777,88**.

---


\newpage


## Ejercicio 2

*Situación base:* Proveedor gasta \$1000/mes por 12 meses ($\text{VP} = 11.255,08$). Patrocinante paga \$14.000 en el mes 12 ($\text{VP Pago} = 12.424,30$). Costo de oportunidad = 1%.

### a. Pago en el mes 14
Para que sea financieramente neutro para el proveedor, el VP del pago no debe cambiar.

$$ \frac{\text{Pago Mes 14}}{(1.01)^{14}} = 12.424,30 $$
$$ \text{Pago Mes 14} = 12.424,30 \times (1.01)^{14} = 14.281,40 $$

### b. Finalización en mes 6 (Pago en mes 12)
Para comprimir 12 meses de trabajo en 6 meses con staff constante original, debemos duplicar el staff, llevando el costo a \$2000 mensuales por 6 meses.

- Nuevo VP Costos Proveedor (6 meses a \$2000) = \$11.590,95.
- El costo (VP) para el proveedor aumentó en **\$335,87**.
- El nuevo VP del Pago requerido para compensar es: \$12.424,30 + \$335,87 = \$12.760,17.

Si este pago se realiza recién en el mes 12, se debe capitalizar hasta esa fecha:

$$ \text{Pago Mes 12} = 12.760,17 \times (1.01)^{12} = 14.378,47 $$

### c. Finalización y Pago en mes 6
Si el patrocinante adelanta el pago al mes 6 (manteniendo el VP requerido de \$12.760,17):

$$ \text{Pago Mes 6} = 12.760,17 \times (1.01)^{6} = 13.545,17 $$

---


\newpage


## Ejercicio 3

La relación matemática dada asume un *escalado lineal perfecto* (dividir el esfuerzo en $N$ personas dividirá el tiempo exacto en $N$). Esta fórmula solo es válida para equipos unipersonales o tareas perfectamente aisladas porque ignora **la Ley de Brooks** (sobrecarga y canales de comunicación) y **la Ley de Amdahl** (dependencias secuenciales que no pueden paralelizarse). A medida que se agregan desarrolladores, el tiempo de coordinación aumenta.

---

## Ejercicio 4

La fórmula $\text{Duracion} = \sum (\text{Duracion de Tareas})$ solo es válida para proyectos triviales **estrictamente secuenciales** (sin actividades en paralelo). En un proyecto real con una red de dependencias, la duración no es la suma de las partes, sino que está dictada por el **camino crítico** (la secuencia de tareas vinculadas de mayor duración).

---

## Ejercicio 5

Las tareas ubicadas en el "camino crítico" tienen una holgura o margen de tiempo igual a cero ($\text{Margen} = 0$). Esto significa que no existe ningún "colchón" de tiempo entre su finalización y el inicio de la siguiente. Retrasar una de estas tareas empuja inmediatamente el inicio de las tareas sucesoras, extendiendo de forma inexorable la duración total del proyecto.

---

## Ejercicio 6

Acelerar una actividad que tiene un margen distinto de cero ($\text{Margen} \neq 0$) no es conveniente porque **no se encuentra en el camino crítico**. Acelerar una tarea que no es crítica no reducirá la duración total del proyecto; simplemente aumentará su margen y probablemente generará un costo adicional innecesario o desaprovechará recursos que podrían haberse asignado a tareas verdaderamente críticas.

---

## Ejercicio 7

Reducir el calendario en un 50% utilizando únicamente *clocking* (exigencia de sobretiempo / doble turno para el mismo equipo) **no es viable**. A corto plazo, trabajar 16 horas diarias en lugar de 8 podría generar un falso avance, pero en el mediano plazo es insostenible: produce fatiga extrema (burnout), una caída drástica de la productividad, un aumento exponencial de los errores técnicos y desmotivación en el equipo, lo que termina por retrasar más el desarrollo.

---

## Ejercicio 8

Una consigna estricta de "cero cambios" **no es recomendable ni realista** en ingeniería de software. Si bien financieramente suena atractivo para "congelar" alcance, blindar presupuestos y cumplir calendarios agresivos, el software es dinámico y las necesidades de los usuarios evolucionan. Si no se aceptan cambios, se corre el altísimo riesgo de entregar el software a tiempo, pero que el mismo sea obsoleto o inútil para el negocio, destruyendo todo el valor del proyecto.

---

## Ejercicio 9

**No consideraría un plan de contingencia.** De acuerdo con el marco teórico de la gestión de riesgos, la severidad de un riesgo se calcula por:

$$ \text{Valor Esperado} = \text{Probabilidad} \times \text{Impacto} $$

La ciudad de Concepción del Uruguay, Entre Ríos, tiene una probabilidad de actividad sísmica destructiva estadísticamente tendiente a cero. Al ser un riesgo de probabilidad nula, la estrategia teórica correcta es **Aceptar** el riesgo; no se justifica económica ni temporalmente planificar o desviar recursos para mitigarlo.

---


\newpage


## Ejercicio 10

La principal razón para transferir un riesgo (ej. mediante contratos a terceros, seguros o garantías) es **económica y de especialización técnica**. Se transfiere cuando el tercero (proveedor) posee mayores economías de escala, experiencia técnica o herramientas especializadas para gestionar ese riesgo de una manera mucho más eficiente y barata que si lo intentara mitigar el propio equipo de proyecto.

---

## Ejercicio 11

Controlar el trabajo mediante métricas del equipo y no del individuo responde a que el desarrollo de software es un esfuerzo colaborativo y sistémico. El micromanagement de individuos incentiva comportamientos tóxicos y competitivos (como optimizar métricas personales arruinando la arquitectura o negándose a ayudar a pares). Controlar los entregables del equipo fomenta la autoorganización, la seguridad psicológica, el sentido de pertenencia y asegura que todos remen hacia la entrega de valor funcional.

---


\newpage


## Ejercicio 12

**¿Satisface GitHub las necesidades de gestión de configuración (SCM)? Sí.**

| Función SCM requerida | Herramienta en GitHub | Justificación |
| :--- | :--- | :--- |
| **Identificación / Control de Versiones** | Repositorios Git | Mantiene el historial inmutable de código fuente, permite crear ramas (*branching*) y versiones base (*tags*). |
| **Control de Cambios** | Pull Requests / Issues | Centraliza la discusión, revisión de código (*Code Review*) y políticas de aprobación antes de integrar un cambio a la rama principal. |
| **Auditoría e Informes de Estado** | Commit History / Blame | Proporciona trazabilidad total: quién hizo qué cambio, cuándo y por qué, manteniendo auditoría constante del estado del proyecto. |
| **Generación de Entregables (Release)** | GitHub Actions / Releases | Permite empaquetar versiones (*Releases*), administrar paquetes y automatizar compilaciones (Integración Continua). |

---

## Ejercicio 13

- **Fábrica de software:** Se estructura como una línea de ensamblaje. Los roles están extremadamente divididos y el trabajo está altamente procedimentado en base a especificaciones estrictas. El desarrollador suele tener poco o nulo contexto del negocio y actúa transaccionalmente (construir lo que dicta un documento).
- **Equipo de proyecto convencional:** Es típicamente un equipo multidisciplinario e integrado (ej. células ágiles). Tienen un alto nivel de involucramiento en entender el problema de negocio subyacente, participan activamente en las decisiones de diseño arquitectónico, son flexibles a cambios y sienten pertenencia sobre el éxito o fracaso del producto.

---


\newpage


## Ejercicio 14

### a. Recursos Infinitos (1 persona por tarea disponible siempre)

- **Duración total del proyecto:** **47 días.**
- **Camino crítico:** Está conformado por la ruta más larga: **A $\rightarrow$ D $\rightarrow$ H $\rightarrow$ J**

  $$ 5 + 20 + 10 + 12 = 47 $$

### b. Staff Limitado a 2 personas (Recursos finitos)

Al limitar el staff a 2 recursos, se genera un cuello de botella. Mientras una persona está obligada a trabajar en la Tarea D (que dura 20 días sin pausas), el segundo recurso debe ejecutar secuencialmente todas las tareas paralelas (B, C, E, F, G). Esto alarga inevitablemente el proyecto.

- **Nueva duración del proyecto:** **52 días.**
- **Nuevo Camino Crítico (Cadena Crítica):**
  Al existir dependencias de recursos limitados, el nuevo camino crítico toma la forma de una *Cadena Crítica*, donde el proyecto se retrasa ya sea por espera técnica o espera de personal. Ambas secuencias determinan el límite de 52 días:

  1. **A $\rightarrow$ D $\rightarrow$ (Espera recurso) $\rightarrow$ E $\rightarrow$ H $\rightarrow$ J**
     $$ 5 + 20 + 5 + 10 + 12 = 52 $$
  2. **A $\rightarrow$ C $\rightarrow$ B $\rightarrow$ F $\rightarrow$ G $\rightarrow$ I $\rightarrow$ J**
     (Ejecutadas secuencialmente por el mismo recurso: $5 + 10 + 3 + 6 + 7 + 9 + 12 = 52$)
