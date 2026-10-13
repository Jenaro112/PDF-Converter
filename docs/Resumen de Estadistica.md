---
coverConfig:
  showCover: false
  title: Resumen de Estadistica
  subtitle: ''
  materia: ''
  coverStyle: blanca_simple
  showLogo: true
  integrantes: []
  profesores: []
  sigla: ''
  fecha: ''
  showHeader: true
  showFooter: true
activeTheme: minimal
---
# **Resumen de Probabilidad y Estadística**

---

## **1. Modelos Probabilísticos Continuos**

### **1.1 Concepto de Variable Aleatoria Continua**

- **Definición formal:** Una variable aleatoria $X$ es ==variable aleatoria continua==(celeste) cuando proviene de un proceso de **medición** y puede asumir **infinitos valores** dentro de un intervalo real $\mathbb{R}$.
- **Probabilidad puntual nula:**  
  $$P(X = x) = 0$$  
  Para toda variable continua, la probabilidad en un punto individual es estrictamente **cero**.
- **Probabilidad sobre intervalos:** La probabilidad se calcula exclusivamente integrando el **área bajo la curva** de su función de densidad de probabilidad $f(x)$:  
  $$P(a \le X \le b) = \int_{a}^{b} f(x) \, dx$$
- **Condiciones obligatorias de la función de densidad:**
  - **No negatividad:** $f(x) \ge 0 \quad \forall x \in \mathbb{R}$
  - **Área total unitaria:** $\int_{-\infty}^{\infty} f(x) \, dx = 1$ (representa el 100% de probabilidad del espacio muestral).

---

### **1.2 Distribución Normal (Gaussiana)**

#### **A. Definición y Notación**
Una variable aleatoria continua $X$ sigue una distribución normal con parámetros de **media** $\mu$ ($-\infty < \mu < \infty$) y **varianza** $\sigma^2$ ($\sigma > 0$), denotada formalmente como:

$$X \sim N(\mu, \sigma^2)$$

#### **B. Función de Densidad**
$$
f(x) = \frac{1}{\sigma \sqrt{2\pi}} \cdot e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2} \quad (-\infty < x < \infty)
$$

*(con constantes $\pi \approx 3.14159$ y $e \approx 2.71828$)*.

#### **C. Características y Propiedades Fundamentales**
- **Forma acampanada y simétrica:** La curva es perfectamente simétrica respecto a la media poblacional $\mu$.
- **Coincidencia de medidas centrales:** En el eje central coinciden exactamente la media, la mediana y la moda:  
  $$\mathbf{\mu = Me = Mo}$$
- **Área total bajo la curva:** El área total es igual a **1** (repartida en exactamente **0.5** a la izquierda de $\mu$ y **0.5** a la derecha).
- **Comportamiento asintótico:** La curva desciende suavemente hacia ambos extremos; cuando $x \to \pm\infty$, la función tiende a cero pero **nunca toca el eje horizontal**.
- **Punto máximo absoluto:** Se ubica exactamente en la media:  
  $$\left(\mu; \; \frac{1}{\sigma \sqrt{2\pi}}\right)$$
- **Puntos de inflexión:** Puntos exactos donde la curvatura cambia de cóncava hacia abajo a cóncava hacia arriba:  
  $$\mathbf{x = \mu - \sigma} \qquad \text{y} \qquad \mathbf{x = \mu + \sigma}$$
- **Regla Empírica de Dispersión:**
  - **$P(\mu - \sigma \le X \le \mu + \sigma) \approx 0.6827$** (el **68.27%** de los datos cae a $\pm 1$ desvío).
  - **$P(\mu - 2\sigma \le X \le \mu + 2\sigma) \approx 0.9545$** (el **95.45%** de los datos cae a $\pm 2$ desvíos).
  - **$P(\mu - 3\sigma \le X \le \mu + 3\sigma) \approx 0.9973$** (el **99.73%** de los datos cae a $\pm 3$ desvíos).

```stats-plot
type: normal
mu: 0
sigma: 1
shade: [-1, 1]
shadeLabel: "P(-1 ≤ Z ≤ 1) ≈ 68.27%"
title: "Distribución Normal Estándar N(0, 1)"
subtitle: "Media μ = 0, Desvío σ = 1. Puntos de inflexión en μ ± σ"
xLabel: "Variable tipificada (Z)"
```

