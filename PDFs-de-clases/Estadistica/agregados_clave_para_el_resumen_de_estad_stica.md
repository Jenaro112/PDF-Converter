# 🚨 PUNTOS CLAVE Y TRAMPAS FRECUENTES (Agregados al Resumen)

## 1. El dilema de la raíz: ¿Divido por $\sqrt{n}$ o por $\sqrt{n-1}$?

La regla depende exclusivamente de **dónde salió el desvío** que estás usando.

* **Uso $\sqrt{n}$ cuando:**
  * El enunciado me da la desviación **Poblacional ($\sigma$)**. Palabras clave: *"históricamente"*, *"estudios previos"*, *"se sabe que la población..."*.
  * Cargo datos sueltos en la calculadora y decido copiar el valor $s_x$ (Desvío muestral corregido o $\hat{s}$). Como este ya fue corregido por $n-1$ internamente, en la fórmula uso $\sqrt{n}$.

* **Uso $\sqrt{n-1}$ cuando:**
  * El enunciado me da la desviación de **la muestra ($s$)** ya calculada en el texto. Ej: *"Se toma una muestra de 55 frascos con una desviación de 0.5"*.
  * Cargo datos sueltos en la calculadora y decido copiar el valor $\sigma_x$ (Desvío muestral ordinario o $s$). Como a este le falta la corrección, se la agrego en la fórmula dividiendo por $\sqrt{n-1}$.

> **💡 Regla de oro para datos crudos en calculadora:**
> Ambas combinaciones dan EXACTAMENTE el mismo resultado: $\frac{s_x}{\sqrt{n}} = \frac{\sigma_x}{\sqrt{n-1}}$. ¡Elegí una y no las mezcles!

## 2. El idioma de los símbolos: Población vs. Muestra

El gran secreto acá es leer de dónde viene el dato. La estadística usa "alfabetos" distintos para que sepamos al instante si estamos hablando del universo total o de un grupito pequeño.

* **LETRAS GRIEGAS = POBLACIÓN (El total o lo histórico):**
  Se usan cuando el dato corresponde a **todos** los elementos posibles o es un dato histórico/teórico.
  * $\mu$ (Mu): Media poblacional (Ej: *"históricamente el peso promedio es..."*).
  * $\sigma$ (Sigma): Desviación estándar poblacional.
  * $N$ (Mayúscula): Tamaño total de la población.

* **LETRAS COMUNES = MUESTRA (Tus datos recolectados):**
  Se usan cuando el dato sale estrictamente del **grupito** que fuiste a encuestar, medir o probar.
  * $\bar{X}$ (X raya): Media muestral (Ej: *"en los 10 frascos analizados el promedio fue..."*).
  * $s$ (o $\hat{s}$): Desviación estándar muestral (la que calculás con los datos o te da la muestra).
  * $n$ (Minúscula): Tamaño de la muestra (Ej: *los 10 frascos*).

> **💡 Truco de lectura para parciales:**
> Si en el texto aparece la frase *"Se tomó una muestra de..."* o *"En 10 recorridos de prueba..."*, prestá muchísima atención: **TODO** lo que el texto te diga inmediatamente después de esa coma es letra común ($\bar{X}$ y $s$), porque esos números nacieron de esa muestra específica.

## 3. Diferencia entre calcular el Error ($e$) y la Muestra ($n$)

La fórmula $e = z \cdot \frac{\sigma}{\sqrt{n}}$ es la misma que $n = \left(\frac{z \cdot \sigma}{e}\right)^2$, pero se usan para cosas distintas:

* **Me piden el tamaño del error (Ej: "¿Cuál es el error de estimación?"):**
  Uso $e = z \cdot \frac{\sigma}{\sqrt{n}}$. Hago la cuenta y **TERMINO AHÍ**. Ese número es el "pedacito" que le sumo y le resto a la media ($\bar{X} \pm e$).

* **Me piden el tamaño de muestra (Ej: "¿Cuántos elementos necesito...?"):**
  Uso $n = \left(\frac{z \cdot \sigma}{e}\right)^2$. El enunciado me va a dar el valor de $e$ como dato (Ej: *"que el error no supere los 2 cm"*). Hago la cuenta y **SIEMPRE REDONDEO HACIA ARRIBA** al entero siguiente (ej: 1082,41 $\rightarrow$ 1083).

## 4. ¿Cuándo uso $Z$ (Normal) y cuándo $t$ de Student?

* **Uso $Z$ si:**
  * Conozco la desviación poblacional ($\sigma$).
  * O si la muestra es GRANDE ($n \ge 30$), sin importar qué desvío tenga.

* **Uso $t$ de Student si (se deben cumplir TODAS):**
  1. La muestra es CHICA ($n < 30$).
  2. No conozco la desviación poblacional (tuve que sacar $s$ de la muestra).
  3. La población de origen es Normal.
  * *Nota:* Para buscar en la tabla de $t$, siempre necesito los **grados de libertad ($gl = n - 1$)**.

## 5. Cómo sacar un valor crítico raro (Ej: 97% de confianza)

Si te piden un nivel de confianza que no está en la tabla básica (como 97%), hacé esto:

1. **Calculá el área central y el riesgo:** El centro es $0,97$. Sobra $0,03$ de riesgo ($\alpha$).
2. **Repartí el riesgo en dos colas:** $\frac{0,03}{2} = 0,015$.
3. **Buscá el área acumulada:** Sumá el centro más la cola izquierda: $0,97 + 0,015 = \mathbf{0,985}$.
4. **A la calculadora/tabla:** Buscá la Normal Inversa para un área de `0.985` y ese es tu valor crítico ($2,17$).

## 6. ⚠️ TRAMPAS MORTALES DE PARCIAL (¡Revisar antes de entregar!)

* **¿Me dieron Varianza o Desviación?** Si el enunciado dice *"varianza de 0,16"*, eso es $\sigma^2$. ¡Tenés que sacarle la raíz cuadrada ($\sqrt{0,16} = 0,4$) antes de meterla en la fórmula!
* **¿Están todas las unidades iguales?** Si el desvío está en metros (ej: $0,4\text{ m}$) y te piden un error máximo de centímetros (ej: $2\text{ cm}$), pasá todo a metros ($e = 0,02\text{ m}$) o todo a centímetros. NUNCA los mezcles en la fórmula de $n$.
* **Calculadora sucia:** Si los desvíos te dan raro, revisá la tabla de datos cargados. Un solo número mal tipeado (ej: 36 en vez de 35) te cambia toda la cuenta.