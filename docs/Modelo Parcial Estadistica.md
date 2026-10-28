---
coverConfig:
  showCover: false
  title: Guía de Modelos de Parcial - Probabilidad y Estadística
  subtitle: 50 Nuevos Ejercicios de Examen con Solucionario Detallado Paso a Paso
  materia: Probabilidad y Estadística
  coverStyle: blanca_simple
  showLogo: true
  integrantes: []
  profesores: []
  sigla: PyE
  fecha: ''
  showHeader: true
  headerLeft: '{sigla} - {titulo}'
  headerCenter: ''
  headerRight: '{fecha}'
  headerShowLine: true
  showFooter: true
  footerLeft: '{materia}'
  footerCenter: ''
  footerRight: ''
  footerNumbering: pagina_x_de_y
  footerShowLine: true
activeTheme: minimal
---
# 📚 **Guía Integral de Modelos de Parcial: 50 Nuevos Ejercicios**
### **Cátedra de Probabilidad y Estadística – Licenciatura e Ingeniería en Sistemas**

Esta guía contiene **50 ejercicios completamente nuevos** diseñados con el nivel, estilo y exigencia de los exámenes parciales y finales de la cátedra. 

> ⚠️ **Pauta pedagógica fundamental:**  
> En los enunciados **no se indican los símbolos algebraicos de las variables**. El estudiante debe deducir a partir del texto si cada cifra corresponde a la población o a la muestra, si la desviación estándar es conocida o desconocida, y qué modelo probabilístico corresponde aplicar.

Al finalizar la sección de enunciados se encuentra el **Solucionario Integral Paso a Paso**, donde se explican detalladamente la extracción de variables, el modelo adoptado, las operaciones matemáticas sin omisión de pasos y la conclusión analítica de cada problema.

---

## 📑 **Índice de Bloques Temáticos**

1. **Bloque I (Ej. 1 al 10):** Fundamentos Teóricos, Muestreo y Propiedades de Estimadores.
2. **Bloque II (Ej. 11 al 16):** Distribuciones Muestrales Empíricas y Verificación de Insesgadez.
3. **Bloque III (Ej. 17 al 26):** Distribución Normal y Aplicaciones del Teorema Central del Límite.
4. **Bloque IV (Ej. 27 al 36):** Intervalos de Confianza para la Media Poblacional.
5. **Bloque V (Ej. 37 al 42):** Factor de Corrección por Población Finita y Tamaño Óptimo de Muestra.
6. **Bloque VI (Ej. 43 al 46):** Muestras Pequeñas, Datos Directos y Control de Especificaciones Técnicas.
7. **Bloque VII (Ej. 47 al 50):** Intervalos de Confianza para la Varianza y Desviación Estándar (Chi-Cuadrado).
8. **Solucionario Paso a Paso:** Respuestas desarrolladas de los 50 ejercicios.

\newpage

---

# 📝 **ENUNCIADOS DE LOS 50 NUEVOS EJERCICIOS**

---

## 📌 **BLOQUE I: Teoría, Muestreo y Propiedades de Estimadores**

### **Ejercicio 1.** Transformación Lineal de la Normal Estándar
Si una variable aleatoria continua sigue una distribución normal con media y desviación estándar conocidas, y a partir de su variable estandarizada se define una nueva variable auxiliar mediante la relación lineal:
$$
W = 3Z + 5
$$
Determine formalmente la media esperada y la varianza de la variable $W$, aplicando propiedades de la esperanza matemática y de la varianza.

---

### **Ejercicio 2.** Sesgo de un Estimador Alternativo de la Varianza
Un investigador propone estimar la varianza poblacional utilizando como divisor el tamaño muestral incrementado en uno:
$$
T = \frac{\sum (X_i - \bar{X})^2}{n + 1}
$$
Demuestre algebraicamente que dicho estimador es sesgado, obtenga su valor esperado y exprese la magnitud exacta de su sesgo en función de la varianza poblacional.

---

### **Ejercicio 3.** Error de Muestreo vs. Error No Muestral
Distinga conceptualmente entre **error muestral** y **error no muestral**. Para cada una de las siguientes situaciones prácticas en auditorías de sistemas, clasifique a qué tipo de error corresponde y justifique:
1. Al auditar la satisfacción de usuarios de una aplicación móvil mediante una encuesta voluntaria en línea, solo el 4% responde, predominando opiniones de usuarios insatisfechos.
2. La media muestral calculada en una muestra de 50 servidores difiere en 2 ms de la media de todos los servidores del centro de cómputo por efecto del azar en la extracción.
3. Un sensor de temperatura defectuoso en una sala de racks registra sistemáticamente 1.5 °C por encima de la temperatura real.

---

### **Ejercicio 4.** Muestreo Estratificado con Afijación Proporcional
Una compañía tecnológica posee 1.200 empleados distribuidos en tres sedes: Sede Central (600 empleados), Sede Norte (360 empleados) y Sede Sur (240 empleados). Se desea realizar una auditoría laboral tomando una muestra estratificada de 100 empleados con asignación proporcional al tamaño de cada estrato.
1. Calcule la cantidad exacta de empleados que deben seleccionarse en cada sede.
2. Explique por qué este diseño resulta más eficiente que un muestreo aleatorio simple si existen grandes diferencias salariales entre sedes pero homogeneidad interna en cada una.

---

### **Ejercicio 5.** Muestreo por Conglomerados en Dos Etapas
Explique en qué consiste el muestreo bietápico por conglomerados. Indique en qué se diferencia del muestreo estratificado en cuanto a la homogeneidad o heterogeneidad dentro y entre los grupos, y plantee un ejemplo de aplicación en una red de 80 sucursales bancarias distribuidas en el país.

---

### **Ejercicio 6.** Comparación de Eficiencia entre Estimadores
Se dispone de una muestra aleatoria de tamaño 3 proveniente de una población normal con media desconocida y varianza finita. Se proponen dos estimadores insesgados para la media:
- La media muestral estándar: $\bar{X} = \frac{X_1 + X_2 + X_3}{3}$
- Un estimador ponderado: $T_1 = \frac{1}{2} X_1 + \frac{1}{4} X_2 + \frac{1}{4} X_3$
Demuestre formalmente cuál de los dos estimadores es más eficiente calculando la varianza de cada uno.

---

### **Ejercicio 7.** Consistencia y Convergencia en Probabilidad
Enuncie la definición matemática formal de un estimador consistente. Explique la relación entre la propiedad de consistencia y la Ley Débil de los Grandes Números aplicada a la media muestral.

---

### **Ejercicio 8.** Distribución Asintótica de la Suma Muestral
Si se extrae una muestra aleatoria de tamaño $n$ de una población con media y varianza finitas:
1. Deduzca la media esperada y la varianza de la suma muestral total: $T_n = \sum_{i=1}^n X_i$.
2. Enuncie la aproximación normal que establece el Teorema Central del Límite para dicha suma cuando el tamaño de la muestra es al menos 30.

---

### **Ejercicio 9.** Grados de Libertad en Modelos Inferenciales
Explique qué representa conceptualmente el número de "grados de libertad" en estadística inferencial. Fundamente por qué la varianza muestral calculada a partir de $n$ observaciones pierde un grado de libertad al trabajar con la restricción lineal:
$$
\sum_{i=1}^n (X_i - \bar{X}) = 0
$$

---

### **Ejercicio 10.** Propiedades Matemáticas de Chi-Cuadrado
Para una variable aleatoria que sigue una distribución Chi-Cuadrado con $k$ grados de libertad:
1. Indique su valor esperado y su varianza en función de $k$.
2. Enuncie la propiedad reproductiva o aditiva de variables Chi-Cuadrado independientes y explique su utilidad en la inferencia estadística de varianzas combinadas.

\newpage

---

## 📌 **BLOQUE II: Distribuciones Muestrales Empíricas**

### **Ejercicio 11.** Distribución Muestral de Latencias con Reposición
Una red local pequeña conecta tres servidores cuyas latencias de respuesta son exactamente: 10, 20 y 30 milisegundos. Se extraen todas las muestras posibles de tamaño 2 con reposición.
1. Construya el espacio muestral de las 9 muestras posibles y determine la media de cada una.
2. Obtenga la distribución de probabilidad de la media muestral.
3. Calcule la media y el error estándar de la distribución muestral y verifique formalmente su coincidencia con los parámetros de la población.

---

### **Ejercicio 12.** Demostración del Sesgo de la Varianza Ordinaria
Con la misma población de latencias $\{10, 20, 30\}$ y las 9 muestras de tamaño 2 obtenidas con reposición:
1. Calcule la varianza muestral ordinaria (con divisor $n$) para cada una de las 9 muestras.
2. Obtenga el promedio de dichas varianzas ordinarias y demuestre empíricamente que subestima a la varianza poblacional en una fracción de $(n-1)/n$.

---

### **Ejercicio 13.** Muestreo sin Reposición en Auditoría de Calidad
En un control de calidad sobre cuatro módulos de software, las calificaciones de estabilidad asignadas son: 12, 14, 16 y 18 puntos. Se extraen muestras aleatorias de tamaño 2 sin reposición.
1. Enumere las 6 combinaciones posibles de muestras y calcule la media de cada una.
2. Determine la media esperada y la varianza de la distribución de medias muestrales, comprobando la validez del factor de corrección por población finita.

---

### **Ejercicio 14.** Insesgadez de la Cuasivarianza sin Reposición
Tomando las 6 muestras sin reposición de tamaño 2 del ejercicio anterior sobre los módulos $\{12, 14, 16, 18\}$:
1. Calcule la varianza muestral corregida de cada muestra.
2. Demuestre que el promedio de dichas varianzas muestrales coincide exactamente con la cuasivarianza de la población.

---

### **Ejercicio 15.** Errores de Código en Módulos de Software
Una suite de software posee cuatro bibliotecas base con las siguientes cantidades de bugs registrados: 1, 3, 5 y 7 errores. Se consideran todas las muestras de tamaño 2 obtenidas con reposición.
1. Obtenga la media y la varianza de la población.
2. Calcule la media de la distribución muestral de la media y su error estándar teórico.

---

### **Ejercicio 16.** Consumo Eléctrico en Sensores de Telemetría
Tres microcontroladores de telemetría registran consumos de corriente de 5, 10 y 15 miliamperios. Se extraen dos mediciones al azar con reposición.
1. Construya la distribución de probabilidad de la media muestral.
2. Compare la dispersión de la media de las muestras con la dispersión individual de los sensores.

\newpage

---

## 📌 **BLOQUE III: Distribución Normal y Teorema Central del Límite**

### **Ejercicio 17.** Consumo de Memoria en Contenedores Docker
El consumo de memoria RAM de un tipo de microservicio contenedorizado sigue una distribución normal con media de 320 MB y desviación estándar de 45 MB.
1. ¿Cuál es la probabilidad de que un contenedor seleccionado al azar consuma entre 300 MB y 380 MB?
2. ¿Qué proporción de contenedores demandará más de 400 MB de memoria?

---

### **Ejercicio 18.** Transferencia de Datos en Enlaces de Fibra Óptica
La velocidad de transmisión en canales troncales de fibra óptica sigue una distribución normal con media de 950 Mbps y desviación estándar de 30 Mbps. Un ingeniero de infraestructura audita una muestra de 36 enlaces.
1. Determine la media esperada y el error estándar de la media muestral.
2. Calcule la probabilidad de que la velocidad promedio de la muestra supere los 960 Mbps.
3. Calcule la probabilidad de que la media se ubique entre 940 Mbps y 955 Mbps.

---

### **Ejercicio 19.** Capacidad de Procesamiento en Nube con Asimetría
La cantidad de peticiones por segundo recibidas por servidores de nube presenta una distribución marcadamente asimétrica con media de 1.200 peticiones por segundo y desviación estándar de 300 peticiones por segundo. Se audita una muestra de 64 servidores independientes.
1. Justifique la validez de utilizar la distribución normal para la media muestral.
2. Calcule la probabilidad de que el promedio de peticiones de la muestra se ubique entre 1.150 y 1.260 peticiones por segundo.

---

### **Ejercicio 20.** Latencia Crítica en Pasarelas de Pago
El tiempo de respuesta de un microservicio de pagos se distribuye normalmente con media de 85 milisegundos y desviación estándar de 18 milisegundos. La gerencia técnica desea establecer un umbral de alarma que delimite al 1% de las transacciones con peor rendimiento (las más lentas). Determine el tiempo de corte correspondiente.

---

### **Ejercicio 21.** Garantía de Durabilidad en Nodos de Sensores IoT
La vida útil de la batería en sensores inalámbricos instalados en campo sigue una distribución normal con media de 1.800 horas y desviación estándar de 120 horas. El fabricante planea ofrecer una garantía de reemplazo que cubra al 2.5% de los sensores con menor durabilidad. ¿Cuál es el tiempo de corte que debe fijarse para la garantía?

---

### **Ejercicio 22.** Despliegue Automatizado en Cluster de Servidores
En un cluster de 250 servidores, el tiempo necesario para desplegar una actualización de seguridad tiene una media de 42 segundos con una desviación estándar de 8 segundos. Si se selecciona una muestra aleatoria de 40 servidores sin reposición para una prueba piloto, calcule la probabilidad de que el tiempo promedio de despliegue se ubique entre 40 y 44 segundos.

---

### **Ejercicio 23.** Consumo de Tráfico en Streaming de Video
El ancho de banda consumido por usuarios de una plataforma de transmisión de video sigue una distribución normal con media de 4.8 GB por hora y desviación estándar de 0.9 GB por hora. Calcule los dos valores simétricos que delimitan al 90% central de los consumos individuales.

---

### **Ejercicio 24.** Confiabilidad en Discos de Estado Sólido (SSD)
La durabilidad de unidades de almacenamiento SSD para centros de datos sigue una distribución normal con media de 55.000 horas de uso y desviación estándar de 4.000 horas. Si se instala un rack con 100 unidades independientes, ¿cuál es la probabilidad de que la durabilidad promedio de las unidades del rack supere las 55.600 horas?

---

### **Ejercicio 25.** Velocidad de Reloj en Lote de Placas de Red
De una partida de 400 placas de red para servidores, se conoce que la frecuencia media es de 980 MHz con una desviación estándar de 25 MHz. Si se extrae una muestra de 50 placas sin reposición, determine la probabilidad de que la frecuencia promedio de la muestra se encuentre entre 975 MHz y 985 MHz.

---

### **Ejercicio 26.** Tiempo de Recuperación ante Desastres (RTO)
El tiempo de restauración de servicios informáticos tras una contingencia tiene una distribución con fuerte asimetría positiva, con media de 75 minutos y desviación estándar de 22 minutos. Si un equipo de contingencia analiza una muestra de 49 incidentes pasados, calcule la probabilidad de que el tiempo medio de recuperación de dicha muestra haya sido menor a 70 minutos.

\newpage

---

## 📌 **BLOQUE IV: Intervalos de Confianza para la Media Poblacional**

### **Ejercicio 27.** Tiempo de Compilación de Proyectos de Software
Un equipo de ingeniería de software mide el tiempo de compilación de un sistema en 18 ejecuciones independientes, obteniendo una media de 4.2 minutos con una desviación estándar de 0.8 minutos. Asumiendo que el tiempo de compilación se distribuye normalmente, construya un intervalo de confianza del 95% para el tiempo medio de compilación del sistema.

---

