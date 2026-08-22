# ==Probabilidad==(amarillo)
# ==Probabilidad==(amarillo)
## Conceptos básicos

- **Probabilidad:** mide qué tan posible es que ocurra un suceso. Siempre: ==$0 \le P(A) \le 1$==(celeste)
- **Espacio muestral ($E$):** conjunto de todos los resultados posibles.
- **Suceso/evento ($A$):** conjunto de resultados que cumplen una condición.

## Definición clásica (a priori)

Se usa cuando el espacio muestral es ==finito, mutuamente excluyente y equiprobable==(celeste):

$$
P(A) = \frac{\text{casos favorables}}{\text{casos posibles}} = \frac{m}{n}
$$

- $P(A) = 1$ → ==evento seguro==(verde).
- $P(A) = 0$ → ==evento imposible==(rojo).
- Complementario: $P(A^c) = 1 - P(A)$.

## Definición frecuentista (a posteriori)

La probabilidad se aproxima mediante la frecuencia relativa. Al repetir muchas veces el experimento, la frecuencia relativa tiende a estabilizarse en la probabilidad del resultado.

## Operaciones con eventos

- **Unión ($A \cup B$):** ocurre A, B o ambos (==al menos uno==(celeste)).
- **Intersección ($A \cap B$):** ocurren A y B ==simultáneamente==(celeste).
- **Complemento ($A^c$):** no ocurre A.

## Regla de la suma

Para cualquier par de eventos:

$$
P(A \cup B) = P(A) + P(B) - P(A \cap B)
$$

Si son ==mutuamente excluyentes==(naranja), $P(A \cap B) = 0$ y queda $P(A \cup B) = P(A) + P(B)$.

## Probabilidad condicional

Indica la probabilidad de que ocurra A sabiendo que B ya ocurrió:

$$
P(A \mid B) = \frac{P(A \cap B)}{P(B)}, \qquad P(B) > 0
$$

Las tablas de contingencia organizan dos variables categóricas y permiten obtener probabilidades conjuntas, marginales y condicionales.

## Teorema de la multiplicación

Para eventos dependientes:

$$
P(A \cap B) = P(A) \cdot P(B \mid A)
$$

Es decir, la probabilidad de que ocurran ambos es el producto de la probabilidad del primero por la probabilidad del segundo sabiendo que el primero ocurrió.

## Eventos independientes

A y B son ==independientes==(celeste) cuando conocer que ocurrió uno no modifica la probabilidad del otro. En ese caso:

$$
P(A \cap B) = P(A)P(B)
$$

## Teorema de Bayes

Permite calcular probabilidades condicionales ==invirtiendo la condición==(celeste), incorporando información adicional:

$$
P(A \mid B) = \frac{P(B \mid A)P(A)}{P(B)}
$$

La idea central es usar información de un evento observado para obtener la probabilidad de otro evento relacionado.

> 🧠 **Tip:** Para resolver ejercicios: identificá el espacio muestral y los eventos → fijate si piden al menos uno (unión), ambos (intersección), sabiendo que (condicional) o una probabilidad “invertida” (Bayes) → elegí la fórmula correspondiente.

---

# ==Variable Aleatoria==(amarillo)

Una variable aleatoria $X$ de un espacio muestral $E$ es una función que le hace corresponder a cada elemento de $E$ un número real.

## Conceptos Básicos

- **Definición:** Una **variable aleatoria ($X$)** de un espacio muestral $E$ es una función que le asigna a cada resultado (elemento) de $E$ un ==**único número real**==(celeste).
- **Propósito:** Permite transformar resultados cualitativos o no numéricos de un experimento (ej. "Defectuoso" o "No Defectuoso") en valores numéricos concretos para su análisis matemático.

## Clasificación de las Variables Aleatorias

Las variables aleatorias se dividen en dos grandes grupos según la naturaleza de su espacio muestral:

### A. Variables Aleatorias Discretas (VAD)

