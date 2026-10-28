---
coverConfig:
  showCover: false
  title: Gestión de Calidad
  subtitle: Trabajo Práctico Nº 11
  materia: Ing. de Software II
  coverStyle: academic_elegant
  showLogo: true
  integrantes:
    - Galdini Jenaro
  profesores:
    - Dr. Pedro E. Colla
    - Lic. Lucía Blanc
    - ''
  sigla: IS2
  fecha: Octubre 2026
  showHeader: false
  showFooter: true
  footerLeft: '{materia}'
  footerNumbering: pagina_x_de_y
  footerShowLine: true
---

# Bloque 1: Caso de Estudio "Conjetura de Collatz" y Proceso de V&V

## 1.1. Estructuración de Requerimientos Funcionales y No Funcionales

A partir del problema enunciado en la consigna, se definen de manera unívoca los requerimientos del sistema:

### Requerimientos Funcionales ($R = \{R_1, R_2, R_3, R_4, R_5, R_6\}$)
- **$R_1$ (Entrada de Datos):** El sistema debe solicitar y aceptar por teclado un número ingresado interactivamente por el usuario a través de la consola estándar.
- **$R_2$ (Validación de Signo y Cota Inferior):** El sistema debe validar que el número ingresado sea un entero positivo estrictamente mayor o igual a $1$.
- **$R_3$ (Validación de Cota Superior Práctica):** El sistema debe validar que el número entero ingresado sea menor o igual al límite práctico de $1999$.
- **$R_4$ (Algoritmo de Collatz):** El sistema debe aplicar de forma iterativa las operaciones de la conjetura:
  - Si el número actual es par, se divide entre 2: $n \leftarrow n // 2$.
  - Si el número actual es impar, se multiplica por 3 y se suma 1: $n \leftarrow 3n + 1$.
  - La secuencia finaliza al converger en el valor $1$.
- **$R_5$ (Cómputo de Iteraciones):** El sistema debe contabilizar el número total de pasos/iteraciones requeridos para alcanzar el valor $1$. Si el valor inicial es $1$, la cantidad de iteraciones es $0$.
- **$R_6$ (Emisión de Resultados):** El sistema debe imprimir por pantalla el valor entero de partida y el número total de iteraciones calculadas en un formato claro para el usuario.

### Requerimientos No Funcionales ($F = \{F_1, F_2, F_3, F_4, F_5\}$)
- **$F_1$ (Usabilidad e Interfaz):** Los mensajes de solicitud y salida por consola deben ser claros, descriptivos y autoexplicativos.
- **$F_2$ (Robustez y Tolerancia a Fallas):** El software debe capturar y tratar excepciones ante ingresos no numéricos (cadenas, números con coma flotante, valores vacíos o caracteres especiales) y valores fuera de rango, impidiendo caídas anormales (*crashes*).
- **$F_3$ (Rendimiento y Eficiencia Temporal):** El tiempo de cálculo para cualquier entero en el rango $[1, 1999]$ debe ser prácticamente instantáneo ($t < 100\text{ ms}$).
- **$F_4$ (Mantenibilidad y Estándares de Código):** El código debe estructurarse de forma modular, con tipado estático (`typing`), docstrings según PEP 257 y una tasa equilibrada de comentarios.
- **$F_5$ (Portabilidad):** El programa debe ejecutarse en cualquier entorno estándar de Python 3 sin dependencias propietarias o librerías externas obligatorias.

---

\newpage

## 1.2. Diseño y Formulación del Conjunto de Casos de Prueba

Se formulan 10 casos de prueba ($T = \{T_1, \dots, T_{10}\}$), clasificados en **Unitarios (Caja Blanca)** y **Funcionales (Caja Negra)**:

### Casos de Prueba Unitarios (Caja Blanca)

| ID | Entrada | Salida Esperada / Comportamiento | Propósito / Cobertura |
| :---: | :---: | :--- | :--- |
| **$T_1$** | `collatz(1)` | `0` iteraciones | Evalúa la condición de parada inmediata del bucle `while num != 1`. |
| **$T_2$** | `collatz(2)` | `1` iteración | Evalúa la rama par única ($2 \to 1$). |
| **$T_3$** | `collatz(3)` | `7` iteraciones | Evalúa la alternancia de ramas impares y pares ($3 \to 10 \to 5 \to 16 \to 8 \to 4 \to 2 \to 1$). |
| **$T_4$** | `collatz(20)` | `7` iteraciones | Valida el caso de prueba testigo provisto en el enunciado original. |
| **$T_5$** | `collatz(1999)` | `50` iteraciones | Evalúa el cálculo correcto en el límite superior práctico. |

\newpage

### Casos de Prueba Funcionales (Caja Negra)

| ID | Entrada | Salida Esperada / Comportamiento | Propósito / Cobertura |
| :---: | :---: | :--- | :--- |
| **$T_6$** | Consola: `"20"` | "El número de partida es 20 y el número de iteraciones es 7" | Valida el flujo normal de punta a punta (E/S por teclado y pantalla). |
| **$T_7$** | Consola: `"1"` | "El número de partida es 1 y el número de iteraciones es 0" | Valida la frontera mínima funcional. |
| **$T_8$** | Consola: `"1999"` | "El número de partida es 1999 y el número de iteraciones es 50" | Valida la frontera máxima funcional. |
| **$T_9$** | Consola: `"0"`, `"-5"`, `"2000"` | Mensaje de error controlado indicando rango `[1, 1999]` | Valida el rechazo de valores fuera de los límites especificados. |
| **$T_{10}$** | Consola: `"abc"`, `"12.5"`, `""` | Mensaje de error controlado capturando `ValueError` | Valida la robustez ante datos de tipo incorrecto. |

