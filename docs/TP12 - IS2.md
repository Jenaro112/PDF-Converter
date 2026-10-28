---
coverConfig:
  showCover: true
  title: Trabajo práctico 12
  subtitle: Sistemas Embebidos
  materia: Ingeniería de Software 2
  coverStyle: fcyt_uader
  showLogo: true
  integrantes:
    - Calivari, Lucas
    - Colazo, Ana Lucía
    - Mas Duarte, María Melina
    - Rodríguez, Lucas
  profesores:
    - Pedro Colla
  sigla: IS2
  fecha: '2026'
  showHeader: false
  showFooter: true
  footerLeft: '{materia}'
  footerNumbering: pagina_x_de_y
  footerShowLine: true
activeTheme: minimal
---

# TP12 Sistemas Embebidos

> [!NOTE]
> **Entorno de simulación:** Utilice el ambiente emulador de Arduino Uno provisto por TinkerCad para evaluar el hardware y el software a desarrollar en este práctico.

---

## Enunciado y Consignas

1. **Construir un circuito** compuesto por un resistor potenciómetro y un pulsador (*pushbutton* físico). Cuando se presione el *push button* en el circuito se leerá en forma analógica el valor de tensión en el potenciómetro. Cuando la tensión en el potenciómetro sea la mitad que la de la fuente o menor:
   - **a.** Se encenderá el LED incorporado en la placa Arduino Uno permanente.
   - **b.** Se exhibirá el valor leído en la consola serie.  
   *Caso contrario:* se apagará el LED "onboard" y el LED incorporado a la placa seguirá parpadeando. Al finalizar la lectura se esperará 500 mSeg y se repetirá el ciclo.  
   *(Se utilizará como referencia el sketch de firmware `is2_taller_sistemas_embebidos.ino`)*.

   > 📷 **[PEGAR AQUÍ CAPTURA 1: Circuito esquemático de referencia de la consigna (Arduino Uno + Protoboard en TinkerCAD)]**
   >
   > *Ejemplo: `![Esquema Circuito Consigna](/images/tu-captura-1.png)`*

2. **Implemente en la plataforma evaluador** y realice el test correspondiente para verificar que el circuito se comporta de acuerdo a la especificación.