### **Ejercicio 28.** Calibración de Voltaje en Fuentes de Alimentación
Una muestra de 40 fuentes de poder industriales arroja un voltaje medio de salida de 12.04 voltios. Por calibraciones de diseño del fabricante se conoce que la desviación estándar de la población de fuentes es de 0.15 voltios.
1. Construya un intervalo de confianza del 90% para el voltaje medio poblacional.
2. Construya un intervalo de confianza del 98% para dicha media y compare la amplitud de ambos intervalos.

---

### **Ejercicio 29.** Calibración en Lote Finito de Fuentes
Recalcule el intervalo de confianza del 98% del ejercicio anterior si se conoce que las 40 fuentes fueron extraídas de un lote cerrado de 600 unidades producidas en el turno matutino.

---

### **Ejercicio 30.** Consumo Eléctrico en Racks de Servidores
El monitoreo energético sobre una muestra de 12 racks de servidores en un centro de cómputo arrojó un consumo medio de 3.8 kW con una varianza de 0.36 kW². Asumiendo una distribución normal del consumo eléctrico, estime el consumo medio poblacional mediante un intervalo de confianza del 99%.

---

### **Ejercicio 31.** Tiempo de Respuesta en Mesa de Ayuda
Una muestra aleatoria de 45 tickets de soporte técnico resueltos arrojó un tiempo promedio de atención de 16.5 minutos con una desviación típica de 3.5 minutos. Construya un intervalo de confianza del 90% para el tiempo medio de resolución de incidencias de todo el departamento.

---

### **Ejercicio 32.** Eficiencia de Compresión en Algoritmo de Datos
Un equipo de desarrollo diseña un nuevo algoritmo de compresión de imágenes. En una muestra de 50 archivos de prueba, se obtiene un porcentaje medio de reducción de tamaño del 68% con una desviación estándar del 4.2%. Construya un intervalo de confianza del 95% para el porcentaje medio poblacional de compresión.

---

### **Ejercicio 33.** Temperatura de Operación en Microprocesadores
Por ensayos históricos de laboratorio se conoce que la desviación estándar de la temperatura de operación en microprocesadores bajo carga máxima es de 3.5 °C. En una muestra de auditoría de 35 microprocesadores de una nueva línea, se constata una temperatura media de 72.4 °C.
1. Halle el intervalo de confianza del 95% para la temperatura media poblacional.
2. Halle el intervalo de confianza del 99%.

---

### **Ejercicio 34.** Comparación de Latencias: HTTP/2 vs. HTTP/3
Se evalúa la latencia de respuesta (en milisegundos) de dos protocolos de transferencia web sobre dos muestras de 8 solicitudes cada una, arrojando los siguientes datos:
- Protocolo A (HTTP/2): 42, 45, 39, 44, 41, 46, 40, 43
- Protocolo B (HTTP/3): 31, 35, 29, 33, 30, 34, 32, 28
Bajo el supuesto de normalidad en ambos protocolos, determine el margen de error y el intervalo de confianza del 95% para la latencia media de cada uno.

---

### **Ejercicio 35.** Longitud de Pistas en Placas de Circuito Impreso (PCB)
Una muestra de 14 placas electrónicas extraída de una línea de fotograbado reporta una longitud media de pistas críticas de 28.5 mm con una desviación estándar de 1.2 mm. Suponiendo una distribución normal de las dimensiones, construya un intervalo de confianza del 95% para la longitud media poblacional.

---

### **Ejercicio 36.** Tiempo de Consulta en Base de Datos (Datos Directos)
Se mide el tiempo de respuesta (en segundos) en 9 ejecuciones de una consulta compleja a un almacén de datos (data warehouse), obteniéndose los siguientes registros:
$$
52, \; 48, \; 55, \; 50, \; 49,
$$
$$
53, \; 47, \; 51, \; 54
$$
Asumiendo distribución normal, construya un intervalo de confianza del 99% para el tiempo medio de respuesta de dicha consulta.

\newpage

---

## 📌 **BLOQUE V: Población Finita y Tamaño Óptimo de Muestra**

### **Ejercicio 37.** Sensores Térmicos en Reactores Químicos
Se instalan sensores para monitorear un reactor continuo. Por especificaciones del proveedor se conoce que la desviación estándar de la temperatura medida es de 1.8 °C y los registros siguen una distribución normal. Una muestra de 60 sensores arroja una temperatura media de 145.2 °C. Construya un intervalo de confianza del 95% para la temperatura media real.

---

### **Ejercicio 38.** Autonomía de Baterías en Flota de Drones
De una partida de 800 baterías de polímero de litio, una muestra aleatoria de 45 baterías arroja una autonomía media de vuelo de 38.5 minutos con una desviación estándar de 3.2 minutos.
1. Construya el intervalo de confianza del 95% asumiendo población infinita.
2. Construya el intervalo del 95% considerando el tamaño finito del lote y compare ambos márgenes de error.

---

### **Ejercicio 39.** Determinación de Muestra para Autonomía de Drones
Utilizando los datos de variabilidad del ejercicio anterior (desviación estándar de 3.2 minutos), ¿de qué tamaño debe ser la muestra si se desea tener un 95% de confianza de que la media muestral no difiera de la media real de la población en más de 0.8 minutos?

---

### **Ejercicio 40.** Reducción del Margen de Error en Tiempos de Llamada
En un centro de soporte técnico telefónico, una muestra de 50 llamadas arrojó una duración media de 180 segundos. Por registros globales históricos se conoce que la desviación estándar es de 30 segundos.
1. Calcule el margen de error y construya el intervalo de confianza del 95%.
2. Si se desea mantener el 95% de confianza pero reduciendo el error máximo admisible a 5 segundos, ¿cuántas llamadas deben auditarse?

---

### **Ejercicio 41.** Encuesta Salarial en Administración de Bases de Datos
Un relevamiento salarial busca estimar el ingreso mensual promedio de los administradores de bases de datos (DBA) en la región. Un estudio gremial previo señala que la desviación estándar de los ingresos es de \$15.000. Se desea que el error de estimación no exceda los \$2.500.
1. ¿Cuál es el tamaño muestral requerido para un 95% de confianza?
2. Si se exige elevar la confianza al 99%, ¿a cuánto debe incrementarse el tamaño de la muestra?

---

### **Ejercicio 42.** Auditoría de Facturación con Confianza del 96%
Se audita la facturación mensual por usuario en una plataforma SaaS. Se conoce una desviación estándar de \$8.000. Calcule el tamaño de muestra necesario si se desea garantizar un error de estimación no mayor a \$1.200 con un nivel de confianza del 96%.

\newpage

---

## 📌 **BLOQUE VI: Muestras Especiales y Control de Especificaciones**

### **Ejercicio 43.** Atenuación de Señal en Cables de Red de Alta Velocidad
Una empresa fabrica cables de red cuya atenuación de señal presenta una desviación estándar de 4.5 dB. De un lote de producción diaria compuesto por 200 cables, se extrae una muestra de 35 cables que arroja una atenuación media de 18.2 dB. Construya un intervalo de confianza del 98% para la atenuación media de los cables producidos ese día.

---

### **Ejercicio 44.** Detección de Incidentes Semanales en Cortafuegos
El número semanal de alertas de intrusión bloqueadas por un firewall perimetral sigue una distribución normal con media desconocida. En una muestra de 12 semanas se registraron las siguientes cantidades de incidentes:
$$
8, \; 12, \; 10, \; 14, \; 9, \; 11,
$$
$$
13, \; 10, \; 8, \; 15, \; 11, \; 9
$$
Obtenga un intervalo de confianza para la media de incidentes semanales con un nivel de significación del 1%.

---

### **Ejercicio 45.** Tarifas de Suscripción en Clientes Corporativos
Una empresa proveedora de software en la nube administra una cartera de 400 clientes corporativos. Una muestra aleatoria de 35 clientes revela una tarifa media mensual de \$4.200 con una desviación estándar de \$650. Suponiendo normalidad, determine el intervalo de confianza del 95% para la tarifa media de la cartera de clientes.

---

### **Ejercicio 46.** Resistencia Térmica en Conmutadores de Red Industriales
Una empresa de telecomunicaciones requiere que los conmutadores (switches) instalados en plantas industriales soporten temperaturas de operación de al menos 65 °C sin fallar. Se ensayan 4 unidades prototipo en una cámara climática, constatándose que operan en promedio hasta 61.5 °C con una desviación estándar de 1.5 °C. Asumiendo distribución normal y un nivel de riesgo del 5%:
1. Construya el intervalo de confianza y dictamine si el modelo ensayado cumple con la especificación de 65 °C.
2. Recalcule el intervalo si las 4 unidades provienen de una partida piloto limitada de 25 unidades.

\newpage

---

## 📌 **BLOQUE VII: Intervalos para la Varianza y Desviación Estándar**

### **Ejercicio 47.** Uniformidad en Envasado de Aceite Dieléctrico
Para controlar el proceso automatizado de llenado de envases de aceite dieléctrico para transformadores, se extrae una muestra de 18 envases, arrojando una varianza de 0.32 litros². Asumiendo que el volumen de llenado se distribuye normalmente, obtenga un intervalo de confianza del 95% para la varianza poblacional de todo el proceso.

---

### **Ejercicio 48.** Variabilidad en Componentes Aeronáuticos
En una muestra de 25 piezas de titanio fabricadas para turbinas de aviación, la desviación estándar del peso fue de 18 gramos. Bajo el supuesto de distribución normal:
1. Halle el intervalo de confianza del 95% para la desviación estándar de la producción total.
2. Halle el intervalo de confianza del 99% para dicha desviación estándar.

---

### **Ejercicio 49.** Resistencia a la Tracción en Compuestos de Carbono
Se ensaya la tensión de ruptura en 7 probetas de un material compuesto de fibra de carbono para estructuras aeroespaciales, obteniéndose las siguientes cargas máximas (en MPa):
$$
410, \; 418, \; 405, \; 422,
$$
$$
415, \; 412, \; 408
$$
Asumiendo normalidad, construya un intervalo de confianza del 95% para la varianza poblacional de la resistencia del material.

---

### **Ejercicio 50.** Variabilidad en Tiempos de Transacción Criptográfica
En una red descentralizada de procesamiento de transacciones, una muestra de 16 nodos reporta una desviación estándar en el tiempo de validación de bloques de 45 milisegundos. Suponiendo que el tiempo de validación se distribuye normalmente:
1. Construya el intervalo de confianza del 90% para la desviación estándar poblacional de los tiempos de validación.
2. Construya el intervalo de confianza del 98% para dicha desviación estándar.

\newpage

---
---

# 🗝️ **SOLUCIONARIO INTEGRAL PASO A PASO (EJERCICIOS 1 AL 50)**


## 📌 **SOLUCIONARIO: BLOQUE I (EJERCICIOS 1 AL 10)**
### **Fundamentos Teóricos, Muestreo y Propiedades de Estimadores**

---

### **Solución del Ejercicio 1**
#### **1. Extracción e Interpretación de Variables**
- Variable estandarizada original: $Z \sim N(0, \; 1)$, donde por definición:
  $$
  E[Z] = 0, \quad \text{Var}(Z) = 1
  $$
- Variable auxiliar definida por transformación lineal:
  $$
  W = a \cdot Z + b \quad \text{con } a = 3, \; b = 5
  $$

#### **2. Elección del Modelo y Propiedades Matemáticas**
Se aplican las propiedades formales de la esperanza y la varianza para transformaciones lineales de variables aleatorias:
1. Linealidad de la esperanza: $E[aZ + b] = a E[Z] + b$.
2. Varianza de una combinación lineal: $\text{Var}(aZ + b) = a^2 \text{Var}(Z)$.

#### **3. Desarrollo Matemático y Operaciones**
1. **Cálculo de la media esperada de $W$:**
   $$
   E[W] = E[3Z + 5]
   $$
   $$
   E[W] = 3 \cdot E[Z] + 5
   $$
   $$
   E[W] = 3 \cdot (0) + 5 = \mathbf{5}
   $$

2. **Cálculo de la varianza de $W$:**
   $$
   \text{Var}(W) = \text{Var}(3Z + 5)
   $$
   $$
   \text{Var}(W) = 3^2 \cdot \text{Var}(Z)
   $$
   $$
   \text{Var}(W) = 9 \cdot (1) = \mathbf{9}
   $$
   $$
   \sigma_W = \sqrt{9} = \mathbf{3}
   $$

#### **4. Conclusión e Interpretación Técnica**
Toda transformación lineal de una variable normal genera otra variable normal. La variable resultante se distribuye como $W \sim N(\mu_W = 5, \; \sigma_W^2 = 9)$. Al multiplicar por la constante $3$, la dispersión se triplica y la varianza se multiplica por $3^2 = 9$; al sumar la constante $5$, el centro de gravedad de la distribución se traslada en $5$ unidades sin alterar la varianza.

---

### **Solución del Ejercicio 2**
#### **1. Extracción e Interpretación de Variables**
- Estimador propuesto: $T = \frac{\sum (X_i - \bar{X})^2}{n + 1}$.
- Suma de cuadrados de desvíos: $\sum_{i=1}^n (X_i - \bar{X})^2 = (n - 1) \cdot S^2$, donde $S^2$ es la cuasivarianza muestral insesgada.
- Parámetro poblacional a estimar: $\sigma^2$ (varianza poblacional).

#### **2. Elección del Modelo y Propiedades Matemáticas**
Un estimador $\hat{\theta}$ es insesgado si $E[\hat{\theta}] = \theta$. En caso contrario, el sesgo se define como:
$$
\text{Sesgo}(\hat{\theta}) = E[\hat{\theta}] - \theta
$$
Sabiendo que $E\left[\sum (X_i - \bar{X})^2\right] = (n - 1)\sigma^2$, evaluamos el valor esperado del estimador $T$.

#### **3. Desarrollo Matemático y Operaciones**
1. **Valor esperado de $T$:**
   $$
   E[T] = E\left[ \frac{\sum (X_i - \bar{X})^2}{n + 1} \right]
   $$
   $$
   E[T] = \frac{1}{n + 1} \cdot E\left[\sum (X_i - \bar{X})^2\right]
   $$
   $$
   E[T] = \frac{n - 1}{n + 1} \cdot \sigma^2
   $$

2. **Determinación y magnitud del sesgo:**
   $$
   \text{Sesgo}(T) = E[T] - \sigma^2
   $$
   $$
   \text{Sesgo}(T) = \left( \frac{n - 1}{n + 1} - 1 \right) \cdot \sigma^2
   $$
   $$
   \text{Sesgo}(T) = \left( \frac{n - 1 - (n + 1)}{n + 1} \right) \sigma^2
   $$
   $$
   \text{Sesgo}(T) = -\frac{2}{n + 1} \cdot \sigma^2
   $$

#### **4. Conclusión e Interpretación Técnica**
El estimador $T$ es **sesgado** porque su valor esperado no coincide con el parámetro $\sigma^2$. Dado que el sesgo es negativo ($-\frac{2}{n+1} \sigma^2$), el estimador **subestima sistemáticamente** a la varianza poblacional. A medida que el tamaño muestral crece ($n \to \infty$), el sesgo tiende a $0$, lo que convierte a $T$ en un estimador asintóticamente insesgado.

---