---

\newpage

## 1.3. Matriz de Trazabilidad RTMX y Validación de Integridad

La Matriz de Trazabilidad Cruzada de Requerimientos y Pruebas (RTMX) establece la correspondencia bidireccional entre el conjunto de requerimientos ($R \cup F$) y los casos de prueba ($T$):

| Req. | Descripción | $T_1$ | $T_2$ | $T_3$ | $T_4$ | $T_5$ | $T_6$ | $T_7$ | $T_8$ | $T_9$ | $T_{10}$ | Cobertura |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$R_1$** | Entrada por teclado | | | | | | **X** | **X** | **X** | **X** | **X** | **100%** |
| **$R_2$** | Entero positivo $\ge 1$ | **X** | **X** | **X** | **X** | **X** | **X** | **X** | | **X** | | **100%** |
| **$R_3$** | Límite máximo 1999 | | | | | **X** | | | **X** | **X** | | **100%** |
| **$R_4$** | Operación de Collatz | **X** | **X** | **X** | **X** | **X** | **X** | **X** | **X** | | | **100%** |
| **$R_5$** | Conteo de iteraciones | **X** | **X** | **X** | **X** | **X** | **X** | **X** | **X** | | | **100%** |
| **$R_6$** | Impresión de resultados | | | | | | **X** | **X** | **X** | | | **100%** |
| **$F_1$** | Usabilidad de consola | | | | | | **X** | **X** | **X** | **X** | **X** | **100%** |
| **$F_2$** | Robustez y excepciones | | | | | | | | | **X** | **X** | **100%** |
| **$F_3$** | Rendimiento temporal | **X** | **X** | **X** | **X** | **X** | **X** | **X** | **X** | | | **100%** |
| **$F_4$** | Mantenibilidad / Estilo | **X** | **X** | **X** | **X** | **X** | **X** | **X** | **X** | **X** | **X** | **100%** |
| **$F_5$** | Portabilidad estándar | **X** | **X** | **X** | **X** | **X** | **X** | **X** | **X** | **X** | **X** | **100%** |

### Validación de Integridad
- **Condición 1 (Completitud):** Todo requerimiento $R_i \in R$ y $F_j \in F$ cuenta con al menos un caso de prueba asociado. No existen requerimientos huérfanos.
- **Condición 2 (Trazabilidad hacia adelante y atrás):** Cada caso de prueba $T_k \in T$ responde directamente a uno o más requerimientos específicos. No existen pruebas espurias.

---

## 1.4. Sesión 1: Inspección Estática de Código (Sin Ejecución)

Se analizó el código original provisto en el enunciado (18 líneas de código declaradas):

```python
#Calculando el número de iteraciones del algoritmo de Collatz
def collatz(num):
 iteraciones = 0
 while num != 1:
 if num % 2 == 0:
 num = num // 2
 else:
 num = 3*num + 1
 iteraciones += 1
 return iter 
#Comprobando los resultados
i=20
print("El número de iteraciones para %d es %d\n" % (i,collatz(j))
```

Mediante inspección estática rigurosa (sin ejecución en intérprete), se identificaron los siguientes **13 defectos latentes**:

1. **Defecto 1 (Sintáctico - Indentación de Bloque):** La instrucción `if num % 2 == 0:` carece de indentación respecto al bloque `while num != 1:`. Provoca `IndentationError`.
2. **Defecto 2 (Sintáctico - Indentación de Rama):** La instrucción `num = num // 2` carece de indentación respecto a la cabecera `if`.
3. **Defecto 3 (Sintáctico - Indentación de Alternativa):** La cláusula `else:` no guarda alineación con la cláusula `if`.
4. **Defecto 4 (Sintáctico - Indentación de Rama):** La instrucción `num = 3*num + 1` no está indentada respecto a `else:`.
5. **Defecto 5 (Sintáctico - Indentación de Acumulador):** La instrucción `iteraciones += 1` está desalineada y no refleja pertenencia al cuerpo del `while`.
6. **Defecto 6 (Sintáctico - Indentación de Retorno):** La sentencia `return iter` está al mismo nivel que las operaciones internas en lugar de estar indentada al nivel de la función `def`.
7. **Defecto 7 (Sintáctico - Delimitador Incompleto):** En la llamada final `print(...)` falta el paréntesis de cierre, provocando `SyntaxError: '(' was never closed`.
8. **Defecto 8 (Semántico - Tipo de Retorno Erróneo):** Se retorna el identificador `iter` (`return iter`) en lugar de la variable acumuladora `iteraciones`. `iter` es una función incorporada (*builtin*) de Python, por lo que la función retornaría un objeto función y no un entero.
9. **Defecto 9 (Semántico - Variable no Definida):** En la invocación `collatz(j)` se utiliza la variable `j`, la cual jamás fue inicializada (`NameError: name 'j' is not defined`).
10. **Defecto 10 (Funcional - Omisión de Entrada por Teclado):** El programa tiene un valor estático fijado en el código (`i=20`) y no implementa la función `input()` requerida por $R_1$.
11. **Defecto 11 (Funcional - Omisión de Validación Inferior):** No existe control para enteros positivos $\ge 1$ ($R_2$). Si se ingresara $0$ o un negativo, el bucle `while` diverge en bucle infinito.
12. **Defecto 12 (Funcional - Omisión de Validación Superior):** No existe control para el límite práctico de $1999$ ($R_3$).
13. **Defecto 13 (Estándares de Calidad - Tasa de Comentarios Excesiva):** La consigna establece: *"Considere como defecto una tasa de comentarios mayor a 12"*. El archivo presenta 2 líneas de comentarios sobre 13 líneas de código efectivas, representando una tasa del **$15.38\%$** ($> 12\%$). Además, son comentarios obvios (*code smells*) que incumplen las guías de código limpio.