#### **D. Rol e Influencia de los Parámetros**
- **Media ($\mu$):** Parámetro de ==posición / localización==(amarillo). Desplaza la campana horizontalmente a lo largo del eje $x$ sin alterar su ancho ni su altura.
- **Desvío estándar ($\sigma$):** Parámetro de ==forma / dispersión==(naranja).
  - **A mayor $\sigma$:** Mayor variabilidad, la campana se aplana y se ensancha.
  - **A menor $\sigma$:** Menor variabilidad, la campana es más estilizada, puntiaguda y concentrada en torno a $\mu$.
  - Por lo tanto, para infinitas combinaciones de $\mu$ y $\sigma$ existen **infinitas curvas normales**.

#### **E. Estandarización y Variable Tipificada $Z$**
Transforma cualquier variable $X \sim N(\mu, \sigma^2)$ en una ==distribución normal estándar==(celeste) $Z \sim N(0, 1)$ con media $0$ y desvío $1$:

$$
Z = \frac{X - \mu}{\sigma}
$$

- **Demostración de la Media $E(Z) = 0$:**
  $$E(Z) = E\left(\frac{X - \mu}{\sigma}\right) = \frac{E(X) - \mu}{\sigma} = \frac{\mu - \mu}{\sigma} = 0$$

- **Demostración de la Varianza $\text{Var}(Z) = 1$:**
  $$\text{Var}(Z) = \text{Var}\left(\frac{X - \mu}{\sigma}\right) = \frac{1}{\sigma^2} \text{Var}(X - \mu) = \frac{1}{\sigma^2} \text{Var}(X) = \frac{\sigma^2}{\sigma^2} = 1$$

- **Cálculo de probabilidad mediante la tabla normal:**
  $$P(x_1 \le X \le x_2) = P\left(\frac{x_1 - \mu}{\sigma} \le Z \le \frac{x_2 - \mu}{\sigma}\right) = \Phi(z_2) - \Phi(z_1)$$

\newpage

### **1.3 Distribución t de Student**

#### **A. Definición y Función de Densidad**
Se utiliza para realizar inferencia sobre la **media poblacional $\mu$** cuando la **varianza poblacional $\sigma^2$ es desconocida** y se dispone de una **muestra pequeña ($n < 30$)**, estimando $\sigma$ a través del desvío muestral $s$. Su función de densidad es:

$$
h(t) = \frac{\Gamma\left(\frac{n+1}{2}\right)}{\Gamma\left(\frac{n}{2}\right)\sqrt{\pi n}} \cdot \left(1 + \frac{t^2}{n}\right)^{-\frac{n+1}{2}} \quad (-\infty < t < \infty)
$$

*(donde $\Gamma(n) = \int_0^\infty e^{-x} x^{n-1} dx$ es la función Gamma)*.

#### **B. Propiedades Clave**
- **Simetría:** Es acampanada y simétrica respecto a $\mathbf{t = 0}$, con media $E(t) = 0$.
- **Colas pesadas:** Presenta ==colas pesadas==(naranja) (más gruesas y levantadas) y una cúspide central más baja que la Normal estándar $Z$, absorbiendo la mayor incertidumbre propia de muestras pequeñas.
- **Parámetro determinante:** Depende exclusivamente de sus ==grados de libertad==(amarillo):  
  $$\mathbf{k = \nu = n - 1}$$
- **Fundamento de los grados de libertad ($n - 1$):** Al estimar previamente la media muestral $\bar{X}$, solo $n - 1$ observaciones son libres de variar de manera independiente; la última observación queda rígidamente fijada por la suma muestral total.
- **Convergencia asintótica:** A medida que aumentan los grados de libertad, la curva $t$ converge hacia la Normal estándar $Z$. A partir de **$n \ge 30$**, ambas distribuciones son prácticamente idénticas.
- **Requisito fundamental:** La población original de donde se extraen los datos debe seguir una **distribución normal**.

```stats-plot
type: compare_normal_student
df: 3
df2: 10
title: "Comparación: Distribución Normal Z vs. t de Student"
subtitle: "A menores grados de libertad (gl = 3), colas más pesadas y centro más bajo"
xLabel: "Valores estandarizados (t, Z)"
```

---