### **Solución del Ejercicio 3**
#### **1. Extracción e Interpretación de Conceptos**
- **Error Muestral:** Discrepancia intrínseca entre el estadístico muestral y el verdadero parámetro poblacional, producida exclusivamente por la aleatoriedad de observar un subconjunto de la población en vez de la totalidad. Es inevitable, pero cuantificable mediante el error estándar.
- **Error No Muestral:** Sesgos, distorsiones o equivocaciones introducidas en el diseño, recolección, medición o procesamiento de los datos. No disminuyen necesariamente al aumentar el tamaño de muestra y pueden invalidar los resultados.

#### **2. Clasificación Justificada de los Casos**
1. **Encuesta voluntaria en línea con 4% de respuesta:**
   - **Clasificación:** **Error No Muestral (Sesgo de No Respuesta y Autoselección).**
   - **Justificación:** Los usuarios que responden voluntariamente tienen motivaciones extremas (usualmente disconformidad), por lo que la muestra no representa a la población general de usuarios.
2. **Diferencia de 2 ms en muestra de 50 servidores:**
   - **Clasificación:** **Error Muestral.**
   - **Justificación:** Proviene de la fluctuación aleatoria inherente a la selección probabilística de un subconjunto de servidores.
3. **Sensor térmico descalibrado (+1.5 °C sistemático):**
   - **Clasificación:** **Error No Muestral (Error de Medición / Instrumental).**
   - **Justificación:** Es una distorsión sistemática en el instrumento físico de medición que afecta a todas las observaciones por igual.

---

### **Solución del Ejercicio 4**
#### **1. Extracción e Interpretación de Variables**
- Tamaño total de la población: $N = 1.200$.
- Tamaño de la muestra requerida: $n = 100$.
- Estratos poblacionales:
  - Sede Central: $N_1 = 600$ empleados.
  - Sede Norte: $N_2 = 360$ empleados.
  - Sede Sur: $N_3 = 240$ empleados.

#### **2. Elección del Modelo y Fórmulas**
En la **afijación proporcional**, el tamaño de muestra de cada estrato $h$ respeta la proporción que representa dicho estrato en la población total:
$$
w_h = \frac{N_h}{N}, \quad n_h = n \cdot w_h = n \cdot \frac{N_h}{N}
$$

#### **3. Desarrollo Matemático y Operaciones**
1. **Cálculo de pesos de cada estrato:**
   $$
   w_1 = \frac{600}{1.200} = 0.50 \quad (50\%)
   $$
   $$
   w_2 = \frac{360}{1.200} = 0.30 \quad (30\%)
   $$
   $$
   w_3 = \frac{240}{1.200} = 0.20 \quad (20\%)
   $$

2. **Asignación muestral por sede:**
   $$
   n_1 = 100 \cdot 0.50 = \mathbf{50\text{ empleados (Central)}}
   $$
   $$
   n_2 = 100 \cdot 0.30 = \mathbf{30\text{ empleados (Norte)}}
   $$
   $$
   n_3 = 100 \cdot 0.20 = \mathbf{20\text{ empleados (Sur)}}
   $$
   $$
   \sum n_h = 50 + 30 + 20 = 100
   $$

#### **4. Conclusión e Interpretación Técnica**
El muestreo estratificado es estrictamente más eficiente que el muestreo aleatorio simple cuando los estratos son **internamente homogéneos y mutuamente heterogéneos**. Al estratificar por sede, se elimina la varianza existente *entre* las distintas sedes del error de estimación global, reduciendo la varianza del estimador muestral.

---

### **Solución del Ejercicio 5**
#### **1. Concepto de Muestreo Bietápico por Conglomerados**
En el muestreo por conglomerados en dos etapas:
- **Etapa 1:** La población se divide en grupos naturales heterogéneos llamados conglomerados. Se selecciona aleatoriamente una muestra de dichos conglomerados (unidades primarias).
- **Etapa 2:** Dentro de cada conglomerado seleccionado, no se censan todos los elementos, sino que se extrae una submuestra aleatoria de elementos finales (unidades secundarias).

#### **2. Comparación Estructural: Conglomerados vs. Estratos**
| Criterio | Muestreo Estratificado | Muestreo por Conglomerados |
| :--- | :--- | :--- |
| **Composición Interna** | Homogénea (elementos muy parecidos) | Heterogénea (microcosmos de la población) |
| **Diferencias entre Grupos** | Heterogéneos (muy distintos entre sí) | Homogéneos (conglomerados similares) |
| **Selección de Grupos** | Se incluyen **todos** los estratos | Se selecciona una **muestra** de conglomerados |
| **Objetivo Principal** | Aumentar precisión analítica | Reducir costos logísticos de relevamiento |

#### **3. Caso Práctico en Red Bancaria (80 Sucursales)**
- **Etapa 1:** Se sortean aleatoriamente $10$ sucursales de las $80$ existentes en el país.
- **Etapa 2:** En cada una de esas $10$ sucursales, los auditores toman una muestra aleatoria de $25$ terminales de caja o transacciones para inspección profunda.

---

### **Solución del Ejercicio 6**
#### **1. Extracción e Interpretación de Variables**
- Muestra de tamaño $n = 3$ de variables $X_1, X_2, X_3$ independientes e idénticamente distribuidas con varianza $\text{Var}(X_i) = \sigma^2$.
- Estimadores propuestos para la media:
  $$
  \bar{X} = \frac{1}{3}X_1 + \frac{1}{3}X_2 + \frac{1}{3}X_3
  $$
  $$
  T_1 = \frac{1}{2}X_1 + \frac{1}{4}X_2 + \frac{1}{4}X_3
  $$

#### **2. Elección del Modelo y Criterio de Eficiencia**
Entre estimadores insesgados, el estimador más eficiente es aquel que posee **menor varianza**. Aplicamos la propiedad de la varianza de combinaciones lineales independientes:
$$
\text{Var}\left(\sum c_i X_i\right) = \sum c_i^2 \text{Var}(X_i) = \sigma^2 \sum c_i^2
$$

#### **3. Desarrollo Matemático y Operaciones**
1. **Varianza de la media muestral $\bar{X}$:**
   $$
   \text{Var}(\bar{X}) = \left[\left(\frac{1}{3}\right)^2 + \left(\frac{1}{3}\right)^2 + \left(\frac{1}{3}\right)^2\right] \sigma^2
   $$
   $$
   \text{Var}(\bar{X}) = \left(\frac{1}{9} + \frac{1}{9} + \frac{1}{9}\right) \sigma^2
   $$
   $$
   \text{Var}(\bar{X}) = \frac{3}{9} \sigma^2 = \frac{1}{3} \sigma^2 \approx \mathbf{0.3333 \, \sigma^2}
   $$

2. **Varianza del estimador ponderado $T_1$:**
   $$
   \text{Var}(T_1) = \left[\left(\frac{1}{2}\right)^2 + \left(\frac{1}{4}\right)^2 + \left(\frac{1}{4}\right)^2\right] \sigma^2
   $$
   $$
   \text{Var}(T_1) = \left(\frac{1}{4} + \frac{1}{16} + \frac{1}{16}\right) \sigma^2
   $$
   $$
   \text{Var}(T_1) = \left(\frac{4 + 1 + 1}{16}\right) \sigma^2 = \frac{6}{16} \sigma^2
   $$
   $$
   \text{Var}(T_1) = \frac{3}{8} \sigma^2 = \mathbf{0.3750 \, \sigma^2}
   $$

3. **Comparación directa de varianzas:**
   $$
   \text{Var}(\bar{X}) = \frac{8}{24} \sigma^2 < \text{Var}(T_1) = \frac{9}{24} \sigma^2
   $$

#### **4. Conclusión e Interpretación Técnica**
La media muestral $\bar{X}$ es **más eficiente** que $T_1$ porque posee menor varianza ($0.3333\,\sigma^2$ frente a $0.3750\,\sigma^2$). Asignar pesos iguales ($\frac{1}{n}$) minimiza la suma de cuadrados de coeficientes, cumpliendo el teorema de Gauss-Markov.

---

### **Solución del Ejercicio 7**
#### **1. Definición Formal de Consistencia**
Un estimador $\hat{\theta}_n$ es **consistente** para un parámetro $\theta$ si converge en probabilidad a $\theta$ cuando el tamaño muestral tiende a infinito:
$$
\lim_{n \to \infty} P\left(|\hat{\theta}_n - \theta| < \varepsilon\right) = 1, \quad \forall \, \varepsilon > 0
$$

#### **2. Condición Suficiente de Consistencia**
Un estimador es cuadráticamente consistente si cumple simultáneamente:
1. Asintóticamente insesgado: $\lim_{n \to \infty} E[\hat{\theta}_n] = \theta$.
2. Varianza asintótica nula: $\lim_{n \to \infty} \text{Var}(\hat{\theta}_n) = 0$.

#### **3. Relación con la Ley Débil de los Grandes Números**
La Ley Débil de los Grandes Números (teorema de Khinchin) garantiza que si una muestra proviene de observaciones independientes con media finita $\mu$, la media muestral $\bar{X}_n$ converge en probabilidad a $\mu$:
$$
\bar{X}_n \xrightarrow{P} \mu \quad \text{cuando } n \to \infty
$$
Esto confirma que la media muestral $\bar{X}$ es siempre un estimador consistente de la media poblacional $\mu$.

---

### **Solución del Ejercicio 8**
#### **1. Extracción e Interpretación de Variables**
- Muestra aleatoria de $n$ variables independientes $X_1, X_2, \dots, X_n$.
- Parámetros individuales: $E[X_i] = \mu$ y $\text{Var}(X_i) = \sigma^2$.
- Suma muestral total: $T_n = \sum_{i=1}^n X_i$.

#### **2. Propiedades Matemáticas de la Suma Muestral**
1. **Media esperada:**
   $$
   E[T_n] = E\left[\sum_{i=1}^n X_i\right] = \sum_{i=1}^n E[X_i] = \mathbf{n \cdot \mu}
   $$
2. **Varianza de la suma (por independencia):**
   $$
   \text{Var}(T_n) = \text{Var}\left(\sum_{i=1}^n X_i\right) = \sum_{i=1}^n \text{Var}(X_i) = \mathbf{n \cdot \sigma^2}
   $$
   $$
   \sigma_{T_n} = \sigma \sqrt{n}
   $$

#### **3. Teorema Central del Límite para la Suma**
Cuando $n \ge 30$, la distribución de la suma total $T_n$ converge asintóticamente hacia una distribución normal:
$$
T_n \approx N\left(n \mu, \; n \sigma^2\right)
$$
Variable estandarizada correspondiente:
$$
Z = \frac{T_n - n\mu}{\sigma \sqrt{n}} \sim N(0, \; 1)
$$

---

### **Solución del Ejercicio 9**
#### **1. Concepto de Grados de Libertad**
Los **grados de libertad** representan el número de observaciones independientes que quedan libres para variar en un cálculo estadístico después de haber fijado ciertas restricciones algebraicas o estimaciones preliminares sobre los datos.

#### **2. Fundamentación en la Varianza Muestral**
La fórmula de la varianza muestral es:
$$
S^2 = \frac{\sum_{i=1}^n (X_i - \bar{X})^2}{n - 1}
$$
Para calcular los desvíos $(X_i - \bar{X})$, es obligatorio calcular previamente la media muestral $\bar{X}$. Por propiedad de la media aritmética, la suma algebraica de los desvíos es idénticamente nula:
$$
\sum_{i=1}^n (X_i - \bar{X}) = 0
$$
Esta relación impone una restricción lineal: conocidos los primeros $n-1$ desvíos, el último queda automáticamente determinado:
$$
(X_n - \bar{X}) = -\sum_{i=1}^{n-1} (X_i - \bar{X})
$$
Por lo tanto, solo $n - 1$ sumandos son libres e independientes, perdiendo $1$ grado de libertad. Dividir por $n-1$ es indispensable para compensar este vínculo y garantizar que $S^2$ sea insesgado.

---

### **Solución del Ejercicio 10**
#### **1. Parámetros de la Distribución Chi-Cuadrado ($\chi^2_k$)**
Para una variable $Y \sim \chi^2_k$ con $k$ grados de libertad:
- **Esperanza matemática:**
  $$
  E[Y] = \mathbf{k}
  $$
- **Varianza:**
  $$
  \text{Var}(Y) = \mathbf{2k}
  $$
- **Desviación estándar:**
  $$
  \sigma_Y = \sqrt{2k}
  $$

#### **2. Propiedad Reproductiva o Aditiva**
Si $Y_1, Y_2, \dots, Y_m$ son variables aleatorias mutuamente independientes, tales que cada una sigue una distribución Chi-Cuadrado:
$$
Y_j \sim \chi^2_{k_j} \quad \text{para } j = 1, 2, \dots, m
$$
Entonces la suma de dichas variables sigue una distribución Chi-Cuadrado cuyos grados de libertad son la suma directa de los grados de libertad individuales:
$$
U = \sum_{j=1}^m Y_j \sim \chi^2_{\left(\sum_{j=1}^m k_j\right)}
$$

\newpage

---

## 📌 **SOLUCIONARIO: BLOQUE II (EJERCICIOS 11 AL 16)**
### **Distribuciones Muestrales Empíricas y Verificación de Insesgadez**

---

### **Solución del Ejercicio 11**
#### **1. Extracción e Interpretación de Variables**
- Población finita de servidores: $N = 3$, con latencias $\{10, \; 20, \; 30\}$ ms.
- Muestreo con reposición de tamaño $n = 2$.
- Cantidad de muestras posibles: $N^n = 3^2 = 9$ muestras equiprobables ($P = \frac{1}{9}$ cada una).

#### **2. Parámetros Poblacionales**
$$
\mu = \frac{10 + 20 + 30}{3} = \frac{60}{3} = \mathbf{20\text{ ms}}
$$
$$
\sigma^2 = \frac{(10-20)^2 + (20-20)^2 + (30-20)^2}{3} = \frac{100 + 0 + 100}{3} = \mathbf{\frac{200}{3}} \approx 66.67\text{ ms}^2
$$

#### **3. Espacio Muestral y Distribución de la Media**
Las 9 muestras y sus medias $\bar{x} = \frac{x_1 + x_2}{2}$ son:
1. $(10, 10) \implies \bar{x} = 10$
2. $(10, 20) \implies \bar{x} = 15$
3. $(10, 30) \implies \bar{x} = 20$
4. $(20, 10) \implies \bar{x} = 15$
5. $(20, 20) \implies \bar{x} = 20$
6. $(20, 30) \implies \bar{x} = 25$
7. $(30, 10) \implies \bar{x} = 20$
8. $(30, 20) \implies \bar{x} = 25$
9. $(30, 30) \implies \bar{x} = 30$

**Distribución de probabilidad de $\bar{X}$:**
| $\bar{x}$ (ms) | Frecuencia | $P(\bar{X} = \bar{x})$ | $\bar{x} \cdot P$ | $(\bar{x} - \mu)^2 \cdot P$ |
| :---: | :---: | :---: | :---: | :---: |
| **10** | 1 | $1/9$ | $10/9$ | $(10-20)^2 \cdot \frac{1}{9} = \frac{100}{9}$ |
| **15** | 2 | $2/9$ | $30/9$ | $(15-20)^2 \cdot \frac{2}{9} = \frac{50}{9}$ |
| **20** | 3 | $3/9$ | $60/9$ | $(20-20)^2 \cdot \frac{3}{9} = 0$ |
| **25** | 2 | $2/9$ | $50/9$ | $(25-20)^2 \cdot \frac{2}{9} = \frac{50}{9}$ |
| **30** | 1 | $1/9$ | $30/9$ | $(30-20)^2 \cdot \frac{1}{9} = \frac{100}{9}$ |
| **Total** | **9** | **1.00** | **$180/9 = 20$** | **$300/9 = 100/3$** |