**Resultado de la Sesión 1:** **13 defectos detectados**.

---

\newpage

## 1.5. Sesión 2: Inspección y Validación de Casos de Prueba

Se inspeccionó la suite de casos de prueba formulada inicialmente para comprobar si cubría todos los escenarios de riesgo y bordes de la especificación:

- **Defecto en Pruebas 1:** El diseño preliminar omitía la validación del límite superior estricto ($1999$), pudiendo pasar desapercibido un desbordamiento o degradación del algoritmo.
- **Defecto en Pruebas 2:** No se contemplaba la frontera mínima $n = 1$ donde el bucle no debe ejecutarse ninguna vez ($0$ iteraciones).
- **Defecto en Pruebas 3:** Se carecía de pruebas para valores fuera del rango acotado ($0$, negativos, mayores a 1999).
- **Defecto en Pruebas 4:** No se habían definido casos para entradas no numéricas o tipos incorrectos (letras, flotantes, cadenas vacías).

**Acción Correctiva:** Se agregaron formalmente los casos $T_5, T_7, T_8, T_9$ y $T_{10}$ y se actualizó la matriz RTMX.  
**Resultado de la Sesión 2:** **4 defectos detectados** en la verificación del artefacto de pruebas.

---

## 1.6. Sesiones de Pruebas Unitarias (Caja Blanca)

Siguiendo la metodología de sesiones académicas, se ejecutaron los casos unitarios $\{T_1, T_2, T_3, T_4, T_5\}$:

### Sesión 3 (Primera sesión de ejecución unitaria - $S_1$)
- **Intento 1:** Ejecución del código original. Falla inmediata por `IndentationError` en línea 5 al intentar compilar el módulo. *(1 defecto registrado)*.
- **Intento 2:** Tras alinear temporalmente el bucle, se ejecuta la función `collatz(1)`: Falla sintáctica en la línea 13 por falta de paréntesis de cierre en `print`. *(1 defecto registrado)*.
- **Intento 3:** Con los paréntesis cerrados, se evalúa `collatz(1)`: Falla en aserción al retornar `<built-in function iter>` en lugar de `0`. *(1 defecto registrado)*.
- **Defectos detectados en Sesión 3:** **3 defectos**.
- **Reparación entre sesiones:** Se reescribe la función `collatz` con indentación normalizada a 4 espacios, se corrige `return iteraciones` y se parametriza la entrada.

### Sesión 4 (Segunda sesión de ejecución unitaria - $S_2$)
- $T_1 (1)$: `collatz(1) == 0` $\to$ **PASS**
- $T_2 (2)$: `collatz(2) == 1` $\to$ **PASS**
- $T_3 (3)$: `collatz(3) == 7` $\to$ **PASS**
- $T_4 (20)$: `collatz(20) == 7` $\to$ **PASS**
- $T_5 (1999)$: `collatz(1999) == 50` $\to$ **PASS**
- **Defectos detectados en Sesión 4:** **0 defectos**. (100% de éxito en pruebas unitarias).

---

\newpage

## 1.7. Sesiones de Pruebas Funcionales (Caja Negra)

Con las pruebas unitarias superadas al 100%, se procedió a ejecutar las pruebas funcionales de sistema $\{T_6, T_7, T_8, T_9, T_{10}\}$:

### Sesión 5 (Primera sesión de ejecución funcional - $S_3$)
- **Falla 1 ($T_6$):** Al intentar la ejecución interactiva, el script aborta con `NameError: name 'j' is not defined` y no solicita datos por consola ($R_1$).
- **Falla 2 ($T_9$):** Al ingresar `0` o `-1`, el programa entra en bucle infinito o genera resultados no válidos ($R_2$).
- **Falla 3 ($T_9$):** Al ingresar `2000`, el sistema procesa el cálculo sin validar la cota máxima ($R_3$).
- **Falla 4 ($T_{10}$):** Al ingresar texto ("abc"), el sistema colapsa con `ValueError: invalid literal for int()` sin brindar mensaje amigable ($F_2$).
- **Defectos detectados en Sesión 5:** **4 defectos**.
- **Reparación entre sesiones:** Se implementa `procesar_entrada()` y `main()` en `collatz.py` con validaciones defensivas de tipo, rango y bloques `try/except`.