- **Definición:** Tienen un espacio muestral finito o infinito numerable.
- **Característica clave:** Entre dos valores consecutivos ==**no existe** ningún valor intermedio==(naranja).
- _Ejemplos:_ Número de caras al lanzar monedas, cantidad de computadoras defectuosas, número de goles en un partido.

### B. Variables Aleatorias Continuas (VAC)

- **Definición:** Tienen un espacio muestral infinito no numerable.
- **Característica clave:** Entre dos valores cualesquiera de la variable ==**siempre existen** valores intermedios==(celeste).
- _Ejemplos:_ Cantidad de agua que se bebe (ej. $2.51$ litros), distancia recorrida, tiempo exacto de una llamada.

---

## Variables Aleatorias Discretas (VAD) en Detalle

### Función de Probabilidad

Es la función que asigna a cada valor posible del espacio muestral su valor de probabilidad correspondiente, denotado como $P(X_i)$.

### Función de Probabilidades Acumuladas

Denotada como $F(x)$, representa la probabilidad de que la variable aleatoria tome un valor menor o igual a $x_k$:

$$
F(x_k) = P(X \le x_k) = \sum_{i=1}^{k} P(x_i)
$$

### Esperanza Matemática y Varianza

- **Esperanza Matemática ($E(X)$ o $\mu$):** Representa el ==valor que se espera que ocurra en promedio==(celeste).
  $$
  E(X) = \sum_{i=1}^{n} X_i \cdot P(X_i) = \mu
  $$
- **Varianza ($Var(X)$ o $\sigma^2$):** Mide la ==dispersión de los datos respecto a la media==(rosa).
  $$
  Var(X) = E(X_i^2) - [E(X)]^2 = E(X_i^2) - \mu^2
  $$

---


<!-- PAGEBREAK -->


## Variables Aleatorias Continuas (VAC) en Detalle

A medida que el número de observaciones tiende a infinito ($n \rightarrow \infty$) y la amplitud de los intervalos tiende a cero, la distribución se representa mediante una curva continua y se usa la integral en lugar de la sumatoria.

### Función de Densidad de Probabilidad ($f(x)$)

Para que $f(x)$ sea válida, debe cumplir las siguientes propiedades matemáticas (analizables en intervalos cerrados de la forma $[a; b]$):

1. $f(x) \ge 0$ para todo $x \in \mathbb{R}$.
2. El área total bajo la curva debe ser ==exactamente 1==(celeste): $\int_{-\infty}^{\infty} f(x)dx = 1$.
3. La probabilidad en un intervalo $[a; b]$ se calcula con la integral definida:
   _Nota:_ En variables continuas, ==la probabilidad de un punto exacto es cero==(naranja), por lo tanto: $P(a \le x \le b) = P(a < x < b)$.
   $$
   P(a \le X \le b) = \int_{a}^{b} f(x)dx
   $$

### Función de Probabilidades Acumuladas

Calcula la probabilidad acumulada hasta un valor límite $x$:

$$
F(x) = \int_{-\infty}^{x} f(x)dx
$$


<!-- PAGEBREAK -->


### Esperanza y Varianza para VAC

Las fórmulas son análogas a las discretas, integrando sobre todo el dominio:

- **Esperanza:**
  $$
  E(X) = \int_{-\infty}^{\infty} X \cdot f(X) dX
  $$
- **Varianza:**
  $$
  Var(X) = E(X^2) - \mu^2
  $$

> 💭 Para sacar $E(x^2)$ debemos hacer $\int_{-\infty}^{\infty} x^2 \cdot f(x) dx$

---

## Propiedades Matemáticas Generales

### Propiedades de la Esperanza

- $E(c) = c$ (donde $c$ es una constante)
- $E(c \cdot X) = c \cdot E(X)$
- $E(X + Y) = E(X) + E(Y)$
- $E(X \cdot Y) = E(X) \cdot E(Y)$ _(==Sólo si X e Y son independientes==(naranja))_

### Propiedades de la Varianza