### **1.4 Distribución Chi-Cuadrado ($\chi^2$)**

#### **A. Definición y Origen**
Surge de la suma de los cuadrados de $k$ variables normales estándar independientes:

$$
\chi^2 = Z_1^2 + Z_2^2 + \dots + Z_k^2
$$

Su único parámetro rector son sus ==grados de libertad==(amarillo) ($gl = k$).

#### **B. Función de Densidad**
$$
f(x) = \frac{1}{2^{k/2} \Gamma(k/2)} \cdot x^{\frac{k}{2} - 1} \cdot e^{-\frac{x}{2}} \quad (x > 0)
$$

#### **C. Propiedades Clave**
- **Valores no negativos:** Su soporte es estrictamente $\mathbf{\chi^2 \ge 0}$. No puede asumir valores negativos por tratarse de una suma de términos elevados al cuadrado.
- **Asimetría positiva:** Para grados de libertad pequeños, la distribución está fuertemente sesgada a la derecha y concentrada cerca de cero.
- **Convergencia a la normal:** Al incrementarse los grados de libertad ($k$), la curva se desplaza a la derecha, se aplana y se vuelve progresivamente simétrica, aproximándose a una campana normal.
- **Media y Varianza:**
  $$\mathbf{E(\chi^2) = k} \qquad \mathbf{\text{Var}(\chi^2) = 2k}$$
- **Área total:** El área total bajo la curva de densidad es igual a **1**.
- **Aplicación principal:** Se emplea para realizar estimaciones y contrastes sobre la ==varianza poblacional ($\sigma^2$)==(naranja) o desviación estándar a partir de una muestra.

```stats-plot
type: chi2
dfs: [2, 4, 8]
title: "Distribución Chi-Cuadrado (χ²) según Grados de Libertad (k)"
subtitle: "Soporte no negativo (x ≥ 0) y convergencia simétrica al aumentar k"
xLabel: "Valores de χ²"
```

---

### **1.5 Cuadro Comparativo de Modelos Continuos**

| Modelo Continuo | Soporte | Parámetros | Condiciones de Aplicación | Parámetro que Infiere |
| :--- | :--- | :--- | :--- | :--- |
| **Normal ($Z$)** | $(-\infty, \infty)$ | $\mu$ (media), $\sigma$ (desvío) | Desvío $\sigma$ poblacional conocido **O** muestra grande ($n \ge 30$) | Media poblacional ($\mu$) |
| **t de Student ($t$)** | $(-\infty, \infty)$ | $k = n - 1$ ($gl$) | Muestra pequeña ($n < 30$), $\sigma$ desconocido (usa $s$), población normal | Media poblacional ($\mu$) |
| **Chi-Cuadrado ($\chi^2$)** | $[0, \infty)$ | $k$ ($gl$) | Suma de normales al cuadrado, población normal | Varianza poblacional ($\sigma^2$) |

\newpage

---

## **2. Teoría del Muestreo**

### **2.1 Fundamento del Muestreo**

- **Concepto:** Hacer un muestreo consiste en ejecutar el procedimiento adecuado para seleccionar un subconjunto que represente fielmente las características de la población.
- **Los 6 Motivos Fundamentales para Trabajar con Muestras:**
  - **1. Económicamente imposible:** Inspeccionar o medir a la totalidad insumiría costos financieros y de instrumental desmedidos.
  - **2. Factor tiempo / Rapidez:** El censo insume semanas o meses; una muestra aporta información rápida para tomar decisiones oportunas.
  - **3. Calidad y fatiga:** Medir excesivos elementos genera errores humanos o de calibración por saturación, apuro o cansancio operativo.
  - **4. Uniforme (Homogeneidad del proceso):** En procesos automatizados o constantes, una muestra reducida es suficiente para representar al conjunto.
  - **5. Proceso destructivo:** Cuando la medición inutiliza o destruye la unidad analizada (ensayos de rotura o tracción), un censo destruiría toda la producción.
  - **6. Población infinita o inaccesible:** Poblaciones que conceptualmente no tienen fin o físicamente no pueden abarcarse en su totalidad.
- **Criterio de tamaño de muestra de la cátedra:** Se considera una muestra representativa y válida si abarca ==como mínimo el 30% de la población==(verde).

---

### **2.2 Lenguaje y Terminología del Muestreo**