### Sesión 6 (Segunda sesión de ejecución funcional - $S_4$)
Se repiten todos los casos de prueba funcionales:
- $T_6$ (Entrada `"20"`): Imprime "El número de partida es 20 y el número de iteraciones es 7" $\to$ **PASS**
- $T_7$ (Entrada `"1"`): Imprime "El número de partida es 1 y el número de iteraciones es 0" $\to$ **PASS**
- $T_8$ (Entrada `"1999"`): Imprime "El número de partida es 1999 y el número de iteraciones es 50" $\to$ **PASS**
- $T_9$ (Entradas `"0"`, `"-5"`, `"2000"`): Se captura la excepción y se emite error controlado indicando el rango permitido $\to$ **PASS**
- $T_{10}$ (Entradas `"abc"`, `"12.5"`, `""`): Se captura `ValueError` y se informa formato incorrecto sin abortar $\to$ **PASS**
- **Defectos detectados en Sesión 6:** **0 defectos**. (100% de éxito en pruebas funcionales).

---

\newpage

## 1.8. Resumen General de Sesiones y Verificación de Criterios

### Listado Total de Sesiones y Defectos Observados

| Sesión | Tipo de Actividad Realizada | Casos de Prueba Ejecutados | Defectos Encontrados | Estado Final |
| :---: | :--- | :---: | :---: | :---: |
| **Sesión 1** | Inspección Estática de Código Fuente | N/A (Inspección) | **13** | Requiere Corrección |
| **Sesión 2** | Inspección de Casos de Prueba | $T_1 \dots T_4$ | **4** | Casos agregados a RTMX |
| **Sesión 3 ($S_1$)** | Ejecución de Pruebas Unitarias | $T_1 \dots T_5$ | **3** | Falla en ejecución |
| **Sesión 4 ($S_2$)** | Re-ejecución de Pruebas Unitarias | $T_1 \dots T_5$ | **0** | **100% Éxito** |
| **Sesión 5 ($S_3$)** | Ejecución de Pruebas Funcionales | $T_6 \dots T_{10}$ | **4** | Falla en validaciones E/S |
| **Sesión 6 ($S_4$)** | Re-ejecución de Pruebas Funcionales | $T_6 \dots T_{10}$ | **0** | **100% Éxito** |
| **TOTAL** | **Proceso Integral de Calidad** | **Todos ($T_1 \dots T_{10}$)** | **24 defectos totales** (20 de código) | **Aprobado** |

### Verificación de Condiciones de Cierre (Definición de Terminado)
- [x] **Condición 1:** Todos los casos de prueba fueron exitosamente ejecutados al menos una vez.
- [x] **Condición 2:** No hubo caso de test que no se hubiera ejecutado.
- [x] **Condición 3:** No hay requerimiento (funcional o no funcional) que no se haya verificado.

---

## 1.9. Cálculo del PCE (Phase Containment Effectiveness) por Etapa

El **PCE (Efectividad de Contención de Defectos por Fase)** mide la capacidad de cada fase del ciclo de calidad para interceptar defectos antes de que se propaguen a fases posteriores:

$$\text{PCE}_i = \frac{\text{Defectos detectados en la fase } i}{\text{Defectos presentes al inicio de la fase } i} \times 100\%$$

Considerando las 3 fases del proceso sobre el código (Total de defectos observados = $13 + 3 + 4 = 20$ defectos = $100\%$):

1. **Fase 1: Inspección de Código:**
   - Defectos presentes al ingresar: $20$
   - Defectos detectados: $13$
   - $\text{PCE}_{\text{Inspección}} = \frac{13}{20} \times 100\% = \mathbf{65.0\%}$
   - Defectos que escapan a la siguiente fase: $20 - 13 = 7$.

2. **Fase 2: Pruebas Unitarias:**
   - Defectos presentes al ingresar: $7$
   - Defectos detectados: $3$
   - $\text{PCE}_{\text{Unitario}} = \frac{3}{7} \times 100\% = \mathbf{42.86\%}$ (representa el $15.0\%$ del total de defectos del proyecto).
   - Defectos que escapan a la siguiente fase: $7 - 3 = 4$.

3. **Fase 3: Pruebas Funcionales:**
   - Defectos presentes al ingresar: $4$
   - Defectos detectados: $4$
   - $\text{PCE}_{\text{Funcional}} = \frac{4}{4} \times 100\% = \mathbf{100.0\%}$ (representa el $20.0\%$ del total de defectos del proyecto).
   - Defectos que escapan a producción / liberación: $4 - 4 = 0$ defectos residuales.

---

\newpage

## 1.10. Cálculo de la Densidad de Defectos Inicial

La densidad de defectos inicial ($\delta_0$) relaciona los defectos totales identificados con el tamaño original del programa ($S = 18$ LOCs):

$$\delta_0 = \frac{\mu_0}{S} = \frac{20 \text{ defectos}}{18 \text{ LOCs}} = \mathbf{1.111 \text{ defectos / LOC}}$$

*(Si se evalúa únicamente respecto a los 13 defectos de la primera sesión de inspección: $\delta_{0,\text{insp}} = \frac{13}{18} = 0.722 \text{ def/LOC}$).*

---

\newpage

# Bloque 2: Modelos Teóricos, Métricas y Confiabilidad

## 2.1. Tutorial "Kanban para uso genérico": Significado y Criticidad del TEP