#### **4. Verificación de Insesgadez y Error Estándar**
1. **Media de la distribución muestral:**
   $$
   \mu_{\bar{X}} = E[\bar{X}] = \sum \bar{x} P = \mathbf{20\text{ ms}} = \mu
   $$
2. **Varianza y error estándar:**
   $$
   \sigma^2_{\bar{X}} = \frac{300}{9} = \mathbf{\frac{100}{3}} \approx 33.33\text{ ms}^2
   $$
   $$
   \sigma_{\text{teórico}}^2 = \frac{\sigma^2}{n} = \frac{200/3}{2} = \mathbf{\frac{100}{3}} \approx 33.33\text{ ms}^2
   $$
   $$
   \sigma_{\bar{X}} = \sqrt{\frac{100}{3}} = \frac{10}{\sqrt{3}} \approx \mathbf{5.77\text{ ms}}
   $$
La media muestral es exactamente insesgada ($E[\bar{X}] = \mu$) y su varianza coincide con el modelo teórico.

---

### **Solución del Ejercicio 12**
#### **1. Extracción e Interpretación de Variables**
- Población: $\{10, \; 20, \; 30\}$, con $\sigma^2 = \frac{200}{3} \approx 66.67$.
- Se evalúa la varianza ordinaria muestral (con divisor $n = 2$):
  $$
  s^2_{\text{ord}} = \frac{\sum_{i=1}^2 (x_i - \bar{x})^2}{2}
  $$

#### **2. Cálculo de $s^2_{\text{ord}}$ para las 9 Muestras**
1. $(10, 10): \bar{x} = 10 \implies s^2_{\text{ord}} = \frac{0^2 + 0^2}{2} = 0$
2. $(10, 20): \bar{x} = 15 \implies s^2_{\text{ord}} = \frac{(-5)^2 + 5^2}{2} = \frac{50}{2} = 25$
3. $(10, 30): \bar{x} = 20 \implies s^2_{\text{ord}} = \frac{(-10)^2 + 10^2}{2} = \frac{200}{2} = 100$
4. $(20, 10): \bar{x} = 15 \implies s^2_{\text{ord}} = 25$
5. $(20, 20): \bar{x} = 20 \implies s^2_{\text{ord}} = 0$
6. $(20, 30): \bar{x} = 25 \implies s^2_{\text{ord}} = 25$
7. $(30, 10): \bar{x} = 20 \implies s^2_{\text{ord}} = 100$
8. $(30, 20): \bar{x} = 25 \implies s^2_{\text{ord}} = 25$
9. $(30, 30): \bar{x} = 30 \implies s^2_{\text{ord}} = 0$

#### **3. Promedio Empírico y Comprobación del Sesgo**
$$
E[s^2_{\text{ord}}] = \frac{0 + 25 + 100 + 25 + 0 + 25 + 100 + 25 + 0}{9}
$$
$$
E[s^2_{\text{ord}}] = \frac{300}{9} = \mathbf{\frac{100}{3}} \approx 33.33
$$
Comparación con la varianza poblacional:
$$
\frac{n - 1}{n} \cdot \sigma^2 = \frac{2 - 1}{2} \cdot \frac{200}{3} = \frac{1}{2} \cdot \frac{200}{3} = \mathbf{\frac{100}{3}}
$$

#### **4. Conclusión e Interpretación Técnica**
Queda demostrado empíricamente que la varianza con divisor $n$ es **sesgada**, pues subestima a la varianza poblacional:
$$
E[s^2_{\text{ord}}] = \frac{n-1}{n} \sigma^2 = \frac{1}{2} \sigma^2
$$
Para eliminar este sesgo del 50%, es necesario utilizar el divisor $n - 1 = 1$, dando lugar a la cuasivarianza.

---

### **Solución del Ejercicio 13**
#### **1. Extracción e Interpretación de Variables**
- Población: $N = 4$ módulos de software con estabilidad $\{12, \; 14, \; 16, \; 18\}$ puntos.
- Muestreo sin reposición de tamaño $n = 2$.
- Número de muestras posibles: $\binom{4}{2} = \frac{4 \cdot 3}{2} = 6$ muestras equiprobables ($P = \frac{1}{6}$).

#### **2. Parámetros de la Población**
$$
\mu = \frac{12 + 14 + 16 + 18}{4} = \frac{60}{4} = \mathbf{15}
$$
$$
\sigma^2 = \frac{(12-15)^2 + (14-15)^2 + (16-15)^2 + (18-15)^2}{4} = \frac{9 + 1 + 1 + 9}{4} = \frac{20}{4} = \mathbf{5}
$$

#### **3. Las 6 Muestras y sus Medias**
1. $\{12, 14\} \implies \bar{x} = \frac{12+14}{2} = 13$
2. $\{12, 16\} \implies \bar{x} = \frac{12+16}{2} = 14$
3. $\{12, 18\} \implies \bar{x} = \frac{12+18}{2} = 15$
4. $\{14, 16\} \implies \bar{x} = \frac{14+16}{2} = 15$
5. $\{14, 18\} \implies \bar{x} = \frac{14+18}{2} = 16$
6. $\{16, 18\} \implies \bar{x} = \frac{16+18}{2} = 17$

#### **4. Verificación del Factor de Corrección por Población Finita (CPF)**
1. **Media esperada:**
   $$
   E[\bar{X}] = \frac{13 + 14 + 15 + 15 + 16 + 17}{6} = \frac{90}{6} = \mathbf{15} = \mu
   $$
2. **Varianza empírica:**
   $$
   \sigma^2_{\bar{X}} = \frac{(13-15)^2 + (14-15)^2 + 0 + 0 + (16-15)^2 + (17-15)^2}{6}
   $$
   $$
   \sigma^2_{\bar{X}} = \frac{4 + 1 + 0 + 0 + 1 + 4}{6} = \frac{10}{6} = \mathbf{\frac{5}{3}} \approx 1.67
   $$
3. **Fórmula teórica con CPF:**
   $$
   \sigma^2_{\bar{X}} = \frac{\sigma^2}{n} \cdot \left(\frac{N - n}{N - 1}\right)
   $$
   $$
   \sigma^2_{\bar{X}} = \frac{5}{2} \cdot \left(\frac{4 - 2}{4 - 1}\right) = \frac{5}{2} \cdot \frac{2}{3} = \mathbf{\frac{5}{3}} \approx 1.67
   $$
El factor de corrección por población finita $\frac{2}{3}$ reproduce exactamente la reducción de dispersión al no reponer elementos.

---

### **Solución del Ejercicio 14**
#### **1. Extracción e Interpretación de Variables**
- Población: $\{12, \; 14, \; 16, \; 18\}$, $N = 4$.
- Cuasivarianza poblacional:
  $$
  S^2_{\text{pob}} = \frac{\sum (X_i - \mu)^2}{N - 1} = \frac{20}{4 - 1} = \mathbf{\frac{20}{3}} \approx 6.67
  $$
- Evaluamos la varianza corregida $S^2 = \frac{\sum (x_i - \bar{x})^2}{n - 1}$ en cada una de las 6 muestras sin reposición ($n - 1 = 1$).

#### **2. Cálculo de $S^2$ para las 6 Muestras**
1. $\{12, 14\}: \bar{x} = 13 \implies S^2 = \frac{(12-13)^2 + (14-13)^2}{1} = 1 + 1 = 2$
2. $\{12, 16\}: \bar{x} = 14 \implies S^2 = \frac{(12-14)^2 + (16-14)^2}{1} = 4 + 4 = 8$
3. $\{12, 18\}: \bar{x} = 15 \implies S^2 = \frac{(12-15)^2 + (18-15)^2}{1} = 9 + 9 = 18$
4. $\{14, 16\}: \bar{x} = 15 \implies S^2 = \frac{(14-15)^2 + (16-15)^2}{1} = 1 + 1 = 2$
5. $\{14, 18\}: \bar{x} = 16 \implies S^2 = \frac{(14-16)^2 + (18-16)^2}{1} = 4 + 4 = 8$
6. $\{16, 18\}: \bar{x} = 17 \implies S^2 = \frac{(16-17)^2 + (18-17)^2}{1} = 1 + 1 = 2$

#### **3. Promedio de las Varianzas Muestrales y Conclusión**
$$
E[S^2] = \frac{2 + 8 + 18 + 2 + 8 + 2}{6} = \frac{40}{6} = \mathbf{\frac{20}{3}} \approx 6.67
$$
$$
E[S^2] = S^2_{\text{pob}}
$$
La cuasivarianza muestral $S^2$ (con divisor $n-1$) es un estimador **rigurosamente insesgado** de la cuasivarianza poblacional aun en muestreo sin reposición sobre poblaciones finitas.

---

### **Solución del Ejercicio 15**
#### **1. Extracción e Interpretación de Variables**
- Población de errores: $\{1, \; 3, \; 5, \; 7\}$, tamaño $N = 4$.
- Muestreo con reposición de tamaño $n = 2$.

#### **2. Parámetros de la Población**
$$
\mu = \frac{1 + 3 + 5 + 7}{4} = \frac{16}{4} = \mathbf{4\text{ errores}}
$$
$$
\sigma^2 = \frac{(1-4)^2 + (3-4)^2 + (5-4)^2 + (7-4)^2}{4} = \frac{9 + 1 + 1 + 9}{4} = \frac{20}{4} = \mathbf{5\text{ errores}^2}
$$
$$
\sigma = \sqrt{5} \approx \mathbf{2.236\text{ errores}}
$$

#### **3. Distribución Muestral Teórica**
1. **Media esperada:**
   $$
   E[\bar{X}] = \mu = \mathbf{4\text{ errores}}
   $$
2. **Error estándar teórico:**
   $$
   \sigma_{\bar{X}} = \frac{\sigma}{\sqrt{n}} = \frac{\sqrt{5}}{\sqrt{2}} = \sqrt{2.5} \approx \mathbf{1.581\text{ errores}}
   $$
   $$
   \sigma^2_{\bar{X}} = \frac{5}{2} = \mathbf{2.5\text{ errores}^2}
   $$

#### **4. Conclusión e Interpretación Técnica**
Al promediar parejas de módulos de software, la variabilidad promedio de los errores se reduce de $2.236$ errores a $1.581$ errores, demostrando el efecto reductor de la dispersión provisto por el muestreo aleatorio.

---

### **Solución del Ejercicio 16**
#### **1. Extracción e Interpretación de Variables**
- Población: consumos de corriente $\{5, \; 10, \; 15\}$ mA, $N = 3$.
- Muestra con reposición: $n = 2$.
- Muestras posibles: $3^2 = 9$ pares equiprobables.

#### **2. Parámetros Poblacionales**
$$
\mu = \frac{5 + 10 + 15}{3} = \mathbf{10\text{ mA}}
$$
$$
\sigma^2 = \frac{(5-10)^2 + (10-10)^2 + (15-10)^2}{3} = \frac{25 + 0 + 25}{3} = \mathbf{\frac{50}{3}} \approx 16.67\text{ mA}^2
$$
$$
\sigma = \sqrt{\frac{50}{3}} \approx \mathbf{4.082\text{ mA}}
$$

#### **3. Distribución de la Media Muestral**
Valores de $\bar{x} = \frac{x_1 + x_2}{2}$:
- $(5,5) \to 5$ ($1/9$)
- $(5,10), (10,5) \to 7.5$ ($2/9$)
- $(5,15), (10,10), (15,5) \to 10$ ($3/9$)
- $(10,15), (15,10) \to 12.5$ ($2/9$)
- $(15,15) \to 15$ ($1/9$)

#### **4. Comparación de Dispersión**
$$
\sigma_{\bar{X}} = \frac{\sigma}{\sqrt{2}} = \sqrt{\frac{50/3}{2}} = \sqrt{\frac{25}{3}} = \frac{5}{\sqrt{3}} \approx \mathbf{2.887\text{ mA}}
$$
- Dispersión individual ($\sigma$): $4.082$ mA.
- Dispersión de la media ($\sigma_{\bar{X}}$): $2.887$ mA.
La dispersión de las medias muestrales es exactamente $\frac{1}{\sqrt{2}} \approx 0.707$ (70.7%) de la dispersión de los sensores individuales.

\newpage

---

## 📌 **SOLUCIONARIO: BLOQUE III (EJERCICIOS 17 AL 26)**
### **Distribución Normal y Teorema Central del Límite**

---

### **Solución del Ejercicio 17**
#### **1. Extracción e Interpretación de Variables**
- Variable aleatoria continua individual: $X =$ Consumo de RAM por contenedor (MB).
- Parámetros poblacionales conocidos del enunciado:
  - Media poblacional: $\mu = 320\text{ MB}$.
  - Desviación estándar poblacional: $\sigma = 45\text{ MB}$.
  - Distribución del proceso: $X \sim N(320, \; 45^2)$.

#### **2. Elección del Modelo y Estandarización**
Dado que la variable es directamente normal y se evalúa un único contenedor individual ($n = 1$), se aplica la variable normal estandarizada:
$$
Z = \frac{X - \mu}{\sigma} \sim N(0, \; 1)
$$

#### **3. Desarrollo Matemático y Operaciones**
1. **Probabilidad de consumo entre 300 MB y 380 MB:**
   $$
   z_1 = \frac{300 - 320}{45} = \frac{-20}{45} \approx \mathbf{-0.44}
   $$
   $$
   z_2 = \frac{380 - 320}{45} = \frac{60}{45} \approx \mathbf{1.33}
   $$
   Buscando probabilidades en tabla normal:
   $$
   \Phi(1.33) = 0.9082, \quad \Phi(-0.44) = 0.3300
   $$
   $$
   P(300 \le X \le 380) = \Phi(1.33) - \Phi(-0.44)
   $$
   $$
   P(300 \le X \le 380) = 0.9082 - 0.3300 = \mathbf{0.5782}
   $$

2. **Proporción de contenedores que demandan más de 400 MB:**
   $$
   z = \frac{400 - 320}{45} = \frac{80}{45} \approx \mathbf{1.78}
   $$
   $$
   P(X > 400) = 1 - \Phi(1.78)
   $$
   $$
   P(X > 400) = 1 - 0.9625 = \mathbf{0.0375}
   $$

#### **4. Conclusión e Interpretación Técnica**
Aproximadamente el 57.82% de los microservicios operará dentro del rango óptimo de 300 a 380 MB. Solo un 3.75% de las instancias superará los 400 MB, permitiendo dimensionar los límites de memoria (memory limits) de Docker sin riesgo de saturación generalizada.

---

### **Solución del Ejercicio 18**
#### **1. Extracción e Interpretación de Variables**
- Parámetros del enlace troncal:
  - Media poblacional: $\mu = 950\text{ Mbps}$.
  - Desviación estándar poblacional: $\sigma = 30\text{ Mbps}$.
- Auditoría sobre una muestra de enlaces:
  - Tamaño muestral: $n = 36$ enlaces.
  - Variable analizada: Media muestral $\bar{X}$.