- **Población ($N$):** Conjunto total de elementos bajo estudio que comparten una característica observable común.
- **Muestra ($n$):** Subconjunto de elementos seleccionados a partir de la población.
- **Parámetro:** Medida numérica fija y constante que describe una característica de toda la **población**. Suele ser desconocido:
  - **Media poblacional:** $\mu$
  - **Varianza poblacional:** $\sigma^2$
  - **Desvío estándar poblacional:** $\sigma$
  - **Proporción poblacional:** $p$
- **Estadístico:** Medida numérica calculada a partir de los datos observados en la **muestra**. Es una ==variable aleatoria==(rosa) porque su valor cambia con cada muestra extraída:
  - **Media muestral:** $\bar{X}$
  - **Varianza muestral:** $s^2$
  - **Desvío estándar muestral:** $s$
  - **Proporción muestral:** $\hat{p}$
- **Estimador:** Función, regla matemática o fórmula utilizada para inferir el valor de un parámetro poblacional a partir de un estadístico muestral.

---

### **2.3 Muestreos Probabilísticos**

Cada elemento de la población tiene una **probabilidad conocida y no nula** de ser seleccionado. Son los únicos métodos que garantizan representatividad estadística rigurosa y permiten acotar el error de muestreo.

#### **1. Muestreo Aleatorio Simple (MAS)**
Todos los individuos de la población tienen exactamente la misma probabilidad de ser elegidos al inicio del proceso.
- **Procedimiento:** 1) Definir población $N$ $\to$ 2) Asignar código único $\to$ 3) Definir tamaño $n$ $\to$ 4) Selección por sorteo, tablas aleatorias o software.
- **Modalidades de selección:**
  - **Con reemplazo (con reposición):** Cada elemento extraído se devuelve al lote antes del siguiente sorteo.  
    $$\mathbf{M = N^n} \quad \text{(Número de muestras posibles)}$$
  - **Sin reemplazo (sin reposición):** El elemento extraído no regresa; evita duplicados en la muestra (método más eficiente).  
    $$\mathbf{M = \binom{N}{n} = \frac{N!}{n!(N-n)!}} \quad \text{(Combinaciones posibles)}$$

#### **2. Muestreo Sistemático**
Se selecciona de forma aleatoria el primer elemento y los siguientes a intervalos regulares fijos.
- **Procedimiento:**
  - **Paso 1:** Calcular el intervalo o salto de muestreo:  
    $$\mathbf{i = \frac{N}{n}}$$
  - **Paso 2:** Elegir un número inicial de arranque al azar $r$ tal que $1 \le r \le i$.
  - **Paso 3:** Los elementos elegidos son:  
    $$\mathbf{r, \; r+i, \; r+2i, \; r+3i, \; \dots}$$
- **Requisito mandatorio:** La lista debe estar ordenada de forma uniforme y coherente, asegurando que no existan periodicidades ocultas que coincidan con el salto $i$.

#### **3. Muestreo Estratificado**
La población se divide en subgrupos llamados ==estratos==: grupos **internamente homogéneos** (muy parecidos entre sí dentro del estrato) y **externamente heterogéneos** (muy diferentes entre estratos distintos). Se toma una muestra independiente dentro de **todos y cada uno** de los estratos.
- **Tipos de afijación (reparto de la muestra $n$ entre estratos):**
  - **Afijación simple:** Asigna el mismo número de elementos a cada estrato ($n_h = n / L$), sin importar su peso real.
  - **Afijación proporcional:** La cantidad asignada es proporcional al peso de cada estrato en la población ($n_h = n \cdot \frac{N_h}{N}$). Es el método más frecuente.
  - **Afijación óptima:** Considera el tamaño poblacional del estrato ($N_h$) y su dispersión interna ($\sigma_h$):  
    $$n_h = n \cdot \frac{N_h \sigma_h}{\sum N_i \sigma_i}$$