En la guía desarrollada por el **Ing. Álvaro Ruiz de Mendarozqueta**, el parámetro **TEP (Trabajo En Proceso)** —traducción directa de *WIP (Work In Progress)*— representa la cantidad total de elementos, tarjetas o tareas que han ingresado al sistema de trabajo y se encuentran activas en algún punto intermedio entre el estado inicial (*Para Hacer / To Do*) y el estado final (*Terminado / Done*).

### Significado Crítico en su Utilización
El principio rector de Kanban es **"Dejar de empezar y empezar a terminar"** (*Stop starting, start finishing*). Establecer un **límite explícito al TEP** (Límite WIP) en cada columna del tablero reviste un valor crítico por las siguientes razones:

1. **Gobernabilidad del Tiempo de Ciclo (Ley de Little):** Según la formulación de Little, el tiempo promedio que tarda una tarea en completarse (*Lead Time*) es directamente proporcional a la cantidad de trabajo en proceso:
   $$\text{Lead Time} = \frac{\text{TEP (WIP)}}{\text{Rendimiento (Throughput)}}$$
   Limitar el TEP disminuye drásticamente el tiempo de entrega y la variabilidad del proceso sin requerir recursos adicionales.
2. **Eliminación del Desperdicio por Multitarea:** La multitarea forzada degrada la concentración cognitiva y genera costos ocultos de cambio de contexto. Al restringir el TEP, los profesionales se focalizan en culminar las tareas abiertas antes de iniciar una nueva.
3. **Visibilización Inmediata de Cuellos de Botella:** Cuando una etapa se congestiona y alcanza su límite de TEP, el sistema bloquea el ingreso de nuevo trabajo aguas arriba, forzando al equipo a colaborar para resolver el obstáculo en lugar de continuar acumulando inventario intermedio.
4. **Prevención de Defectos:** La sobrecarga y el apuro son los principales causantes de fallas en software. Un TEP controlado reduce la presión de entrega y eleva la calidad intrínseca del código.

---

\newpage

## 2.2. Proyección de Defectos con el Modelo de Musa (Taller de Defectos)

El modelo de confiabilidad de tiempo de ejecución básico de **John D. Musa** modela la tasa de aparición de defectos $\lambda(\tau)$ como una función decreciente exponencial del tiempo de test continuo $\tau$:

$$\lambda(\tau) = \lambda_0 e^{-\left(\frac{\lambda_0}{\mu_0}\right)\tau}$$

Donde:
- $\lambda_0$: Tasa de intensidad de fallas al origen ($\tau = 0$).
- $\mu_0$: Número total de defectos latentes presentes al comienzo del test.
- $\tau$: Tiempo neto de prueba continuo.

La cantidad acumulada de defectos detectados $\mu(\tau)$ viene dada por:
$$\mu(\tau) = \int_0^\tau \lambda(t) dt = \mu_0 \left(1 - e^{-\frac{\lambda_0}{\mu_0}\tau}\right)$$

### Linealización por Regresión
Aplicando logaritmo natural a la función de intensidad:
$$\ln(\lambda(\tau)) = \ln(\lambda_0) - \left(\frac{\lambda_0}{\mu_0}\right)\tau \iff Y = b + m X$$
Con:
$$b = \ln(\lambda_0) \implies \lambda_0 = e^b$$
$$m = -\frac{\lambda_0}{\mu_0} \implies \mu_0 = -\frac{\lambda_0}{m}$$

### Aplicación sobre los Datos Provistos

| Día ($t$) | Defectos Observados ($d$) | $\ln(d)$ |
| :---: | :---: | :---: |
| 0 | 9 | 2.1972 |
| 1 | 18 | 2.8904 |
| 2 | 5 | 1.6094 |
| 3 | 7 | 1.9459 |
| 4 | 23 | 3.1355 |
| 5 | 2 | 0.6931 |
| 6 | 8 | 2.0794 |

Ajustando los parámetros mediante mínimos cuadrados lineales (`np.polyfit(t, ln_d, 1)`):
- **Pendiente ($m$):** $-0.11506$
- **Ordenada al origen ($b$):** $2.42390$

Despejando las constantes del modelo:
$$\lambda_0 = e^{2.42390} = \mathbf{11.290 \text{ defectos / día}}$$
$$\mu_0 = -\frac{11.2899}{-0.11506} = \mathbf{98.12 \approx 98 \text{ defectos totales esperados}}$$

El modelo proyecta que la aplicación contenía un total de aproximadamente **98 defectos latentes**. Dado que en los primeros 7 días (días 0 a 6) se detectaron $\sum d_i = 72$ defectos, la cantidad de defectos latentes remanentes estimada al día 6 es:
$$\mu_r = \mu_0 - 72 = 98.12 - 72 = \mathbf{26.12 \text{ defectos remanentes}}.$$

---

\newpage

## 2.3. Aplicación del Modelo de Musa al Dataset de Pruebas de Collatz

Asimilando cada sesión de prueba realizada en el ejercicio de Collatz a un "Día" de prueba continuo:
- Sesión 1 (Inspección estática): 13 defectos
- Sesión 2 (Inspección casos de prueba): 4 defectos
- Sesión 3 (Pruebas unitarias): 3 defectos

Ajustando el modelo de Musa sobre las sesiones activas de detección decreciente ($t = [1, 2, 3]$ con $d = [13, 4, 3]$):
- $\ln(d) = [2.5649, 1.3863, 1.0986]$
- Pendiente de regresión ($m$): $-0.7332$
- Ordenada al origen ($b$): $3.1496$