#### **2. Elección del Modelo y Parámetros Muestrales**
Como la población es normal y $n = 36 \ge 30$, la media muestral sigue una distribución normal exacta:
$$
\bar{X} \sim N\left(\mu_{\bar{X}} = \mu, \; \sigma_{\bar{X}} = \frac{\sigma}{\sqrt{n}}\right)
$$

#### **3. Desarrollo Matemático y Operaciones**
1. **Media esperada y error estándar:**
   $$
   E[\bar{X}] = \mu = \mathbf{950\text{ Mbps}}
   $$
   $$
   \sigma_{\bar{X}} = \frac{30}{\sqrt{36}} = \frac{30}{6} = \mathbf{5\text{ Mbps}}
   $$

2. **Probabilidad de que la media muestral supere 960 Mbps:**
   $$
   z = \frac{960 - 950}{5} = \frac{10}{5} = \mathbf{2.00}
   $$
   $$
   P(\bar{X} > 960) = 1 - \Phi(2.00)
   $$
   $$
   P(\bar{X} > 960) = 1 - 0.9772 = \mathbf{0.0228} \quad (2.28\%)
   $$

3. **Probabilidad de que la media se ubique entre 940 y 955 Mbps:**
   $$
   z_1 = \frac{940 - 950}{5} = \frac{-10}{5} = -2.00
   $$
   $$
   z_2 = \frac{955 - 950}{5} = \frac{5}{5} = 1.00
   $$
   $$
   P(940 \le \bar{X} \le 955) = \Phi(1.00) - \Phi(-2.00)
   $$
   $$
   P(940 \le \bar{X} \le 955) = 0.8413 - 0.0228 = \mathbf{0.8185} \quad (81.85\%)
   $$

#### **4. Conclusión e Interpretación Técnica**
Gracias al agrupamiento de 36 enlaces, la dispersión se redujo de 30 Mbps a solo 5 Mbps. Es altamente probable (81.85%) que la velocidad promedio de la muestra se mantenga entre 940 y 955 Mbps, y resulta extremadamente improbable (2.28%) que supere los 960 Mbps de manera sostenida.

---

### **Solución del Ejercicio 19**
#### **1. Extracción e Interpretación de Variables**
- Población original: distribución marcadamente asimétrica.
  - Media poblacional: $\mu = 1.200\text{ pet/s}$.
  - Desviación estándar poblacional: $\sigma = 300\text{ pet/s}$.
- Auditoría sobre servidores de nube:
  - Tamaño de muestra: $n = 64$ servidores independientes.

#### **2. Justificación Teórica: Teorema Central del Límite**
Aunque la población original no sea normal y presente fuerte asimetría, el **Teorema Central del Límite (TCL)** establece que la distribución muestral de la media $\bar{X}$ converge hacia una distribución normal a medida que crece el tamaño muestral. Al ser $n = 64 > 30$, la aproximación normal es perfectamente válida:
$$
\bar{X} \approx N\left(\mu = 1.200, \; \sigma_{\bar{X}} = \frac{300}{\sqrt{64}}\right)
$$

#### **3. Desarrollo Matemático y Operaciones**
1. **Error estándar de la media:**
   $$
   \sigma_{\bar{X}} = \frac{300}{8} = \mathbf{37.5\text{ pet/s}}
   $$

2. **Cálculo de probabilidad entre 1.150 y 1.260 pet/s:**
   $$
   z_1 = \frac{1.150 - 1.200}{37.5} = \frac{-50}{37.5} \approx \mathbf{-1.33}
   $$
   $$
   z_2 = \frac{1.260 - 1.200}{37.5} = \frac{60}{37.5} = \mathbf{1.60}
   $$
   Valores acumulados:
   $$
   \Phi(1.60) = 0.9452, \quad \Phi(-1.33) = 0.0918
   $$
   $$
   P(1.150 \le \bar{X} \le 1.260) = 0.9452 - 0.0918 = \mathbf{0.8534} \quad (85.34\%)
   $$

#### **4. Conclusión e Interpretación Técnica**
Existe una probabilidad del 85.34% de que el promedio de solicitudes por segundo procesadas por los 64 servidores se ubique entre 1.150 y 1.260 pet/s, amortiguando la asimetría individual del tráfico.

---

### **Solución del Ejercicio 20**
#### **1. Extracción e Interpretación de Variables**
- Variable: $X =$ Tiempo de respuesta de transacción (ms).
- Distribución: $X \sim N(\mu = 85, \; \sigma = 18)$.
- Condición de corte: umbral superior que delimita al 1% de las transacciones más lentas:
  $$
  P(X > x_{\text{corte}}) = 0.01 \iff P(X \le x_{\text{corte}}) = 0.99
  $$

#### **2. Elección del Modelo y Cuantil Normal**
Buscamos el valor $z$ correspondiente a un área acumulada de $0.9900$:
$$
z_{0.01} = \Phi^{-1}(0.99) \approx \mathbf{2.326} \quad (\text{o } 2.33)
$$

#### **3. Desarrollo Matemático y Operaciones**
Despejamos la variable original de la relación de estandarización:
$$
x_{\text{corte}} = \mu + z \cdot \sigma
$$
$$
x_{\text{corte}} = 85 + 2.326 \cdot 18
$$
$$
x_{\text{corte}} = 85 + 41.868 = \mathbf{126.87\text{ ms}}
$$
*(Utilizando $z = 2.33$: $85 + 2.33 \cdot 18 = 126.94\text{ ms}$).*

#### **4. Conclusión e Interpretación Técnica**
El umbral de alarma crítica debe fijarse en **126.87 milisegundos**. Cualquier petición que supere este valor pertenece al 1% de peor rendimiento y disparará una alerta técnica de degradación de servicio.

---

### **Solución del Ejercicio 21**
#### **1. Extracción e Interpretación de Variables**
- Variable: $X =$ Autonomía de batería en sensores IoT (horas).
- Distribución: $X \sim N(\mu = 1.800, \; \sigma = 120)$.
- Condición de garantía: reemplazo para el 2.5% inferior de menor duración:
  $$
  P(X \le x_{\text{garantía}}) = 0.025
  $$

#### **2. Elección del Modelo y Cuantil Crítico**
Para un área en la cola izquierda del 2.5% ($0.0250$):
$$
z_{0.025} = \Phi^{-1}(0.025) = \mathbf{-1.96}
$$

#### **3. Desarrollo Matemático y Operaciones**
$$
x_{\text{garantía}} = \mu + z \cdot \sigma
$$
$$
x_{\text{garantía}} = 1.800 + (-1.96) \cdot 120
$$
$$
x_{\text{garantía}} = 1.800 - 235.2 = \mathbf{1.564.8\text{ horas}}
$$

#### **4. Conclusión e Interpretación Técnica**
El fabricante debe fijar la garantía de reemplazo en **1.564.8 horas de servicio continuo** (aproximadamente 65 días). Con este umbral, estadísticamente solo el 2.5% de los sensores fallará antes de dicho plazo, protegiendo los costos del fabricante.

---

### **Solución del Ejercicio 22**
#### **1. Extracción e Interpretación de Variables**
- Población finita del cluster: $N = 250$ servidores.
- Parámetros poblacionales: $\mu = 42\text{ s}$, $\sigma = 8\text{ s}$.
- Muestra piloto: $n = 40$ servidores sin reposición.
- Fracción de muestreo:
  $$
  \frac{n}{N} = \frac{40}{250} = 0.16 \quad (16\% > 5\%)
  $$

#### **2. Elección del Modelo: Factor de Corrección por Población Finita (CPF)**
Dado que la fracción supera el 5% y el muestreo es sin reposición, se aplica el CPF al error estándar:
$$
\text{CPF} = \sqrt{\frac{N - n}{N - 1}} = \sqrt{\frac{250 - 40}{250 - 1}} = \sqrt{\frac{210}{249}} \approx \mathbf{0.9184}
$$
$$
\sigma_{\bar{X}} = \frac{\sigma}{\sqrt{n}} \cdot \text{CPF}
$$

#### **3. Desarrollo Matemático y Operaciones**
1. **Cálculo del error estándar corregido:**
   $$
   \sigma_{\bar{X}} = \frac{8}{\sqrt{40}} \cdot 0.9184 = \frac{8}{6.3246} \cdot 0.9184
   $$
   $$
   \sigma_{\bar{X}} = 1.2649 \cdot 0.9184 = \mathbf{1.1617\text{ s}}
   $$

2. **Estandarización del intervalo [40 s, 44 s]:**
   $$
   z_1 = \frac{40 - 42}{1.1617} = \frac{-2}{1.1617} \approx \mathbf{-1.72}
   $$
   $$
   z_2 = \frac{44 - 42}{1.1617} = \frac{2}{1.1617} \approx \mathbf{1.72}
   $$
   $$
   P(40 \le \bar{X} \le 44) = \Phi(1.72) - \Phi(-1.72)
   $$
   $$
   P(40 \le \bar{X} \le 44) = 0.9573 - 0.0427 = \mathbf{0.9146} \quad (91.46\%)
   $$

#### **4. Conclusión e Interpretación Técnica**
Existe una probabilidad del 91.46% de que el tiempo medio de despliegue en la muestra de 40 servidores se encuentre entre 40 y 44 segundos. Ignorar el CPF habría sobreestimado la dispersión y arrojado una probabilidad inferior (88.58%).

---

### **Solución del Ejercicio 23**
#### **1. Extracción e Interpretación de Variables**
- Variable individual: $X =$ Tráfico de streaming (GB/h).
- Parámetros: $\mu = 4.8\text{ GB/h}$, $\sigma = 0.9\text{ GB/h}$.
- Región central requerida: 90% central de los consumos individuales.
- Nivel de significación en los extremos: $\alpha = 0.10 \implies \alpha/2 = 0.05$ por cola.

#### **2. Elección del Modelo y Coeficiente Crítico**
Para delimitar el 90% central en una distribución normal:
$$
z_{\text{crit}} = \Phi^{-1}(0.95) = \mathbf{1.645}
$$

#### **3. Desarrollo Matemático y Operaciones**
$$
L.I. = \mu - z \cdot \sigma = 4.8 - 1.645 \cdot 0.9
$$
$$
L.I. = 4.8 - 1.4805 = \mathbf{3.32\text{ GB/h}}
$$
$$
L.S. = \mu + z \cdot \sigma = 4.8 + 1.645 \cdot 0.9
$$
$$
L.S. = 4.8 + 1.4805 = \mathbf{6.28\text{ GB/h}}
$$

#### **4. Conclusión e Interpretación Técnica**
El 90% central de los usuarios consume entre **3.32 GB/h y 6.28 GB/h**. Solo el 5% de los usuarios consume menos de 3.32 GB/h y el 5% más demandante supera los 6.28 GB/h.

---

### **Solución del Ejercicio 24**
#### **1. Extracción e Interpretación de Variables**
- Parámetros individuales de los discos: $\mu = 55.000\text{ hs}$, $\sigma = 4.000\text{ hs}$.
- Muestra instalada en el rack: $n = 100$ discos SSD independientes.
- Variable de análisis: Media muestral $\bar{X}$.

#### **2. Elección del Modelo y Parámetros Muestrales**
Por distribución normal y tamaño $n = 100 \ge 30$:
$$
\bar{X} \sim N\left(\mu = 55.000, \; \sigma_{\bar{X}} = \frac{\sigma}{\sqrt{n}}\right)
$$
$$
\sigma_{\bar{X}} = \frac{4.000}{\sqrt{100}} = \frac{4.000}{10} = \mathbf{400\text{ hs}}
$$

#### **3. Desarrollo Matemático y Operaciones**
$$
z = \frac{55.600 - 55.000}{400} = \frac{600}{400} = \mathbf{1.50}
$$
$$
P(\bar{X} > 55.600) = 1 - \Phi(1.50)
$$
$$
P(\bar{X} > 55.600) = 1 - 0.9332 = \mathbf{0.0668} \quad (6.68\%)
$$

#### **4. Conclusión e Interpretación Técnica**
La probabilidad de que el lote de 100 discos del rack mantenga una vida promedio superior a 55.600 horas es de apenas el 6.68%. La mayor parte de los racks promediará muy cerca del valor nominal de 55.000 horas.

---

### **Solución del Ejercicio 25**
#### **1. Extracción e Interpretación de Variables**
- Población del lote: $N = 400$ placas de red.
- Parámetros: $\mu = 980\text{ MHz}$, $\sigma = 25\text{ MHz}$.
- Muestra sin reposición: $n = 50$ placas.
- Fracción de muestreo: $\frac{n}{N} = \frac{50}{400} = 0.125 > 0.05 \implies \text{requiere CPF}$.

#### **2. Elección del Modelo y CPF**
$$
\text{CPF} = \sqrt{\frac{400 - 50}{400 - 1}} = \sqrt{\frac{350}{399}} \approx \mathbf{0.9366}
$$
$$
\sigma_{\bar{X}} = \frac{25}{\sqrt{50}} \cdot 0.9366 = \frac{25}{7.0711} \cdot 0.9366 \approx \mathbf{3.311\text{ MHz}}
$$

#### **3. Desarrollo Matemático y Operaciones**
$$
z_1 = \frac{975 - 980}{3.311} = \frac{-5}{3.311} \approx \mathbf{-1.51}
$$
$$
z_2 = \frac{985 - 980}{3.311} = \frac{5}{3.311} \approx \mathbf{1.51}
$$
$$
P(975 \le \bar{X} \le 985) = \Phi(1.51) - \Phi(-1.51)
$$
$$
P(975 \le \bar{X} \le 985) = 0.9345 - 0.0655 = \mathbf{0.8690} \quad (86.90\%)
$$

#### **4. Conclusión e Interpretación Técnica**
Existe una probabilidad del 86.90% de que la frecuencia media de la muestra de 50 placas se sitúe dentro de $\pm 5$ MHz del valor nominal.

---

### **Solución del Ejercicio 26**
#### **1. Extracción e Interpretación de Variables**
- Población: tiempos de restauración con marcada asimetría positiva.
  - Media poblacional: $\mu = 75\text{ min}$.
  - Desviación estándar poblacional: $\sigma = 22\text{ min}$.
- Muestra auditada: $n = 49$ incidentes.

#### **2. Aplicación del Teorema Central del Límite**
Dado que $n = 49 \ge 30$, por TCL la media muestral se aproxima normalmente:
$$
\sigma_{\bar{X}} = \frac{22}{\sqrt{49}} = \frac{22}{7} \approx \mathbf{3.1429\text{ min}}
$$

#### **3. Desarrollo Matemático y Operaciones**
$$
z = \frac{70 - 75}{3.1429} = \frac{-5}{3.1429} \approx \mathbf{-1.59}
$$
$$
P(\bar{X} < 70) = \Phi(-1.59) = \mathbf{0.0559} \quad (5.59\%)
$$

#### **4. Conclusión e Interpretación Técnica**
La probabilidad de que una muestra de 49 incidentes logre un tiempo medio de recuperación inferior a 70 minutos es de solo el 5.59%, lo que alerta al equipo de contingencia a no comprometer SLAs por debajo de 75 minutos sin ampliar la capacidad técnica.

\newpage

---

## 📌 **SOLUCIONARIO: BLOQUE IV (EJERCICIOS 27 AL 36)**
### **Intervalos de Confianza para la Media Poblacional**

---