#### **4. Muestreo por Conglomerados (o por Racimos)**
Aprovecha grupos naturales preexistentes en la población (sucursales, facultades, escuelas, comisiones, distritos).
- **Estructura interna:** Los conglomerados son **internamente heterogéneos** (reflejan la diversidad poblacional) y **externamente homogéneos** (parecidos entre sí).
- **Procedimiento:** Se seleccionan al azar **algunos conglomerados completos** y se analizan todos los elementos dentro de ellos.
- **Subtipos según etapas:**
  - **Monoetápico (una etapa):** Se analizan todos los miembros de los conglomerados sorteados.
  - **Bietápico (dos etapas):** Se sortean conglomerados y luego se extrae una submuestra dentro de ellos.
  - **Polietápico:** Múltiples etapas jerárquicas de sorteo.

---

### **2.4 Muestreos No Probabilísticos**

La selección depende del criterio, juicio o facilidad del analista; no todos los individuos tienen probabilidad de ser elegidos.

- **Casos de aplicación legítima:**
  - Carencia de marco muestral o listado de la población.
  - Exigencia de rapidez crítica o presupuesto nulo.
  - Búsqueda de casos con perfiles o atributos muy específicos.
  - Poblaciones de difícil localización, cerradas u ocultas.
  - Estudios preliminares o exploratorios iniciales.
- **Métodos principales:**
  - **A conveniencia o intencional:** Selección guiada por juicio personal o facilidad de acceso del investigador.
  - **Casual, incidental o fortuito:** Basado en la disponibilidad inmediata (el analista se conforma con los elementos que tiene al alcance).
  - **Bola de nieve (*Snowball*):** Se ubican pocos sujetos iniciales y ellos contactan a otros integrantes (indispensable para poblaciones ocultas o con reserva).
  - **Por cuotas o accidental:** Se fijan metas numéricas por categoría, pero la elección interna no es aleatoria.
  - **Poblaciones móviles:** Muestreo en puntos de tránsito o flujos continuos.

---

### **2.5 Comparación: Muestreo Estratificado vs. Conglomerados**

| Criterio | Muestreo Estratificado | Muestreo por Conglomerados |
| :--- | :--- | :--- |
| **Origen del subgrupo** | Creado artificialmente por el investigador | Agrupamiento natural ya existente en la población |
| **Composición interna** | **Homogénea** (elementos idénticos o similares) | **Heterogénea** (cada grupo refleja la población) |
| **Comparación entre grupos** | **Heterogénea** (los estratos difieren fuertemente) | **Homogénea** (los conglomerados se parecen entre sí) |
| **Procedimiento de selección** | Se extrae una muestra de **todos los estratos** | Se eligen al azar **algunos conglomerados completos** |
| **Objetivo principal** | Maximizar la **precisión estadística** | Optimizar la **logística y reducir costos de traslado** |

\newpage

---

## **3. Distribuciones Muestrales**

### **3.1 Distribución Muestral de la Media ($\bar{X}$)**

Si de una población se extraen todas las muestras posibles de tamaño $n$ y a cada una se le calcula su media $\bar{x}$, el conjunto resultante de todas esas medias conforma la ==distribución muestral de la media==(celeste).

#### **A. Esperanza Matemática (Media de Medias)**
$$\mathbf{\mu_{\bar{X}} = E(\bar{X}) = \mu}$$

- **Demostración para $M$ muestras posibles:**
  $$\mu_{\bar{X}} = \frac{\sum_{i=1}^M \bar{x}_i}{M} = \mu$$
- **Propiedad:** Las medias de muestras individuales varían, pero su promedio general es exactamente igual a la media poblacional verdadera. Por lo tanto, $\bar{X}$ es un ==estimador insesgado==(verde) de $\mu$.

#### **B. Varianza y Error Estándar de la Media**
El desvío estándar de las medias muestrales se denomina formalmente ==Error Estándar== ($\sigma_{\bar{X}}$):

- **1. Poblaciones infinitas o Muestreo con reposición:**
  $$\mathbf{\sigma^2_{\bar{X}} = \frac{\sigma^2}{n}} \qquad \Longrightarrow \qquad \mathbf{\sigma_{\bar{X}} = \frac{\sigma}{\sqrt{n}}}$$
  *(A mayor tamaño de muestra $n$, la dispersión de las medias decrece notablemente).*