Cálculo de parámetros:
$$\lambda_0 = e^{3.1496} = \mathbf{23.33 \text{ defectos/sesión}}$$
$$\mu_0 = -\frac{23.3273}{-0.7332} = \mathbf{31.82 \approx 32 \text{ defectos totales proyectados}}$$

### Tamaño Final del Código y Defectos Liberados
1. **Tamaño final del código:** Mediante el comando equivalente a `cat collatz.py | wc -l`:
   $$\text{LOCs Finales} = \mathbf{51 \text{ LOCs}}$$
2. **Defectos Liberados ($\mu_r$):**
   Si se corrigen los 20 defectos de código identificados durante las fases de prueba ($\sum \mu_i = 20$):
   $$\mu_r = \mu_0 - \sum \mu_i = 31.82 - 20 = \mathbf{11.82 \text{ defectos liberados proyectados}}$$
   *(Si se computan las 24 observaciones totales incluyendo pruebas: $\mu_r = 31.82 - 24 = 7.82$ defectos).*

---

\newpage

## 2.4. Marco para Evaluar Garantía en Software (Colla): Efecto del PCE en el Tiempo de Test

En la investigación *"Marco para evaluar garantía en desarrollos de software"* del **Dr. Pedro E. Colla** (ASSE 2015 / JAIIO), se plantea un modelo de optimización económica del costo total del ciclo de vida:

$$C_t(\tau_r) = C_{\text{test}}(\tau_r) + W_{\text{garantía}}(\tau_r)$$

Donde el costo de test $C_{\text{test}}(\tau_r)$ crece linealmente con la duración de las pruebas $\tau_r$, mientras que el costo de soporte posventa por garantía $W_{\text{garantía}}(\tau_r)$ decrece exponencialmente a medida que se liberan menos defectos residuales $\mu_r$.

### Comportamiento Cualitativo al Incrementar el PCE
Al **incrementar el PCE (Efectividad de Contención de Defectos)** en las etapas tempranas de desarrollo (arquitectura, diseño e inspecciones de código):
1. **Reducción de Defectos de Entrada:** El software arriba a la etapa de pruebas con una masa de defectos latentes iniciales significativamente menor:
   $$\mu_{\text{ingreso}} = \mu_0 \cdot (1 - \text{PCE})$$
2. **Desplazamiento del Óptimo Temporal hacia la Izquierda:** Para satisfacer el umbral de confiabilidad requerido para otorgar garantía contractual con un nivel predeterminado de defectos tolerables ($\delta_r$), **el tiempo total de test óptimo ($\tau_r^*$) disminuye sustancialmente**.
3. **Optimización Financiera:** La curva de costos de garantía se aplana más rápidamente, permitiendo alcanzar el mínimo de costo total $C_t$ en un tiempo menor y con menor consumo de esfuerzo de testing.

---

\newpage

## 2.5. Línea de Base Organizacional y Control Estadístico

**Datos de la organización:**
- Línea de base de PCE: $89\% = 0.89$
- Densidad de defectos al momento de liberación ($\delta_r$): $0.12\text{ def/FP}$
- Tamaño del proyecto finalizado ($S$): $100\text{ FP}$

### a. Expectativa de defectos totales ($\mu_0$)
Los defectos liberados esperados son:
$$\mu_r = S \cdot \delta_r = 100\text{ FP} \times 0.12\text{ def/FP} = 12\text{ defectos}$$

Dado que $\mu_r$ representa los defectos que escapan al proceso de V&V ($\text{escape} = 1 - \text{PCE} = 1 - 0.89 = 0.11$):
$$\mu_r = \mu_0 \cdot (1 - \text{PCE}) \implies \mu_0 = \frac{\mu_r}{1 - \text{PCE}} = \frac{12}{0.11} = \mathbf{109.09 \approx 109 \text{ defectos totales}}$$

### b. Densidad de defectos al finalizar la construcción ($\delta_0$)
$$\delta_0 = \frac{\mu_0}{S} = \frac{109.09}{100\text{ FP}} = \mathbf{1.0909 \text{ def/FP} \approx 1.09 \text{ def/FP}}$$

### c. Cantidad de defectos a planear detectar durante V&V
$$\mu_{V\&V} = \mu_0 \cdot \text{PCE} = 109.09 \times 0.89 = \mathbf{97.09 \approx 97 \text{ defectos}}$$
*(Comprobación: $\mu_{V\&V} + \mu_r = 97.09 + 12 = 109.09 = \mu_0$).*

### d. Opinión Fundamentada sobre el Caso de Detección Anómala
**Escenario:** Se detectan en los primeros 3 días $20\text{ def/día}$, sumando **60 defectos en total**.