### **Solución del Ejercicio 27**
#### **1. Extracción e Interpretación de Variables**
- Tamaño de la muestra: $n = 18$ ejecuciones.
- Media muestral: $\bar{X} = 4.2\text{ minutos}$.
- Desviación estándar muestral: $s = 0.8\text{ minutos}$ *(es muestral $s$, pues surge de las 18 ejecuciones; la poblacional $\sigma$ es desconocida)*.
- Nivel de confianza: $1 - \alpha = 0.95 \implies \alpha = 0.05$.

#### **2. Elección del Modelo y Justificación**
- Población normal.
- Desviación estándar poblacional $\sigma$ desconocida.
- Tamaño muestral pequeño ($n = 18 < 30$).
- **Modelo obligatorio:** Distribución **$t$ de Student** con $n - 1 = 17$ grados de libertad:
  $$
  t_{\alpha/2; \; n-1} = t_{0.025; \; 17} = \mathbf{2.110}
  $$

#### **3. Desarrollo Matemático y Operaciones**
1. **Margen de error ($E$):**
   $$
   E = t_{0.025; \; 17} \cdot \frac{s}{\sqrt{n}}
   $$
   $$
   E = 2.110 \cdot \frac{0.8}{\sqrt{18}} = 2.110 \cdot \frac{0.8}{4.2426}
   $$
   $$
   E = 2.110 \cdot 0.1886 \approx \mathbf{0.398\text{ min}}
   $$

2. **Límites del intervalo de confianza:**
   $$
   L.I. = \bar{X} - E = 4.2 - 0.398 = \mathbf{3.802\text{ min}}
   $$
   $$
   L.S. = \bar{X} + E = 4.2 + 0.398 = \mathbf{4.598\text{ min}}
   $$
   $$
   IC_{95\%}(\mu) = [\mathbf{3.802\text{ min}}, \; \mathbf{4.598\text{ min}}]
   $$

#### **4. Conclusión e Interpretación Técnica**
Con un 95% de confianza, el tiempo medio real de compilación de todo el sistema se encuentra entre 3.80 y 4.60 minutos.

---

### **Solución del Ejercicio 28**
#### **1. Extracción e Interpretación de Variables**
- Muestra de fuentes de poder: $n = 40$ unidades.
- Media muestral observada: $\bar{X} = 12.04\text{ V}$.
- Desviación estándar poblacional conocida por diseño: $\sigma = 0.15\text{ V}$ *(es $\sigma$ porque proviene de las especificaciones globales de calibración)*.

#### **2. Elección del Modelo y Valores Críticos**
Dado que la varianza poblacional es conocida y $n = 40 \ge 30$, se emplea la distribución Normal estándar ($Z$):
- Al 90% de confianza: $z_{0.05} = 1.645$.
- Al 98% de confianza: $z_{0.01} = 2.326$.

#### **3. Desarrollo Matemático y Operaciones**
1. **Error estándar:**
   $$
   \sigma_{\bar{X}} = \frac{0.15}{\sqrt{40}} = \frac{0.15}{6.3246} \approx \mathbf{0.02372\text{ V}}
   $$

2. **Intervalo al 90% de confianza:**
   $$
   E_{90\%} = 1.645 \cdot 0.02372 \approx \mathbf{0.039\text{ V}}
   $$
   $$
   L.I. = 12.04 - 0.039 = \mathbf{12.001\text{ V}}
   $$
   $$
   L.S. = 12.04 + 0.039 = \mathbf{12.079\text{ V}}
   $$
   $$
   IC_{90\%}(\mu) = [\mathbf{12.001\text{ V}}, \; \mathbf{12.079\text{ V}}]
   $$

3. **Intervalo al 98% de confianza:**
   $$
   E_{98\%} = 2.326 \cdot 0.02372 \approx \mathbf{0.055\text{ V}}
   $$
   $$
   L.I. = 12.04 - 0.055 = \mathbf{11.985\text{ V}}
   $$
   $$
   L.S. = 12.04 + 0.055 = \mathbf{12.095\text{ V}}
   $$
   $$
   IC_{98\%}(\mu) = [\mathbf{11.985\text{ V}}, \; \mathbf{12.095\text{ V}}]
   $$

#### **4. Comparación de Amplitud e Interpretación**
- Amplitud al 90%: $2 \cdot 0.039 = 0.078\text{ V}$.
- Amplitud al 98%: $2 \cdot 0.055 = 0.110\text{ V}$.
Al exigir mayor certeza (98% vs. 90%), el intervalo se ensancha un 41%, aumentando el margen de error para cubrir una mayor proporción de incertidumbre.

---

### **Solución del Ejercicio 29**
#### **1. Extracción e Interpretación de Variables**
- Lote total cerrado: $N = 600$ unidades.
- Muestra extraída: $n = 40$ unidades.
- Fracción de muestreo: $\frac{n}{N} = \frac{40}{600} = 0.0667 > 0.05 \implies \text{requiere CPF}$.
- Nivel de confianza: 98% ($z = 2.326$).

#### **2. Elección del Modelo y Factor Finito**
$$
\text{CPF} = \sqrt{\frac{N - n}{N - 1}} = \sqrt{\frac{600 - 40}{600 - 1}} = \sqrt{\frac{560}{599}} \approx \mathbf{0.9669}
$$

#### **3. Desarrollo Matemático y Operaciones**
$$
E = z \cdot \frac{\sigma}{\sqrt{n}} \cdot \text{CPF}
$$
$$
E = 0.0552 \cdot 0.9669 \approx \mathbf{0.0534\text{ V}}
$$
$$
L.I. = 12.04 - 0.0534 = \mathbf{11.987\text{ V}}
$$
$$
L.S. = 12.04 + 0.0534 = \mathbf{12.093\text{ V}}
$$
$$
IC_{98\%}(\mu)_{\text{finito}} = [\mathbf{11.987\text{ V}}, \; \mathbf{12.093\text{ V}}]
$$

#### **4. Conclusión e Interpretación Técnica**
El factor de población finita reduce el error de $0.0552\text{ V}$ a $0.0534\text{ V}$ debido a que el 6.67% del lote ya fue inspeccionado.

---

### **Solución del Ejercicio 30**
#### **1. Extracción e Interpretación de Variables**
- Tamaño muestral: $n = 12$ racks de servidores.
- Media muestral: $\bar{X} = 3.8\text{ kW}$.
- Varianza muestral informada: $s^2 = 0.36\text{ kW}^2 \implies s = \sqrt{0.36} = 0.6\text{ kW}$.
- Nivel de confianza: $99\% \implies \alpha = 0.01 \implies \alpha/2 = 0.005$.

#### **2. Elección del Modelo y Parámetro Crítico**
- Supuesto de normalidad.
- Varianza poblacional $\sigma^2$ desconocida.
- Tamaño $n = 12 < 30 \implies t$ de Student con $\nu = 12 - 1 = 11$ grados de libertad:
  $$
  t_{0.005; \; 11} = \mathbf{3.106}
  $$

#### **3. Desarrollo Matemático y Operaciones**
$$
E = t_{0.005; \; 11} \cdot \frac{s}{\sqrt{n}}
$$
$$
E = 3.106 \cdot \frac{0.6}{\sqrt{12}} = 3.106 \cdot \frac{0.6}{3.4641}
$$
$$
E = 3.106 \cdot 0.1732 \approx \mathbf{0.538\text{ kW}}
$$
$$
L.I. = 3.8 - 0.538 = \mathbf{3.262\text{ kW}}
$$
$$
L.S. = 3.8 + 0.538 = \mathbf{4.338\text{ kW}}
$$
$$
IC_{99\%}(\mu) = [\mathbf{3.262\text{ kW}}, \; \mathbf{4.338\text{ kW}}]
$$

#### **4. Conclusión e Interpretación Técnica**
Con una certidumbre técnica del 99%, el consumo medio por rack en el centro de datos oscila entre 3.26 kW y 4.34 kW, dato fundamental para el dimensionamiento de las unidades UPS y aires acondicionados.

---

### **Solución del Ejercicio 31**
#### **1. Extracción e Interpretación de Variables**
- Muestra de tickets: $n = 45$ tickets resueltos.
- Media muestral: $\bar{X} = 16.5\text{ minutos}$.
- Desviación muestral: $s = 3.5\text{ minutos}$.
- Nivel de confianza: $90\% \implies \alpha = 0.10 \implies \alpha/2 = 0.05$.

#### **2. Elección del Modelo y Justificación**
Dado que el tamaño de la muestra es grande ($n = 45 \ge 30$), por el Teorema Central del Límite el estimador estándar se comporta normalmente:
$$
z_{0.05} = \mathbf{1.645}
$$

#### **3. Desarrollo Matemático y Operaciones**
$$
E = z_{0.05} \cdot \frac{s}{\sqrt{n}}
$$
$$
E = 1.645 \cdot \frac{3.5}{\sqrt{45}} = 1.645 \cdot \frac{3.5}{6.7082}
$$
$$
E = 1.645 \cdot 0.5217 \approx \mathbf{0.858\text{ min}}
$$
$$
L.I. = 16.5 - 0.858 = \mathbf{15.642\text{ min}}
$$
$$
L.S. = 16.5 + 0.858 = \mathbf{17.358\text{ min}}
$$
$$
IC_{90\%}(\mu) = [\mathbf{15.642\text{ min}}, \; \mathbf{17.358\text{ min}}]
$$

#### **4. Conclusión e Interpretación Técnica**
El tiempo medio global para la resolución de un incidente de soporte técnico se ubica entre 15.64 y 17.36 minutos al 90% de confianza.

---

### **Solución del Ejercicio 32**
#### **1. Extracción e Interpretación de Variables**
- Muestra de archivos procesados: $n = 50$ archivos.
- Media muestral de ahorro: $\bar{X} = 68\%$.
- Desviación estándar muestral: $s = 4.2\%$.
- Nivel de confianza: $95\% \implies z = 1.96$.

#### **2. Elección del Modelo**
Tamaño de muestra grande ($n = 50 \ge 30$) con varianza poblacional desconocida:
$$
z_{0.025} = \mathbf{1.96}
$$

#### **3. Desarrollo Matemático y Operaciones**
$$
E = 1.96 \cdot \frac{4.2}{\sqrt{50}} = 1.96 \cdot \frac{4.2}{7.0711}
$$
$$
E = 1.96 \cdot 0.5940 \approx \mathbf{1.164\%}
$$
$$
L.I. = 68 - 1.164 = \mathbf{66.836\%}
$$
$$
L.S. = 68 + 1.164 = \mathbf{69.164\%}
$$
$$
IC_{95\%}(\mu) = [\mathbf{66.836\%}, \; \mathbf{69.164\%}]
$$

#### **4. Conclusión e Interpretación Técnica**
El algoritmo de compresión garantiza una reducción media de tamaño de imagen situada entre 66.84% y 69.16% con un 95% de confianza.

---

### **Solución del Ejercicio 33**
#### **1. Extracción e Interpretación de Variables**
- Parámetro poblacional conocido por ensayos previos: $\sigma = 3.5\text{ }^\circ\text{C}$.
- Muestra auditada: $n = 35$ microprocesadores.
- Media muestral: $\bar{X} = 72.4\text{ }^\circ\text{C}$.

#### **2. Elección del Modelo y Error Estándar**
Con $\sigma$ conocida y $n = 35 \ge 30$, se emplea la distribución Normal estándar ($Z$):
$$
\sigma_{\bar{X}} = \frac{3.5}{\sqrt{35}} = \frac{3.5}{5.9161} \approx \mathbf{0.5916\text{ }^\circ\text{C}}
$$

#### **3. Desarrollo Matemático y Operaciones**
1. **Intervalo al 95% de confianza ($z = 1.96$):**
   $$
   E_{95\%} = 1.96 \cdot 0.5916 \approx \mathbf{1.160\text{ }^\circ\text{C}}
   $$
   $$
   L.I. = 72.4 - 1.160 = \mathbf{71.240\text{ }^\circ\text{C}}
   $$
   $$
   L.S. = 72.4 + 1.160 = \mathbf{73.560\text{ }^\circ\text{C}}
   $$
   $$
   IC_{95\%}(\mu) = [\mathbf{71.240\text{ }^\circ\text{C}}, \; \mathbf{73.560\text{ }^\circ\text{C}}]
   $$

2. **Intervalo al 99% de confianza ($z = 2.576$):**
   $$
   E_{99\%} = 2.576 \cdot 0.5916 \approx \mathbf{1.524\text{ }^\circ\text{C}}
   $$
   $$
   L.I. = 72.4 - 1.524 = \mathbf{70.876\text{ }^\circ\text{C}}
   $$
   $$
   L.S. = 72.4 + 1.524 = \mathbf{73.924\text{ }^\circ\text{C}}
   $$
   $$
   IC_{99\%}(\mu) = [\mathbf{70.876\text{ }^\circ\text{C}}, \; \mathbf{73.924\text{ }^\circ\text{C}}]
   $$

#### **4. Conclusión e Interpretación Técnica**
Al 99% de confianza, la temperatura promedio real bajo carga máxima no supera los 73.92 °C, asegurando que el microprocesador opera lejos de su umbral térmico de degradación de 85 °C.

---

### **Solución del Ejercicio 34**
#### **1. Extracción e Interpretación de Datos Directos**
- Muestras de latencia ($n = 8$ solicitudes por protocolo):
  - **HTTP/2 (A):** $\{42, 45, 39, 44, 41, 46, 40, 43\}$
    $$
    \bar{X}_A = \frac{340}{8} = \mathbf{42.50\text{ ms}}
    $$
    $$
    s_A^2 = \frac{\sum (x_{iA} - 42.5)^2}{7} = \frac{42}{7} = \mathbf{6.00} \implies s_A = \mathbf{2.4495\text{ ms}}
    $$
  - **HTTP/3 (B):** $\{31, 35, 29, 33, 30, 34, 32, 28\}$
    $$
    \bar{X}_B = \frac{252}{8} = \mathbf{31.50\text{ ms}}
    $$
    $$
    s_B^2 = \frac{\sum (x_{iB} - 31.5)^2}{7} = \frac{42}{7} = \mathbf{6.00} \implies s_B = \mathbf{2.4495\text{ ms}}
    $$

#### **2. Elección del Modelo: Student con $n - 1 = 7$ g.l.**
Con $n = 8 < 30$ y varianzas poblacionales desconocidas:
$$
t_{0.025; \; 7} = \mathbf{2.365}
$$

#### **3. Desarrollo Matemático y Operaciones**
El margen de error es idéntico para ambos protocolos:
$$
E = 2.365 \cdot \frac{2.4495}{\sqrt{8}} = 2.365 \cdot \frac{2.4495}{2.8284}
$$
$$
E = 2.365 \cdot 0.8660 \approx \mathbf{2.048\text{ ms}}
$$

1. **Intervalo para HTTP/2:**
   $$
   IC_{95\%}(\mu_A) = [42.50 - 2.05, \; 42.50 + 2.05] = [\mathbf{40.45\text{ ms}}, \; \mathbf{44.55\text{ ms}}]
   $$
2. **Intervalo para HTTP/3:**
   $$
   IC_{95\%}(\mu_B) = [31.50 - 2.05, \; 31.50 + 2.05] = [\mathbf{29.45\text{ ms}}, \; \mathbf{33.55\text{ ms}}]
   $$