3. **Descargar e instalar el Ambiente Integrado de Desarrollo (IDE)** correspondiente a la plataforma Arduino. El mismo puede obtenerse en la URL [https://www.arduino.cc/en/software](https://www.arduino.cc/en/software) donde se deberá seleccionar el *build* correspondiente al sistema operativo y versión que disponga.

4. **Cargue el programa** utilizado para la emulación en plataforma TinkerCad (así como todas las modificaciones que le hubiera hecho para que funcionare).

5. **Compile el programa** y luego de asegurar que se lo hace en forma exitosa copie el objeto resultante a la memoria flash de la placa que esté utilizando.  
   *Observe para comprobar el resultado que luego de hacerlo y reciclar la energía de la placa (cortar su energía y restituirla) el LED que está presente en la placa parpadea.*

6. **Realice las siguientes modificaciones en el firmware** y realice el correspondiente test de resultado:
   - **a.** Modifique el programa para que el ritmo de parpadeo sea una vez cada 5 segundos, repita el procedimiento de compilación, carga en la placa y verificación anterior.
   - **b.** Modifique para que el parpadeo ocurra cada 1 segundo.
   - **c.** Modifique el límite para que el mecanismo se active si la tensión medida en el potenciómetro alcanza el 25% de la tensión total.

---

## Resolución

### 1. Diseño y Simulación en TinkerCAD

Se llevó a cabo la implementación del sketch de firmware `is2_taller_sistemas_embebidos.ino` en TinkerCAD con todas las especificaciones:

> 📷 **[PEGAR AQUÍ CAPTURA 2: Simulación y conexionado del circuito en TinkerCAD]**
>
> *Ejemplo: `![Circuito TinkerCAD](/images/tu-captura-2.png)`*

Se generó el siguiente código para verificar que el potenciómetro leía correctamente los valores y los enviaba al monitor serie de forma fluida, mientras el LED integrado parpadea cada 500 milisegundos:

```cpp
const int pinPulsador = 2;
const int pinPotenciometro = A0;

void setup() {
  pinMode(pinPulsador, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600); // Inicializa la comunicación serie
}

void loop() {
  int valorPot = analogRead(pinPotenciometro); // Lee el potenciómetro
  Serial.print("Valor del potenciometro: ");
  Serial.println(valorPot); // Imprime el valor en la consola

  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
}
```

Se ejecutó el test correspondiente para verificar que el circuito se comporta de acuerdo a la especificación:

> 📷 **[PEGAR AQUÍ CAPTURA 3: Monitor en serie en TinkerCAD con las lecturas analógicas del potenciómetro]**
>
> *Ejemplo: `![Monitor Serie TinkerCAD](/images/tu-captura-3.png)`*

---

### 2. Implementación en Entorno de Desarrollo (Arduino IDE)

Se cargó en Arduino IDE el programa utilizado para la emulación en plataforma TinkerCad y se compiló el programa para asegurar que lo hace en forma exitosa.

> 📷 **[PEGAR AQUÍ CAPTURA 4: Compilación exitosa en Arduino IDE con uso de memoria y flash]**
>
> *Ejemplo: `![Compilación en Arduino IDE](/images/tu-captura-4.png)`*

---

### 3. Modificaciones y Pruebas (Incisos a, b y c)

Para dar cumplimiento a las modificaciones del firmware requeridas en los incisos **a**, **b** y **c**, se refactorizó el código introduciendo constantes de control parametrizadas (`UMBRAL_PCT` y `PERIODO_PARPADEO`), lo que permitió adaptar la lógica del sistema embebido sin alterar la estructura base.

En primer lugar, para los incisos **a** y **b**, se modificó el valor de `PERIODO_PARPADEO` a **5000 ms** y **1000 ms** respectivamente, dividiendo dicho período de forma simétrica en la función auxiliar `parpadear()` para regular el ritmo de parpadeo del LED integrado (`LED_BUILTIN`) a una vez cada 5 segundos o cada 1 segundo.

En segundo lugar, para el inciso **c**, se estableció la constante `UMBRAL_PCT` en **25**, aplicando una fórmula de cálculo dinámico:

$$ \text{UMBRAL} = \frac{(\text{long})\text{ADC\_MAX} \times \text{UMBRAL\_PCT}}{100} $$

Esta fórmula traduce porcentajes a lecturas del conversor analógico-digital (ADC), configurando el umbral de activación permanente del LED en un cuarto de la tensión total de la fuente (equivalente a **255 sobre 1023**).

#### Código Refactorizado:

```cpp
const int pinPulsador = 2;          // Pin digital del pulsador (pull-up externo 10k: presionado = LOW)
const int pinPotenciometro = A0;   // Pin analógico del potenciómetro

// --- Parámetros de cada inciso (cambiar solo estos valores) ---
// Versión base: UMBRAL_PCT 50 y PERIODO_PARPADEO 1000
// Inciso 6a:    PERIODO_PARPADEO 5000  (un parpadeo cada 5 s)
// Inciso 6b:    PERIODO_PARPADEO 1000  (un parpadeo cada 1 s)
// Inciso 6c:    UMBRAL_PCT 25          (se activa con el 25% de la tensión)
const int UMBRAL_PCT = 25;
const long PERIODO_PARPADEO = 1000; // Período completo encendido + apagado (ms)

const int ADC_MAX = 1023;                                  // Lectura máxima del ADC (5V)
const int UMBRAL = (long)ADC_MAX * UMBRAL_PCT / 100;       // 25% -> 255 / 50% -> 511
const int ESPERA_LECTURA = 500;                            // Espera al finalizar la lectura (ms)

void setup() {
  pinMode(pinPulsador, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);                  // Inicializa la consola serie
  Serial.println("Kernel Arduino inicializando");
}

void loop() {
  int estadoBoton = digitalRead(pinPulsador);

  // Con resistencia pull-up, el pulsador presionado se lee como LOW
  if (estadoBoton == LOW) {
    int valorPot = analogRead(pinPotenciometro); // Lee el valor (0 a 1023)

    if (valorPot <= UMBRAL) {
      digitalWrite(LED_BUILTIN, HIGH);           // Encendido permanente
      Serial.print("Potenciometro <= ");
      Serial.print(UMBRAL_PCT);
      Serial.print("% (Valor: ");
      Serial.print(valorPot);
      Serial.println(")");
      delay(ESPERA_LECTURA);                     // Espera 500 ms y repite el ciclo
      return;
    }
  }

  parpadear(); // Botón suelto o tensión por encima del umbral
}

// Un ciclo completo de parpadeo del LED onboard
void parpadear() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(PERIODO_PARPADEO / 2);
  digitalWrite(LED_BUILTIN, LOW);
  delay(PERIODO_PARPADEO / 2);
}
```

> 📷 **[PEGAR AQUÍ CAPTURA 5: Salida del Monitor en Serie ("Kernel Arduino inicializando" y lecturas de test)]**
>
> *Ejemplo: `![Salida Monitor Serie Arduino](/images/tu-captura-5.png)`*