**Fundamentación de Ingeniería de Software:**
1. **Detección desproporcionada:** En apenas 3 días se ha detectado el **$61.8\%$** de todos los defectos previstos para todo el período de V&V ($60 / 97.09$).
2. **Inyección Anómala de Defectos:** Esta tasa de intensidad inicial ($\lambda_0 \ge 20\text{ def/día}$) evidencia de manera inequívoca que la calidad del código entregado por la etapa de construcción fue muy inferior a la línea de base histórica. La densidad real de inyección fue ampliamente superior a $\delta_0 = 1.09\text{ def/FP}$.
3. **Proyección del Total de Defectos:** En función de los modelos de confiabilidad de Musa, si la intensidad inicial es tan elevada, el total de defectos reales $\mu_0$ del proyecto **será sustancialmente mayor a 109 defectos** (probablemente en el orden de $180\text{ a }250\text{ defectos}$).
4. **Decisión Gerencial Recomendada:** Continuar bajo el plan original y liberar el producto manteniendo el tiempo prefijado conducirá a violar la densidad contractual de liberación ($\delta_r \gg 0.12\text{ def/FP}$), provocando sobrecostos masivos de garantía. Es imperativo declarar el proceso fuera de control estadístico, reestimar $\mu_0$ con los nuevos datos, extender el tiempo de prueba $\tau_r$ y realizar una auditoría de causa raíz sobre el proceso de construcción.

---

\newpage

## 2.6. Deuda Técnica en "Agile and software engineering, an invisible bond"

En el artículo de investigación de **Álvaro Ruiz de Mendarozqueta, Fabio O. Bustos y Pedro E. Colla**, se analiza cómo la adopción de metodologías ágiles sin una sólida base de prácticas de ingeniería de software formal deriva en una rápida acumulación de **deuda técnica**, degradando la capacidad del proyecto de generar valor sostenible.

### Factores Gestionados desde Calidad que Mejoran la Deuda Técnica
1. **Prácticas Continuas de Verificación (Integración Continua y TDD):** La automatización de pruebas unitarias y de regresión en cada commit/PR asegura una red de contención inmediata frente a regresiones.
2. **Inspecciones Sistemáticas de Código (Code Reviews):** La revisión por pares formalizada previene que atajos de diseño o antipatrones ingresen a la rama principal.
3. **Puertas de Calidad Automatizadas (Quality Gates):** La imposición de umbrales estrictos de cobertura ($\ge 85\%$), análisis estático de tipado (`mypy`/`pyright`), linters (`ruff`/`black`) y escaneo de vulnerabilidades (`bandit`).
4. **Visibilización y Monitoreo del Costo de la Pobre Calidad (CoPQ):** Cuantificar el esfuerzo invertido en retrabajo frente a nuevas funcionalidades para que la deuda técnica sea un factor visible en el backlog.

### Por Qué Producen esa Mejora
Porque acortan drásticamente el bucle de retroalimentación (*feedback loop*). En lugar de acumular defectos de arquitectura que generan "intereses financieros compuestos" (donde corregir una falla en producción cuesta entre 10 y 100 veces más que en la etapa de desarrollo), la calidad gestionada eleva el PCE y remueve los defectos en el momento exacto de su inyección, preservando la agilidad del equipo a largo plazo.

---

## 2.7. Impacto de una Multa en el Punto de Equilibrio del Proceso de Garantía

En los modelos económicos de garantía de software, el **punto de equilibrio (*break-even point*)** representa el nivel de calidad y duración de pruebas en el cual el costo marginal de extender el testeo iguala al costo marginal de fallas evitadas en el período de posventa:

$$\frac{d C_{\text{test}}(\tau)}{d\tau} = -\frac{d W_{\text{garantía}}(\tau)}{d\tau}$$

### Efecto de la Aplicación de una Multa Contractual
Cuando el cliente o el marco regulatorio introduce una **multa o penalización económica por falla en producción** ($M$):
1. **Incremento del Costo Unitario de Falla:** El costo asociado a cada defecto latente que escapa a la liberación aumenta drásticamente: $C_{\text{defecto}} \to C_{\text{reparación}} + M$.
2. **Aumento de la Pendiente de Costo de Garantía:** La curva de costo de garantía $W(\tau)$ se traslada hacia arriba y se vuelve mucho más empinada.
3. **Desplazamiento del Punto de Equilibrio:**
   - **Exigencia de Calidad Superior:** El punto de equilibrio se desplaza hacia un nivel de exigencia de contención mucho más estricto (menor tolerancia a defectos residuales $\delta_r$).
   - **Prolongación del Tiempo Óptimo de Prueba ($\tau_r^*$):** Económicamente, a la organización le resulta mucho más rentable extender la duración del período de test y aumentar la exhaustividad de V&V, ya que el costo marginal de realizar pruebas adicionales es significativamente inferior al riesgo financiero y legal de incurrir en la multa.

---

\newpage

# Bloque 3: Proyecto `json2csv.py` y Marco de CI/CD

## 3.1. Arquitectura y Estrategia de Filtro

La herramienta `json2csv.py` fue concebida bajo el patrón arquitectónico de **Filtro UNIX / Pipeline**, procesando flujos de datos continuos sin acoplarse al almacenamiento físico:

```
[ Entrada: sys.stdin o Archivo -i ] 
             │
             ▼
   [ json.loads (Parser) ]
             │
             ▼
[ aplanar_diccionario (Normalizador) ] 
             │
             ▼
[ csv.DictWriter (Formateador con -d) ]
             │
             ▼
[ Salida: sys.stdout o Archivo -o ]
```