#### **4. Conclusión e Interpretación Técnica**
Los intervalos no se solapan: el límite superior de HTTP/3 ($33.55\text{ ms}$) es estrictamente menor al límite inferior de HTTP/2 ($40.45\text{ ms}$). Existe evidencia estadística con un 95% de confianza de que HTTP/3 reduce de forma real y significativa la latencia de transferencia web.

---

### **Solución del Ejercicio 35**
#### **1. Extracción e Interpretación de Variables**
- Muestra de placas PCB: $n = 14$ placas.
- Longitud media muestral: $\bar{X} = 28.5\text{ mm}$.
- Desviación estándar muestral: $s = 1.2\text{ mm}$.
- Nivel de confianza: $95\% \implies \alpha = 0.05$.

#### **2. Elección del Modelo: Student con $n - 1 = 13$ g.l.**
Población normal con $\sigma$ desconocida y $n = 14 < 30$:
$$
t_{0.025; \; 13} = \mathbf{2.160}
$$

#### **3. Desarrollo Matemático y Operaciones**
$$
E = 2.160 \cdot \frac{1.2}{\sqrt{14}} = 2.160 \cdot \frac{1.2}{3.7417}
$$
$$
E = 2.160 \cdot 0.3207 \approx \mathbf{0.693\text{ mm}}
$$
$$
L.I. = 28.5 - 0.693 = \mathbf{27.807\text{ mm}}
$$
$$
L.S. = 28.5 + 0.693 = \mathbf{29.193\text{ mm}}
$$
$$
IC_{95\%}(\mu) = [\mathbf{27.807\text{ mm}}, \; \mathbf{29.193\text{ mm}}]
$$

#### **4. Conclusión e Interpretación Técnica**
La longitud media poblacional de las pistas críticas de fotograbado se encuentra entre 27.81 mm y 29.19 mm con un 95% de certidumbre estadística.

---

### **Solución del Ejercicio 36**
#### **1. Extracción e Interpretación de Datos Directos**
- Registros muestrales ($n = 9$ ejecuciones de consulta):
  $$
  \{52, \; 48, \; 55, \; 50, \; 49, \; 53, \; 47, \; 51, \; 54\}
  $$
- Suma: $\sum x_i = 459 \implies \bar{X} = \frac{459}{9} = \mathbf{51.00\text{ s}}$.
- Suma de cuadrados de desvíos:
  $$
  \sum (x_i - 51)^2 = 1 + 9 + 16 + 1 + 4 + 4 + 16 + 0 + 9 = 60
  $$
- Cuasivarianza muestral insesgada:
  $$
  s^2 = \frac{60}{9 - 1} = \frac{60}{8} = \mathbf{7.50} \implies s = \sqrt{7.50} \approx \mathbf{2.7386\text{ s}}
  $$

#### **2. Elección del Modelo: Student con $n - 1 = 8$ g.l.**
Al 99% de confianza ($\alpha = 0.01 \implies \alpha/2 = 0.005$):
$$
t_{0.005; \; 8} = \mathbf{3.355}
$$

#### **3. Desarrollo Matemático y Operaciones**
$$
E = t_{0.005; \; 8} \cdot \frac{s}{\sqrt{n}} = 3.355 \cdot \frac{2.7386}{\sqrt{9}}
$$
$$
E = 3.355 \cdot \frac{2.7386}{3} = 3.355 \cdot 0.9129 \approx \mathbf{3.063\text{ s}}
$$
$$
L.I. = 51.00 - 3.063 = \mathbf{47.937\text{ s}}
$$
$$
L.S. = 51.00 + 3.063 = \mathbf{54.063\text{ s}}
$$
$$
IC_{99\%}(\mu) = [\mathbf{47.937\text{ s}}, \; \mathbf{54.063\text{ s}}]
$$

#### **4. Conclusión e Interpretación Técnica**
Con una confianza técnica del 99%, el tiempo medio de respuesta de esta consulta pesada al data warehouse se ubica entre 47.94 y 54.06 segundos.

\newpage

---

## 📌 **SOLUCIONARIO: BLOQUE V (EJERCICIOS 37 AL 42)**
### **Población Finita y Tamaño Óptimo de Muestra**

---

### **Solución del Ejercicio 37**
#### **1. Extracción e Interpretación de Variables**
- Desviación estándar poblacional del proveedor: $\sigma = 1.8\text{ }^\circ\text{C}$ *(es $\sigma$ por ser especificación previa de fabricación)*.
- Tamaño de la muestra: $n = 60$ sensores.
- Media muestral observada: $\bar{X} = 145.2\text{ }^\circ\text{C}$.
- Nivel de confianza: $95\% \implies \alpha = 0.05 \implies z_{0.025} = 1.96$.

#### **2. Elección del Modelo y Justificación**
Varianza conocida y muestra grande ($n = 60 \ge 30$):
$$
z_{0.025} = \mathbf{1.96}
$$

#### **3. Desarrollo Matemático y Operaciones**
$$
E = z \cdot \frac{\sigma}{\sqrt{n}} = 1.96 \cdot \frac{1.8}{\sqrt{60}}
$$
$$
E = 1.96 \cdot \frac{1.8}{7.7460} = 1.96 \cdot 0.2324 \approx \mathbf{0.455\text{ }^\circ\text{C}}
$$
$$
L.I. = 145.2 - 0.455 = \mathbf{144.745\text{ }^\circ\text{C}}
$$
$$
L.S. = 145.2 + 0.455 = \mathbf{145.655\text{ }^\circ\text{C}}
$$
$$
IC_{95\%}(\mu) = [\mathbf{144.745\text{ }^\circ\text{C}}, \; \mathbf{145.655\text{ }^\circ\text{C}}]
$$

#### **4. Conclusión e Interpretación Técnica**
La temperatura media real del reactor opera entre 144.75 °C y 145.66 °C con un 95% de confianza, garantizando estabilidad térmica del proceso.

---

### **Solución del Ejercicio 38**
#### **1. Extracción e Interpretación de Variables**
- Partida total de baterías: $N = 800$ unidades.
- Muestra de prueba: $n = 45$ unidades.
- Media muestral: $\bar{X} = 38.5\text{ minutos}$.
- Desviación estándar muestral: $s = 3.2\text{ minutos}$.
- Fracción de muestreo: $\frac{n}{N} = \frac{45}{800} = 0.05625 > 0.05 \implies \text{amerita CPF}$.

#### **2. Elección del Modelo y Factor de Corrección**
Nivel de confianza 95% ($z = 1.96$).
$$
\text{CPF} = \sqrt{\frac{N - n}{N - 1}} = \sqrt{\frac{800 - 45}{800 - 1}} = \sqrt{\frac{755}{799}} \approx \mathbf{0.9721}
$$

#### **3. Desarrollo Matemático y Operaciones**
1. **Asumiendo población infinita (sin CPF):**
   $$
   E_{\infty} = 1.96 \cdot \frac{3.2}{\sqrt{45}} = 1.96 \cdot \frac{3.2}{6.7082}
   $$
   $$
   E_{\infty} = 1.96 \cdot 0.4770 \approx \mathbf{0.935\text{ min}}
   $$
   $$
   IC_{95\%}(\mu)_{\infty} = [\mathbf{37.565\text{ min}}, \; \mathbf{39.435\text{ min}}]
   $$

2. **Considerando población finita (con CPF):**
   $$
   E_{\text{fin}} = E_{\infty} \cdot \text{CPF} = 0.935 \cdot 0.9721 \approx \mathbf{0.909\text{ min}}
   $$
   $$
   L.I. = 38.5 - 0.909 = \mathbf{37.591\text{ min}}
   $$
   $$
   L.S. = 38.5 + 0.909 = \mathbf{39.409\text{ min}}
   $$
   $$
   IC_{95\%}(\mu)_{\text{fin}} = [\mathbf{37.591\text{ min}}, \; \mathbf{39.409\text{ min}}]
   $$

#### **4. Conclusión e Interpretación Técnica**
El factor finito reduce el margen de error de $\pm 0.935$ a $\pm 0.909$ minutos (una reducción del 2.8%), otorgando un intervalo más ajustado al reconocer que la muestra cubre más del 5% del lote total.

---

### **Solución del Ejercicio 39**
#### **1. Extracción e Interpretación de Variables**
- Desviación típica estimada: $s \approx \sigma = 3.2\text{ minutos}$.
- Error máximo admisible: $e = 0.8\text{ minutos}$.
- Nivel de confianza: $95\% \implies z_{0.025} = 1.96$.

#### **2. Elección del Modelo y Fórmula de Tamaño Muestral**
Fórmula básica para población infinita:
$$
n_0 = \left(\frac{z \cdot \sigma}{e}\right)^2
$$

#### **3. Desarrollo Matemático y Operaciones**
1. **Cálculo preliminar para población infinita:**
   $$
   n_0 = \left(\frac{1.96 \cdot 3.2}{0.8}\right)^2 = (1.96 \cdot 4)^2
   $$
   $$
   n_0 = (7.84)^2 = 61.466 \implies \mathbf{62\text{ baterías}}
   $$

2. **Ajuste para la población finita de $N = 800$:**
   $$
   n = \frac{N \cdot n_0}{N + n_0 - 1} = \frac{800 \cdot 61.47}{800 + 61.47 - 1}
   $$
   $$
   n = \frac{49.176}{860.47} \approx 57.15 \implies \mathbf{58\text{ baterías}}
   $$

#### **4. Conclusión e Interpretación Técnica**
Se requiere auditar **62 baterías** si no se acota el tamaño del lote, o **58 baterías** aprovechando el tamaño finito de $800$ unidades. Se redondea siempre al entero inmediato superior para garantizar el error estipulado.

---

### **Solución del Ejercicio 40**
#### **1. Extracción e Interpretación de Variables**
- Desviación estándar histórica: $\sigma = 30\text{ segundos}$ *(conocida)*.
- Muestra inicial: $n = 50$ llamadas, con $\bar{X} = 180\text{ segundos}$.
- Nivel de confianza: $95\% \implies z = 1.96$.

#### **2. Desarrollo Matemático del Intervalo Actual**
$$
E = 1.96 \cdot \frac{30}{\sqrt{50}} = 1.96 \cdot \frac{30}{7.0711}
$$
$$
E = 1.96 \cdot 4.2426 \approx \mathbf{8.316\text{ s}}
$$
$$
IC_{95\%}(\mu) = [180 - 8.316, \; 180 + 8.316] = [\mathbf{171.684\text{ s}}, \; \mathbf{188.316\text{ s}}]
$$

#### **3. Tamaño Muestral para Reducir el Error a $e = 5$ segundos**
$$
n = \left(\frac{z \cdot \sigma}{e}\right)^2 = \left(\frac{1.96 \cdot 30}{5}\right)^2
$$
$$
n = (1.96 \cdot 6)^2 = (11.76)^2 = 138.298 \implies \mathbf{139\text{ llamadas}}
$$

#### **4. Conclusión e Interpretación Técnica**
Para reducir el margen de incertidumbre de 8.32 s a un máximo estricto de 5 s, el centro de soporte debe incrementar su muestra de 50 a **139 llamadas auditadas**.

---

### **Solución del Ejercicio 41**
#### **1. Extracción e Interpretación de Variables**
- Desviación estándar salarial previa: $\sigma = 15.000$.
- Margen de error deseado: $e = 2.500$.
- Niveles de confianza:
  - Al 95%: $z = 1.96$.
  - Al 99%: $z = 2.576$.

#### **2. Desarrollo Matemático y Operaciones**
1. **Tamaño muestral al 95% de confianza:**
   $$
   n_{95\%} = \left(\frac{1.96 \cdot 15.000}{2.500}\right)^2 = (1.96 \cdot 6)^2
   $$
   $$
   n_{95\%} = (11.76)^2 = 138.30 \implies \mathbf{139\text{ DBAs}}
   $$

2. **Tamaño muestral al 99% de confianza:**
   $$
   n_{99\%} = \left(\frac{2.576 \cdot 15.000}{2.500}\right)^2 = (2.576 \cdot 6)^2
   $$
   $$
   n_{99\%} = (15.456)^2 = 238.89 \implies \mathbf{239\text{ DBAs}}
   $$

#### **4. Conclusión e Interpretación Técnica**
Subir la exigencia de confianza del 95% al 99% demanda recolectar $100$ encuestas adicionales (un 72% de incremento muestral), manteniendo fijo el error de \$2.500.

---

### **Solución del Ejercicio 42**
#### **1. Extracción e Interpretación de Variables**
- Desviación estándar de facturación: $\sigma = 8.000$.
- Error máximo tolerado: $e = 1.200$.
- Nivel de confianza: $96\% \implies 1 - \alpha = 0.96 \implies \alpha = 0.04 \implies \alpha/2 = 0.02$.

#### **2. Elección del Modelo y Coeficiente Crítico**
Área en cada cola: $0.0200 \implies \Phi(z) = 0.9800$:
$$
z_{0.02} = \Phi^{-1}(0.98) \approx \mathbf{2.054} \quad (\text{o } 2.05)
$$

#### **3. Desarrollo Matemático y Operaciones**
$$
n = \left(\frac{z \cdot \sigma}{e}\right)^2 = \left(\frac{2.054 \cdot 8.000}{1.200}\right)^2
$$
$$
n = \left(\frac{16.432}{1.200}\right)^2 = (13.6933)^2 = 187.51 \implies \mathbf{188\text{ usuarios}}
$$
*(Utilizando $z = 2.05$: $(2.05 \cdot 6.6667)^2 = (13.667)^2 = 186.78 \implies 187\text{ usuarios}$).*

#### **4. Conclusión e Interpretación Técnica**
La auditoría debe muestrear al menos **188 cuentas de usuarios SaaS** para asegurar que el ingreso promedio estimado no se desvíe en más de \$1.200 con un 96% de confianza.

---
\newpage

---

## 📌 **SOLUCIONARIO: BLOQUE VI (EJERCICIOS 43 AL 46)**
### **Muestras Especiales y Control de Especificaciones**

---

### **Solución del Ejercicio 43**
#### **1. Extracción e Interpretación de Variables**
- Lote de producción diaria: $N = 200$ cables.
- Muestra de cables: $n = 35$ unidades.
- Media muestral de atenuación: $\bar{X} = 18.2\text{ dB}$.
- Desviación estándar poblacional: $\sigma = 4.5\text{ dB}$.
- Nivel de confianza: $98\% \implies \alpha = 0.02 \implies z_{0.01} = 2.326$.
- Fracción de muestreo: $\frac{n}{N} = \frac{35}{200} = 0.175 > 0.05 \implies \text{requiere CPF}$.

#### **2. Elección del Modelo y Factor Finito**
$$
\text{CPF} = \sqrt{\frac{N - n}{N - 1}} = \sqrt{\frac{200 - 35}{200 - 1}} = \sqrt{\frac{165}{199}} \approx \mathbf{0.9106}
$$

#### **3. Desarrollo Matemático y Operaciones**
$$
E = z \cdot \frac{\sigma}{\sqrt{n}} \cdot \text{CPF}
$$
$$
E = 2.326 \cdot \frac{4.5}{\sqrt{35}} \cdot 0.9106 = 2.326 \cdot 0.7606 \cdot 0.9106
$$
$$
E \approx \mathbf{1.611\text{ dB}}
$$
$$
L.I. = 18.2 - 1.611 = \mathbf{16.589\text{ dB}}
$$
$$
L.S. = 18.2 + 1.611 = \mathbf{19.811\text{ dB}}
$$
$$
IC_{98\%}(\mu) = [\mathbf{16.589\text{ dB}}, \; \mathbf{19.811\text{ dB}}]
$$