- **2. Poblaciones finitas ($N$) sin reposición ($\frac{n}{N} \ge 0.05$):**  
  Cuando la muestra supera el 5% de la población, debe aplicarse el **Factor de Corrección por Población Finita (CPF)**:
  $$\mathbf{\text{CPF} = \sqrt{\frac{N - n}{N - 1}}}$$
  $$\mathbf{\sigma^2_{\bar{X}} = \frac{\sigma^2}{n} \cdot \left(\frac{N - n}{N - 1}\right)} \qquad \Longrightarrow \qquad \mathbf{\sigma_{\bar{X}} = \frac{\sigma}{\sqrt{n}} \cdot \sqrt{\frac{N - n}{N - 1}}}$$

#### **C. Teorema Central del Límite (TCL)**
- **Población normal:** $\bar{X}$ tiene distribución normal para **cualquier** tamaño de muestra $n$.
- **Población no normal:** A medida que $n$ crece, la distribución de $\bar{X}$ se aproxima a una distribución normal con media $\mu$ y desvío $\sigma / \sqrt{n}$.
- **Criterio formal:** Para **$n \ge 30$**, la aproximación normal es plenamente válida sin importar la distribución de la población de origen.

---

### **3.2 Distribución Muestral de la Varianza y Varianza Corregida**

Al calcular la varianza de todas las muestras posibles surgen dos fórmulas con propiedades matemáticas distintas:

#### **A. Varianza Muestral Ordinaria ($s^2$) — Estimador Sesgado**
Calculada dividiendo por el tamaño total de la muestra $n$:

$$s^2 = \frac{\sum_{i=1}^n (x_i - \bar{x})^2}{n}$$

- **Esperanza matemática en poblaciones con reposición:**
  $$\mu_{s^2} = E(s^2) = \frac{n - 1}{n} \cdot \sigma^2 \neq \sigma^2$$
- **Causa del sesgo:** Como $\frac{n - 1}{n} < 1$, la varianza ordinaria $s^2$ es un ==estimador sesgado==(rojo): en promedio subestima sistemáticamente la varianza real de la población.

#### **B. Varianza Muestral Corregida ($\hat{s}^2$ o $S^2$) — Estimador Insesgado**
Aplica la ==Corrección de Bessel==(verde), dividiendo por $n - 1$:

$$\hat{s}^2 = \frac{\sum_{i=1}^n (x_i - \bar{x})^2}{n - 1} = \frac{n}{n - 1} \cdot s^2$$

- **Esperanza matemática en poblaciones con reposición:**
  $$\mu_{\hat{s}^2} = E(\hat{s}^2) = \sigma^2$$
- **Conclusión:** Al dividir por $n - 1$, la media de las varianzas muestrales coincide exactamente con la varianza poblacional $\sigma^2$ ($\hat{s}^2$ es un ==estimador insesgado==(verde)).
- **¿Por qué dividir por $n - 1$?:** Al calcular los desvíos respecto a la media muestral $\bar{x}$, se consume un grado de libertad de la información muestral; dividir por $n - 1$ compensa esa restricción algebraica.

#### **C. Caso de Poblaciones Finitas sin Reposición ($\frac{n}{N} \ge 0.05$)**
El factor de corrección para las medidas de dispersión de la varianza es $\frac{N}{N - 1}$:
- **Varianza corregida:**  
  $$\mathbf{\mu_{\hat{s}^2} = \frac{N}{N - 1} \cdot \sigma^2}$$
- **Varianza ordinaria:**  
  $$\mathbf{\mu_{s^2} = \frac{N}{N - 1} \cdot \frac{n - 1}{n} \cdot \sigma^2}$$

\newpage

---

## **4. Estimación de Parámetros (Estimación Puntual)**

*(Contenido formal de Inferencia Estadística centrado exclusivamente en la teoría de estimación)*

### **4.1 Modalidades de Estimación**

La inferencia estadística busca determinar características poblacionales a partir de los datos observados en una muestra a través de dos enfoques:

- **1. Estimación Puntual:** A partir de las observaciones de la muestra, se calcula un **único valor numérico** para estimar el parámetro poblacional:  
  $$\text{Estadístico } \hat{\theta} \xrightarrow{\quad \text{estimador} \quad} \text{Parámetro } \theta$$
- **2. Estimación por Intervalo de Confianza:** A partir de los datos muestrales, se calculan dos valores numéricos que definen un intervalo $[\hat{\theta} - a, \; \hat{\theta} + a]$ dentro del cual se espera que se ubique el parámetro con un determinado nivel de confianza ($1 - \alpha$).

---