### Funcionalidades Destacadas
- **Aplanamiento Recursivo:** Los objetos JSON jerárquicos se aplanan automáticamente utilizando notación de puntos (ej: `{"cliente": {"direccion": {"ciudad": "Paraná"}}}` genera la columna `cliente.direccion.ciudad`).
- **Registros Heterogéneos:** Extrae dinámicamente la unión ordenada de claves presentes a lo largo de toda la colección de objetos, rellenando valores nulos para aquellos registros que omitan determinados campos.
- **Manejo Robusto de Excepciones:** Retorna códigos de error estándar en el sistema operativo:
  - `0`: Ejecución exitosa.
  - `1`: `FileNotFoundError` (archivo no encontrado).
  - `2`: `PermissionError` (permiso denegado).
  - `3`: `json.JSONDecodeError` (sintaxis JSON inválida con reporte de fila/columna).
  - `4`: `ValueError` (delimitador inválido o estructura no convertible).

---

\newpage

## 3.2. Verificación de Requisitos de Calidad e Ingeniería (Puntos a - u)

Se validó el cumplimiento riguroso de cada uno de los ítems requeridos por la consigna del trabajo práctico:

### Estructura y Entorno del Proyecto (Ítems a - f)

| Ítem | Requisito Exigido en el PDF | Estado | Evidencia de Cumplimiento |
| :---: | :--- | :---: | :--- |
| **a** | Ambiente virtual Python (`venv`) | **CUMPLIDO** | Entorno creado en `venv/` con Python 3.14.5. |
| **b** | Esqueleto de proyecto CookieCutter | **CUMPLIDO** | Estructura modular `src/`, `tests/`, `docs/`, `samples/`, `pyproject.toml`. |
| **c** | Registro de Prompts de IA en `CONTEXT.md` | **CUMPLIDO** | Documento `CONTEXT.md` generado con bitácora detallada. |
| **d** | Descripción del proyecto en `README.md` | **CUMPLIDO** | `README.md` con arquitectura, ejemplos y badges. |
| **e** | Registro de cambios en `CHANGELOG.md` | **CUMPLIDO** | Formato *Keep a Changelog* en `CHANGELOG.md`. |
| **f** | Archivo `REQUIREMENTS.TXT` generado | **CUMPLIDO** | Dependencias fijadas y verificadas en `REQUIREMENTS.TXT`. |

\newpage

### Documentación, Versión y Control Estático (Ítems g - l)

| Ítem | Requisito Exigido en el PDF | Estado | Evidencia de Cumplimiento |
| :---: | :--- | :---: | :--- |
| **g** | Licencia MIT y documentación con `pdoc` | **CUMPLIDO** | Archivo `LICENSE` MIT y carpeta `docs/` con HTMLs autogenerados. |
| **h** | Registro de `VERSION` y `BUILD` | **CUMPLIDO** | Archivos `VERSION` (1.0.0) y `BUILD` (20261013.1). |
| **i** | Validación con `ruff` sin errores | **CUMPLIDO** | `ruff check json2csv.py src/ tests/` $\to$ **All checks passed!** |
| **j** | Formato consistente con `black` | **CUMPLIDO** | `black --check json2csv.py src/ tests/` $\to$ **0 dif (All done!)** |
| **k** | Reglas de formateo PEP 8 con `flake8` | **CUMPLIDO** | `flake8 --max-line-length=88` $\to$ **0 errores**. |
| **l** | Docstrings bajo PEP 257 con `pydocstyle` | **CUMPLIDO** | `pydocstyle` $\to$ **0 observaciones**. |

\newpage

### Tipado, Pruebas, Seguridad y CI/CD (Ítems m - u)

| Ítem | Requisito Exigido en el PDF | Estado | Evidencia de Cumplimiento |
| :---: | :--- | :---: | :--- |
| **m** | Chequeo estático con `MyPy` sin errores | **CUMPLIDO** | `mypy json2csv.py src/` $\to$ **Success: no issues found!** |
| **n** | Chequeo estático con `PyRight` sin errores | **CUMPLIDO** | `pyright` $\to$ **0 errors, 0 warnings**. |
| **o** | Pruebas con `Pytest` (cobertura $\ge 85\%$) | **CUMPLIDO** | **42 pruebas superadas** con **92% de cobertura**. |
| **p** | Análisis de seguridad con `bandit` | **CUMPLIDO** | `bandit -r json2csv.py src/` $\to$ **No issues identified!** |
| **q** | No utilizar Trufflehog | **CUMPLIDO** | Control de seguridad resuelto exclusivamente mediante Bandit. |
| **r** | Documentación de funcionamiento de módulos | **CUMPLIDO** | Incluida en `README.md` y docstrings de paquetes. |
| **s** | Actualización de `requirements.txt` | **CUMPLIDO** | Archivo `requirements.txt` sincronizado. |
| **t** | Workflow automatizado de CI/CD | **CUMPLIDO** | Pipeline en `.github/workflows/ci.yml`. |
| **u** | Generación de documentación en cada PR | **CUMPLIDO** | Tarea `pdoc` integrada en el job de GitHub Actions. |

---

\newpage

# Conclusión

El presente trabajo práctico ha integrado de manera armónica los aspectos teóricos y prácticos de la **Gestión de Calidad en Ingeniería de Software**: desde las fases fundamentales de Verificación y Validación (inspección estática, diseño de casos de prueba, matrices RTMX y métricas de contención PCE), pasando por la modelización matemática de confiabilidad y costos de garantía, hasta la construcción de una herramienta de software moderna gobernada por un pipeline de Integración Continua con estrictas puertas de calidad (*Quality Gates*).