#### **4. Conclusión e Interpretación Técnica**
La atenuación media real de los 200 cables producidos ese día se encuentra entre 16.59 dB y 19.81 dB con un 98% de confianza.

---

### **Solución del Ejercicio 44**
#### **1. Extracción e Interpretación de Datos Directos**
- Muestra de $n = 12$ semanas:
  $$
  \{8, \; 12, \; 10, \; 14, \; 9, \; 11, \; 13, \; 10, \; 8, \; 15, \; 11, \; 9\}
  $$
- Suma: $\sum x_i = 130 \implies \bar{X} = \frac{130}{12} \approx \mathbf{10.833\text{ alertas}}$.
- Suma de cuadrados de desvíos: $\sum (x_i - 10.833)^2 \approx 57.667$.
- Cuasivarianza muestral insesgada:
  $$
  s^2 = \frac{57.667}{12 - 1} = \frac{57.667}{11} \approx \mathbf{5.2424}
  $$
  $$
  s = \sqrt{5.2424} \approx \mathbf{2.2896\text{ alertas}}
  $$

#### **2. Elección del Modelo: Student con $n - 1 = 11$ g.l.**
Nivel de significación: $\alpha = 0.01 \implies \text{Confianza } 99\%$:
$$
t_{0.005; \; 11} = \mathbf{3.106}
$$

#### **3. Desarrollo Matemático y Operaciones**
$$
E = t_{0.005; \; 11} \cdot \frac{s}{\sqrt{n}} = 3.106 \cdot \frac{2.2896}{\sqrt{12}}
$$
$$
E = 3.106 \cdot \frac{2.2896}{3.4641} = 3.106 \cdot 0.6609 \approx \mathbf{2.053\text{ alertas}}
$$
$$
L.I. = 10.833 - 2.053 = \mathbf{8.780\text{ alertas}}
$$
$$
L.S. = 10.833 + 2.053 = \mathbf{12.886\text{ alertas}}
$$
$$
IC_{99\%}(\mu) = [\mathbf{8.780\text{ alertas}}, \; \mathbf{12.886\text{ alertas}}]
$$

#### **4. Conclusión e Interpretación Técnica**
Con una significación del 1% (99% de confianza), la media poblacional de alertas bloqueadas semanalmente por el firewall perimetral se sitúa entre 8.78 y 12.89 incidentes.

---

### **Solución del Ejercicio 45**
#### **1. Extracción e Interpretación de Variables**
- Cartera corporativa total: $N = 400$ clientes.
- Muestra auditada: $n = 35$ clientes.
- Media muestral observada: $\bar{X} = 4.200$.
- Desviación estándar muestral: $s = 650$ *(es muestral $s$, surge del relevamiento)*.
- Fracción de muestreo: $\frac{n}{N} = \frac{35}{400} = 0.0875 > 0.05 \implies \text{requiere CPF}$.

#### **2. Elección del Modelo y Factores**
Al 95% de confianza ($z = 1.96$ por $n \ge 30$):
$$
\text{CPF} = \sqrt{\frac{400 - 35}{400 - 1}} = \sqrt{\frac{365}{399}} \approx \mathbf{0.9564}
$$

#### **3. Desarrollo Matemático y Operaciones**
$$
E = 1.96 \cdot \frac{650}{\sqrt{35}} \cdot 0.9564 = 1.96 \cdot 109.87 \cdot 0.9564 \approx \mathbf{206}
$$
$$
L.I. = 4.200 - 206 = \mathbf{\$3.994}
$$
$$
L.S. = 4.200 + 206 = \mathbf{\$4.406}
$$
$$
IC_{95\%}(\mu) = [\mathbf{3.994}, \; \mathbf{4.406}]
$$

#### **4. Conclusión e Interpretación Técnica**
La tarifa mensual media de toda la cartera corporativa se sitúa entre \$3.994 y \$4.406 con un 95% de confianza.

---

### **Solución del Ejercicio 46**
#### **1. Extracción e Interpretación de Variables**
- Especificación mínima requerida: $\mu \ge 65\text{ }^\circ\text{C}$.
- Muestra de prototipos ensayados: $n = 4$ conmutadores.
- Media muestral obtenida: $\bar{X} = 61.5\text{ }^\circ\text{C}$.
- Desviación muestral: $s = 1.5\text{ }^\circ\text{C}$.
- Nivel de riesgo del 5%: $\alpha = 0.05 \implies \text{Confianza } 95\%$.

#### **2. Elección del Modelo: Student con $n - 1 = 3$ g.l.**
$$
t_{0.025; \; 3} = \mathbf{3.182}
$$

#### **3. Desarrollo Matemático y Operaciones**
1. **Caso estándar (sin lote finito acotado):**
   $$
   E = 3.182 \cdot \frac{1.5}{\sqrt{4}} = 3.182 \cdot 0.75 \approx \mathbf{2.387\text{ }^\circ\text{C}}
   $$
   $$
   L.I. = 61.5 - 2.387 = \mathbf{59.113\text{ }^\circ\text{C}}
   $$
   $$
   L.S. = 61.5 + 2.387 = \mathbf{63.887\text{ }^\circ\text{C}}
   $$
   $$
   IC_{95\%}(\mu) = [\mathbf{59.113\text{ }^\circ\text{C}}, \; \mathbf{63.887\text{ }^\circ\text{C}}]
   $$

   **Dictamen técnico:**  
   El límite superior del intervalo es $63.887\text{ }^\circ\text{C}$, el cual se ubica estrictamente por debajo de los $65\text{ }^\circ\text{C}$ exigidos. Con un 95% de certeza, el lote **NO CUMPLE** con la especificación térmica y debe ser rechazado.

2. **Recálculo con lote piloto finito de $N = 25$:**
   $$
   \text{CPF} = \sqrt{\frac{25 - 4}{25 - 1}} = \sqrt{\frac{21}{24}} = \sqrt{0.875} \approx \mathbf{0.9354}
   $$
   $$
   E_{\text{fin}} = 2.387 \cdot 0.9354 \approx \mathbf{2.233\text{ }^\circ\text{C}}
   $$
   $$
   IC_{95\%}(\mu)_{\text{fin}} = [61.5 - 2.233, \; 61.5 + 2.233] = [\mathbf{59.267\text{ }^\circ\text{C}}, \; \mathbf{63.733\text{ }^\circ\text{C}}]
   $$
   Aún con el factor finito, el límite superior ($63.73\text{ }^\circ\text{C}$) no alcanza los $65\text{ }^\circ\text{C}$, ratificando el rechazo.

---
\newpage

---

## 📌 **SOLUCIONARIO: BLOQUE VII (EJERCICIOS 47 AL 50)**
### **Intervalos de Confianza para la Varianza y Desviación Estándar**

---

### **Solución del Ejercicio 47**
#### **1. Extracción e Interpretación de Variables**
- Muestra de envases: $n = 18$.
- Varianza muestral informada: $s^2 = 0.32\text{ litros}^2$.
- Nivel de confianza: $95\% \implies \alpha = 0.05$.
- Grados de libertad: $\nu = n - 1 = 18 - 1 = 17$.

#### **2. Elección del Modelo y Valores Críticos Chi-Cuadrado ($\chi^2_{17}$)**
La variable pivotal para la varianza es $\frac{(n-1)s^2}{\sigma^2} \sim \chi^2_{n-1}$.
Buscamos los percentiles en tabla Chi-Cuadrado con 17 grados de libertad:
$$
\chi^2_{\text{inf}} = \chi^2_{0.975; \; 17} = \mathbf{7.564}
$$
$$
\chi^2_{\text{sup}} = \chi^2_{0.025; \; 17} = \mathbf{30.191}
$$

#### **3. Desarrollo Matemático y Operaciones**
El intervalo de confianza para la varianza es:
$$
\left[ \frac{(n - 1) s^2}{\chi^2_{\text{sup}}}, \; \frac{(n - 1) s^2}{\chi^2_{\text{inf}}} \right]
$$
Numerador común:
$$
(n - 1) s^2 = 17 \cdot 0.32 = \mathbf{5.44}
$$
1. **Límite inferior:**
   $$
   \sigma^2_{\text{inf}} = \frac{5.44}{30.191} \approx \mathbf{0.1802\text{ litros}^2}
   $$
2. **Límite superior:**
   $$
   \sigma^2_{\text{sup}} = \frac{5.44}{7.564} \approx \mathbf{0.7192\text{ litros}^2}
   $$
$$
IC_{95\%}(\sigma^2) = [\mathbf{0.1802\text{ litros}^2}, \; \mathbf{0.7192\text{ litros}^2}]
$$

#### **4. Conclusión e Interpretación Técnica**
Con un 95% de confianza, la varianza del volumen de llenado de toda la producción automatizada se encuentra entre 0.1802 y 0.7192 litros² (desviación estándar entre 0.424 L y 0.848 L).

---

### **Solución del Ejercicio 48**
#### **1. Extracción e Interpretación de Variables**
- Muestra de piezas de titanio: $n = 25$ piezas.
- Desviación estándar muestral: $s = 18\text{ gramos} \implies s^2 = 324\text{ gramos}^2$.
- Grados de libertad: $\nu = 25 - 1 = 24$.
- Numerador común: $(n - 1) s^2 = 24 \cdot 324 = \mathbf{7.776}$.

#### **2. Desarrollo Matemático y Operaciones**
1. **Al 95% de confianza ($\alpha = 0.05$):**  
   Percentiles para 24 g.l.: $\chi^2_{\text{inf}} = 12.401, \quad \chi^2_{\text{sup}} = 39.364$.
   $$
   \sigma_{\text{inf}} = \sqrt{\frac{7.776}{39.364}} = \sqrt{197.54} \approx \mathbf{14.05\text{ g}}
   $$
   $$
   \sigma_{\text{sup}} = \sqrt{\frac{7.776}{12.401}} = \sqrt{627.05} \approx \mathbf{25.04\text{ g}}
   $$
   $$
   IC_{95\%}(\sigma) = [\mathbf{14.05\text{ g}}, \; \mathbf{25.04\text{ g}}]
   $$

2. **Al 99% de confianza ($\alpha = 0.01$):**  
   Percentiles para 24 g.l.: $\chi^2_{\text{inf}} = 9.886, \quad \chi^2_{\text{sup}} = 45.559$.
   $$
   \sigma_{\text{inf}} = \sqrt{\frac{7.776}{45.559}} = \sqrt{170.68} \approx \mathbf{13.06\text{ g}}
   $$
   $$
   \sigma_{\text{sup}} = \sqrt{\frac{7.776}{9.886}} = \sqrt{786.57} \approx \mathbf{28.05\text{ g}}
   $$
   $$
   IC_{99\%}(\sigma) = [\mathbf{13.06\text{ g}}, \; \mathbf{28.05\text{ g}}]
   $$

#### **4. Conclusión e Interpretación Técnica**
A mayor confianza (99% frente a 95%), la dispersión estimada se amplía, oscilando entre 13.06 g y 28.05 g de desviación en el peso de las piezas.

---

### **Solución del Ejercicio 49**
#### **1. Extracción e Interpretación de Datos Directos**
- Ensayos en probetas ($n = 7$ registros):
  $$
  \{410, \; 418, \; 405, \; 422, \; 415, \; 412, \; 408\}\text{ MPa}
  $$
- Media: $\bar{X} = \frac{2890}{7} \approx 412.857\text{ MPa}$.
- Suma de cuadrados de desvíos: $\sum (x_i - \bar{X})^2 = 208.857$.
- Cuasivarianza insesgada ($n - 1 = 6$ g.l.):
  $$
  s^2 = \frac{208.857}{6} \approx \mathbf{34.8095\text{ MPa}^2}
  $$
- Numerador: $(n - 1) s^2 = 6 \cdot 34.8095 = \mathbf{208.857}$.

#### **2. Elección del Modelo: Chi-Cuadrado con 6 g.l. al 95%**
$$
\chi^2_{\text{inf}} = \chi^2_{0.975; \; 6} = \mathbf{1.237}
$$
$$
\chi^2_{\text{sup}} = \chi^2_{0.025; \; 6} = \mathbf{14.449}
$$

#### **3. Desarrollo Matemático y Operaciones**
$$
\sigma^2_{\text{inf}} = \frac{208.857}{14.449} \approx \mathbf{14.455\text{ MPa}^2}
$$
$$
\sigma^2_{\text{sup}} = \frac{208.857}{1.237} \approx \mathbf{168.842\text{ MPa}^2}
$$
$$
IC_{95\%}(\sigma^2) = [\mathbf{14.455\text{ MPa}^2}, \; \mathbf{168.842\text{ MPa}^2}]
$$
*(En términos de desviación estándar: $[3.80\text{ MPa}, \; 12.99\text{ MPa}]$).*

#### **4. Conclusión e Interpretación Técnica**
Con un 95% de certidumbre, la varianza estructural de la resistencia a la tracción del compuesto de carbono se ubica entre 14.46 y 168.84 MPa².

---

### **Solución del Ejercicio 50**
#### **1. Extracción e Interpretación de Variables**
- Muestra de nodos de red: $n = 16$ nodos.
- Desviación estándar muestral: $s = 45\text{ ms} \implies s^2 = 2.025\text{ ms}^2$.
- Grados de libertad: $\nu = 16 - 1 = 15$.
- Numerador común: $(n - 1) s^2 = 15 \cdot 2.025 = \mathbf{30.375}$.

#### **2. Desarrollo Matemático y Operaciones**
1. **Al 90% de confianza ($\alpha = 0.10$):**  
   Percentiles para 15 g.l.: $\chi^2_{\text{inf}} = 7.261, \quad \chi^2_{\text{sup}} = 24.996$.
   $$
   \sigma_{\text{inf}} = \sqrt{\frac{30.375}{24.996}} = \sqrt{1.215.19} \approx \mathbf{34.86\text{ ms}}
   $$
   $$
   \sigma_{\text{sup}} = \sqrt{\frac{30.375}{7.261}} = \sqrt{4.183.31} \approx \mathbf{64.68\text{ ms}}
   $$
   $$
   IC_{90\%}(\sigma) = [\mathbf{34.86\text{ ms}}, \; \mathbf{64.68\text{ ms}}]
   $$

2. **Al 98% de confianza ($\alpha = 0.02$):**  
   Percentiles para 15 g.l.: $\chi^2_{\text{inf}} = 5.229, \quad \chi^2_{\text{sup}} = 30.578$.
   $$
   \sigma_{\text{inf}} = \sqrt{\frac{30.375}{30.578}} = \sqrt{993.36} \approx \mathbf{31.52\text{ ms}}
   $$
   $$
   \sigma_{\text{sup}} = \sqrt{\frac{30.375}{5.229}} = \sqrt{5.808.95} \approx \mathbf{76.22\text{ ms}}
   $$
   $$
   IC_{98\%}(\sigma) = [\mathbf{31.52\text{ ms}}, \; \mathbf{76.22\text{ ms}}]
   $$

#### **4. Conclusión e Interpretación Técnica**
La variabilidad temporal en la validación descentralizada de bloques criptográficos tiene una desviación estándar acotada entre 34.86 ms y 64.68 ms con un 90% de confianza, y entre 31.52 ms y 76.22 ms con un 98% de confianza.