- $Var(c) = 0$
- $Var(X + c) = Var(X)$
- $Var(c \cdot X) = c^2 \cdot Var(X)$
- $Var(X + Y) = Var(X) + Var(Y)$ _(==Sólo si X e Y son independientes==(naranja))_

---

_Anexo: Regla práctica para la Varianza:_
Se parte de $Var(x) = E[(X - \mu_X)^2]$ y, aplicando el cuadrado de un binomio y las propiedades de la esperanza, se demuestra la forma simplificada $Var(X) = E(X^2) - \mu_X^2$.

---


<!-- PAGEBREAK -->


# ==Modelos Probabilísticos Discretos==(amarillo)

### ==Modelo de Bernoulli==(naranja)

**Condiciones:**

- Se realiza una ==sola prueba==(celeste).
- Las pruebas tienen dos resultados posibles (éxito y fracaso).

**Función de probabilidad:**

$$
f(x) = P(X=x) = p^x(1-p)^{1-x} \quad \text{con } x = 0; 1
$$

**Esperanza y Varianza:**

- **Media:** $\mu = E(x) = p$
- **Varianza:** $\sigma^2 = p(1-p)$

---

### ==Modelo Binomial==(naranja)

**Condiciones:**

- Existe un ==número finito de pruebas independientes==(celeste).
- Cada prueba tiene dos resultados posibles (éxito y fracaso).
- La probabilidad del éxito y fracaso son constantes en cada repetición.

**Generalizando:**

$$
b(k;n;p) = \binom{n}{k} \cdot p^k \cdot q^{n-k}
$$

- $n$: número de repeticiones de un suceso
- $k$: número de éxitos obtenidos
- $n-k$: número de fracasos obtenidos
- $p$: probabilidad de tener éxito
- $q$: probabilidad de obtener un fracaso


<!-- PAGEBREAK -->


**Esperanza y Varianza:**

- $E(X) = n \cdot p$
- $Var(X) = n \cdot p \cdot q$

---

### ==Distribución Hipergeométrica==(naranja)

**Condiciones:**

- Se extraen muestras de tamaño $n$ (==sin reposición==(rosa)) de un conjunto finito ($N$).
- En cada prueba existen dos resultados posibles (éxito y fracaso).
- Las pruebas son ==dependientes==(naranja).
- La probabilidad del éxito y fracaso varía de una prueba a otra.

**Generalizando:**

$$
h(x;n,k,N) = \frac{\binom{k}{x} \binom{N-k}{n-x}}{\binom{N}{n}}
$$

- Tamaño del lote: $N$ piezas
- Número de éxitos en el lote: $k$
- Número de fracasos en el lote: $N-k$
- Tamaño de la muestra: $n$ piezas
- Número de éxitos en la muestra: $x$
- Número de fracasos en la muestra: $n-x$

**Esperanza y Varianza:**

- $E(x) = n \cdot p$ con $p = \frac{k}{N}$
- $Var(x) = n \cdot p \cdot q \cdot \frac{N-n}{N-1}$ con $p = \frac{k}{N}$

**Aproximación de hipergeométrica mediante la binomial:**

- Si ==$\frac{n}{N} \le 5\%$==(verde) $\rightarrow$ Hipergeométrica o Binomial
- Si $\frac{n}{N} > 5\% \rightarrow$ Hipergeométrica

---


<!-- PAGEBREAK -->


### ==Distribución de Poisson==(naranja)

**Condiciones:**

- Se cuentan ocurrencias en un ==intervalo fijo de tiempo, espacio o longitud==(celeste).
- La tasa media de ocurrencia es constante.
- Las ocurrencias son independientes.
- La probabilidad del éxito es pequeña.
- El número de pruebas es grande.

**Fórmula:**

$$
P(X=k) = \frac{e^{-\lambda} \cdot \lambda^k}{k!}
$$

**Esperanza y Varianza:**

- La esperanza es: $\lambda = n \cdot p$
- $E(X) = \mu = \lambda$
- $Var(X) = \lambda$

**Aproximación de la binomial con Poisson:**

- Si ==$n \ge 100$ y $\mu < 10$==(verde)