### **4.2 Error Muestral y Sesgo**

#### **A. Error Muestral ($e$)**
Es la diferencia numérica entre el valor arrojado por el estimador y el verdadero parámetro poblacional:

$$e = \hat{\theta} - \theta$$

- **Propiedad fundamental:** El error muestral varía de una muestra a otra, por lo que es una **variable aleatoria**.

#### **B. Sesgo del Estimador ($S$)**
Es la diferencia entre la esperanza matemática (valor esperado promedio) del estimador y el parámetro poblacional a estimar:

$$S = E(\hat{\theta}) - \theta$$

- **Estimador insesgado:** Si $\mathbf{S = 0 \iff E(\hat{\theta}) = \theta}$, el estimador acierta en promedio al parámetro real.
- **Estimador sesgado:** Si $\mathbf{S \neq 0}$, el estimador presenta un desvío sistemático hacia valores mayores o menores que el parámetro.

---

### **4.3 Propiedades de los Buenos Estimadores**

Para evaluar y comparar la calidad técnica de diferentes estimadores se estudian cuatro propiedades matemáticas formales:

#### **1. Insesgabilidad (Insesgadez)**
Un estimador es insesgado si su esperanza matemática coincide exactamente con el parámetro poblacional correspondiente:

$$\mathbf{E(\hat{\theta}) = \theta}$$

- **Media aritmética:** $\bar{X}$ es un estimador insesgado de la media poblacional $\mu$:  
  $$E(\bar{X}) = \mu$$
- **Varianza corregida:** $\hat{s}^2$ es un estimador insesgado de la varianza poblacional $\sigma^2$:  
  $$E(\hat{s}^2) = \sigma^2$$
- **Varianza ordinaria:** $s^2$ es un estimador sesgado de $\sigma^2$:  
  $$E(s^2) = \frac{n - 1}{n} \sigma^2 \neq \sigma^2$$

#### **2. Eficiencia**
Dados dos o más estimadores insesgados $\hat{\theta}_1$ y $\hat{\theta}_2$ para un mismo parámetro $\theta$, el más **eficiente** es aquel cuya distribución muestral posee ==menor varianza==(amarillo):

$$\mathbf{\text{Var}(\hat{\theta}_1) < \text{Var}(\hat{\theta}_2) \implies \hat{\theta}_1 \text{ es más eficiente que } \hat{\theta}_2}$$

- El estimador más eficiente presenta menor dispersión y mayor concentración en torno al verdadero parámetro.
- **Comparación formal:** Al estimar la media poblacional $\mu$ comparando la media muestral $\bar{X}$ y la mediana muestral $Me$: como $\mathbf{\sigma^2_{\bar{X}} < \sigma^2_{Me}}$, la **media aritmética es un estimador más eficiente que la mediana**.

#### **3. Consistencia**
Un estimador es consistente si la probabilidad de que la diferencia absoluta entre el estimador y el parámetro sea menor que cualquier margen de error prefijado $\epsilon > 0$ tiende a **1** cuando el tamaño de la muestra tiende a infinito:

$$\mathbf{P(|\hat{\theta} - \theta| < \epsilon) \to 1 \quad \text{cuando } n \to \infty}$$

- A medida que el tamaño muestral crece, el estimador converge probabilísticamente al valor real del parámetro.

#### **4. Suficiencia**
Un estimador es ==suficiente==(violeta) si utiliza y agota **toda la información disponible** que la muestra contiene acerca del parámetro analizado.

- **Estimadores suficientes:**
  - **Media muestral ($\bar{X}$):** Utiliza en su cálculo el valor de cada una de las observaciones de la muestra:  
    $$\bar{x} = \frac{x_1 + x_2 + \dots + x_n}{n}$$
  - **Varianza muestral ($s^2$ o $\hat{s}^2$):** Utiliza la totalidad de los datos observados:  
    $$s^2 = \frac{\sum_{i=1}^n (x_i - \bar{x})^2}{n}$$
- **Estimadores NO suficientes:**
  - **Mediana ($Me$):** Únicamente utiliza la posición del dato central, descartando la magnitud de los restantes valores observados.
  - **Rango ($R = x_{\max} - x_{\min}$):** Solo utiliza el valor máximo y el mínimo observados, desperdiciando por completo toda la información de las observaciones intermedias.
