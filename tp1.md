# TP1: Introducción a la Web: Arquitectura y Protocolos





## 1. Introducción

### 1. ¿Cómo surgió el sistema de documentos distribuidos WWW?
Surgió como una solución para la gestión de la información general en el CERN (Organización Europea para la Investigación Nuclear). La necesidad principal era compartir y actualizar información científica entre múltiples investigadores distribuidos en diferentes institutos y universidades a nivel mundial, evitando la incompatibilidad entre los distintos sistemas informáticos de la época.

### 2. ¿En qué año se creó la WWW? ¿Quién la creó? ¿Cuál fue el propósito inicial?
Fue creada en el año 1989 por el físico británico Tim Berners-Lee. Su propósito inicial era crear un sistema de intercambio de hipertexto global que permitiera a los científicos compartir documentos, investigaciones y actualizaciones de manera rápida e interconectada.

### 3. ¿Sobre qué red funcionaba? ¿Cuáles fueron los componentes iniciales?
Funcionaba sobre la red global de Internet, utilizando la pila de protocolos TCP/IP existente. Los componentes iniciales fueron:

- **HTML (HyperText Markup Language):** Lenguaje de marcado para crear los documentos.
- **HTTP (Hypertext Transfer Protocol):** Protocolo de red para transferir los documentos.
- **WorldWideWeb:** El primer navegador web (que también funcionaba como editor).
- **httpd (HyperText Transfer Protocol daemon):** El primer servidor web.

### 4. Nombre y describa las distintas etapas de evolución en la web. Realice una cronología de tecnologías.
- **Web 1.0 (Web estática - Años 90):** Solo lectura. Documentos HTML planos entrelazados por hipervínculos con muy poca o nula interacción del usuario.  
  *Tecnologías:* HTML estático, HTTP, GIF.
- **Web 2.0 (Web social/colaborativa - 2004 en adelante):** Web de lectura y escritura. Auge de foros, blogs, wikis y redes sociales donde el contenido es generado por los usuarios.  
  *Tecnologías:* AJAX, JavaScript, PHP, MySQL, CSS avanzado.
- **Web 3.0 (Web semántica - 2010s):** Datos interconectados y comprensibles por máquinas. Mayor personalización y búsquedas inteligentes.  
  *Tecnologías:* RDF, OWL, Microformatos, HTML5, IA inicial.
- **Web 4.0 (Web ubicua - Actualidad):** Movilidad constante, Internet de las Cosas (IoT), asistentes virtuales predictivos e IA generativa integrada, con conexiones permanentes y procesamiento en la nube.

<!-- PAGEBREAK -->
### 5. ¿Qué es un Servidor WWW?
Es un software (y la infraestructura de hardware que lo aloja) encargado de atender las peticiones de los clientes (generalmente navegadores) utilizando el protocolo HTTP/HTTPS. Su función principal es procesar dichas peticiones, localizar o generar el recurso solicitado (documentos HTML, imágenes, JSON) y devolverlo al cliente.

### 6. ¿Qué es un cliente web? Explique detalladamente.
Un cliente web es una aplicación, como un navegador (Chrome, Firefox) o una herramienta de línea de comandos (cURL), que se ejecuta en el dispositivo del usuario final.

Actúa iniciando la comunicación: formula y envía una solicitud HTTP/HTTPS al servidor web especificando el recurso que requiere. Una vez que recibe la respuesta, el cliente web (en el caso de un navegador) interpreta el código (HTML, CSS, JavaScript) y lo renderiza visualmente en la pantalla para que el usuario pueda interactuar con él.

### 7. ¿Cómo está compuesto el sistema WWW actual?
Está compuesto por una arquitectura masiva y heterogénea que incluye:

- **Clientes:** Navegadores web y aplicaciones móviles.
- **Servidores Web:** Apache, Nginx, IIS, entre otros.
- **Servidores de Aplicaciones y Bases de Datos:** Encargados de procesar la lógica de negocio y almacenar información.
- **Infraestructura de Red:** Routers, switches y conexiones de fibra/radio.
- **Servidores DNS:** Para la resolución de nombres de dominio a direcciones IP.
- **Redes de Distribución de Contenido (CDN):** Para almacenamiento en caché global y reducción de latencia.
- **Protocolos Base:** Pila TCP/IP, HTTP/HTTPS, TLS/SSL.

### 8. Realice un diagrama de crecimiento de hosts conectados a Internet desde su inicio hasta la actualidad.
*(Descripción evolutiva del diagrama)*: El gráfico representa una curva de crecimiento exponencial a lo largo del tiempo:

- **1969-1980:** Crecimiento plano y casi nulo (solo cientos de hosts experimentales en ARPANET).
- **1990-2000:** Inicio de la curva ascendente pronunciada, pasando de cientos de miles a millones de hosts con la comercialización de la WWW.
- **2000-2010:** Crecimiento acelerado impulsado por la Web 2.0 y el surgimiento de los smartphones, alcanzando cientos de millones de hosts.
- **2010-Actualidad:** Curva masiva constante que supera los miles de millones de hosts, empujada por los dispositivos móviles y el Internet de las Cosas (IoT).

<!-- PAGEBREAK -->
### 9. Realice un diagrama conceptual de composición de la web. ¿Cuáles son los componentes de la WWW?
La web se compone conceptualmente de tres pilares fundamentales interconectados:

1. **URI / URL:** Sistema universal para identificar y localizar los recursos en la red.
2. **HTTP / HTTPS:** Protocolo de comunicación que establece las reglas de solicitud y transferencia de recursos.
3. **HTML y Recursos:** Formato estándar en el que se estructuran y presentan los documentos distribuidos (junto con imágenes, estilos y scripts).

### 10. ¿Cuál es la arquitectura del sistema distribuido de documentos?
Sigue principalmente una arquitectura **Cliente-Servidor**. Los documentos están distribuidos en servidores independientes en todo el mundo y los clientes los solicitan bajo demanda.

Actualmente, esta arquitectura ha evolucionado hacia un modelo de múltiples capas (n-tier), donde el servidor web delega el procesamiento a servidores de aplicación (lógica de negocio) y estos a su vez se comunican con servidores de bases de datos.

### 11. ¿Cómo funciona el sistema WWW?
1. El usuario ingresa una dirección (URL) o hace clic en un hipervínculo.
2. El cliente web consulta al servidor DNS para traducir el nombre de dominio a una dirección IP.
3. Se establece una conexión TCP/IP con el servidor en la IP obtenida.
4. El cliente envía una petición HTTP especificando el recurso solicitado.
5. El servidor web procesa la solicitud y responde enviando el archivo correspondiente o un código de estado/error.
6. El cliente web interpreta y renderiza el contenido en la pantalla.

---
<!-- PAGEBREAK -->

## 2. Tecnologías, Servidores y Clientes

### 12. ¿Qué es HTML? ¿De dónde proviene?
HTML (HyperText Markup Language) es el lenguaje de marcado estándar utilizado para estructurar y organizar el contenido en las páginas web. Proviene de SGML (Standard Generalized Markup Language), un estándar internacional previo y más complejo diseñado para la definición de lenguajes de marcado de documentos.

### 13. ¿A qué se le llama página web estática? ¿Y página dinámica? ¿Y página activa?
- **Página Estática:** Documento preconstruido que reside en el servidor y se envía al cliente exactamente como fue guardado (HTML puro). No requiere procesamiento en servidor ni interacción con bases de datos.
- **Página Dinámica:** El contenido no existe como un archivo fijo en disco, sino que es generado en tiempo real por el servidor (usando lenguajes como PHP, Node.js o Python) en respuesta a la solicitud del usuario, consultando habitualmente una base de datos.
- **Página Activa:** El documento se descarga al navegador cliente y, mediante scripts que se ejecutan localmente (como JavaScript), modifica su contenido, estructura o comportamiento en tiempo real según la interacción del usuario sin necesidad de recargar la página completa desde el servidor.

### 14. ¿Qué es una URL? ¿Qué función cumple en la Web? ¿Qué es un servidor de archivos basado en URL?
Una URL (Uniform Resource Locator) es la dirección específica asignada a un recurso en la red para su localización unívoca.

Un servidor de archivos basado en URL es un servidor web básico cuya función principal es mapear la ruta indicada en la URL directamente a una ruta física en su sistema de archivos local para servir documentos estáticos.

### 15. ¿Dónde y cómo se ejecuta el lenguaje HTML?
HTML no se ejecuta como un programa tradicional ya que no es un lenguaje de programación; en su lugar, se interpreta y renderiza. Este proceso ocurre en el lado del cliente, dentro del motor de renderizado del navegador web, que lee las etiquetas de marcado y construye la estructura visual del documento (árbol DOM).
<!-- PAGEBREAK -->

### 16. ¿Qué es un lenguaje script en la tecnología WWW?
Es un lenguaje de programación interpretado y ligero diseñado para automatizar tareas y añadir lógica a la web. 

Pueden ejecutarse en el lado del servidor (PHP, Python, Ruby) para generar contenido HTML dinámico, o en el lado del cliente (JavaScript) para brindar interactividad y manipular el DOM tras la carga del documento.

### 17. ¿Qué es un plugin? ¿Qué es una cookie?
- **Plugin:** Módulo de software adicional que se integra al navegador para extender sus capacidades por defecto (por ejemplo, reproducir formatos de video específicos o gestionar firmas digitales).
- **Cookie:** Pequeño archivo de datos enviado por el servidor web y almacenado en el navegador del usuario. El cliente lo reenvía en cada petición posterior al mismo servidor, permitiendo mantener sesiones, recordar preferencias e identificar usuarios.

### 18. Tecnologías clave: JavaScript, DHTML, XHTML y XML
- **JavaScript:** Lenguaje de programación interpretado, orientado a objetos y eventos. Se ejecuta principalmente en el motor JavaScript del navegador del cliente (y también en servidor mediante Node.js). Fue creado en 1995 por Brendan Eich en Netscape bajo el nombre de LiveScript.
- **DHTML (Dynamic HTML):** Término utilizado a finales de los años 90 para describir la combinación de HTML, CSS y JavaScript que permitía crear páginas interactivas y animadas.
- **XHTML (eXtensible HyperText Markup Language):** Redefinición del lenguaje HTML bajo las reglas estrictas de XML, exigiendo un código limpio con etiquetas cerradas y en minúsculas.
- **XML (eXtensible Markup Language):** Metalenguaje que permite definir lenguajes de marcado personalizados para almacenar y estructurar datos de forma legible tanto por humanos como por computadoras. A diferencia de HTML (enfocado en mostrar datos), XML se centra en describir y transportar datos.

### 19. ¿Qué son los Servicios Web? Dé un ejemplo de aplicación utilizando Servicios Web.
Los servicios web son sistemas de software diseñados para permitir la interacción interoperable máquina a máquina a través de una red, haciendo posible la comunicación entre aplicaciones desarrolladas en distintos lenguajes (mediante arquitecturas REST o SOAP).

*Ejemplo:* Una aplicación móvil universitaria (UADER) consulta los horarios de cursada de un alumno. La app (cliente) realiza una petición a un servicio web (API REST) del sistema académico (SIU Guaraní), enviando una solicitud JSON y recibiendo los datos actualizados para mostrarlos en pantalla.

---

## 3. URLs, Dominios y Direcciones

### 20. ¿Qué es una URL? ¿Qué función cumple en la web? ¿Cuál es la estructura de una URL?
Una URL identifica la ubicación exacta de un recurso en la web y el protocolo utilizado para acceder a él.

**Estructura genérica:**
```text
esquema://usuario:contraseña@host:puerto/ruta/al/recurso?cadena_de_consulta#fragmento
```

**Ejemplo de URL completa:**
```text
https://www.ejemplo.com:443/docs/index.html?id=10#seccion2
```

### 21. ¿Qué es un servidor de archivos basado en URL?
Es un servidor web que procesa peticiones HTTP asociando el segmento de ruta de la URL solicitada con la jerarquía de directorios de su disco local, devolviendo el archivo estático correspondiente.

### 22. ¿Cuál es el formato de una URL en IPv6?
Para evitar conflictos con los dos puntos (`:`) utilizados para indicar el puerto, las direcciones IPv6 en las URLs se deben encerrar obligatoriamente entre corchetes (`[ ]`).

**Ejemplo:**
```text
http://[2001:0db8:85a3:0000:0000:8a2e:0370:7334]:80/index.html
```

### 23. ¿Qué es un Dominio WWW? ¿Qué relación tiene con una URL?
Un dominio es un nombre mnemotécnico fácil de recordar (por ejemplo, `uader.edu.ar`) asociado a una dirección IP en Internet. En una URL, el dominio representa la sección del host que indica a qué servidor debe conectarse el cliente.

### 24. ¿Cuál es la función del DNS en la WEB?
El Sistema de Nombres de Dominio (DNS) funciona como la guía telefónica de Internet. Su función principal es traducir nombres de dominio legibles por las personas (`www.uader.edu.ar`) en direcciones IP numéricas (`190.220.10.15`) necesarias para establecer la conexión en la red.

---
<!-- PAGEBREAK -->

## 4. Protocolos Utilizados en la WWW

### 25. ¿Cuál es la relación entre HTML, HTTP y HTTPS?
- **HTML:** Lenguaje utilizado para estructurar y dar formato al contenido del documento.
- **HTTP:** Protocolo de red que establece las reglas de transferencia de los documentos HTML entre servidor y cliente.
- **HTTPS:** Versión segura de HTTP que añade una capa de cifrado (TLS/SSL) para proteger la confidencialidad e integridad de la información transmitida.

### 26. ¿Cuáles son las versiones de HTTP/HTTPS y cuáles sus diferencias?
Las versiones de HTTP y los protocolos de seguridad evolucionan de la siguiente manera:

**Evolución del protocolo HTTP:**
- **HTTP/1.1:** Transmisión en texto plano. Presenta bloqueo de cabeza de línea (*Head-of-line blocking*), donde una respuesta lenta detiene las subsecuentes.
- **HTTP/2:** Protocolo binario que introduce multiplexación (múltiples solicitudes simultáneas en una sola conexión TCP) y compresión de cabeceras.
- **HTTP/3:** Reemplaza TCP por QUIC (basado en UDP), reduciendo la latencia y mejorando el desempeño en redes inestables.

**Capa de cifrado TLS (HTTPS):**
- **TLS 1.2:** Estándar ampliamente adoptado, aunque con ciertos algoritmos antiguos desaconsejados.
- **TLS 1.3:** Versión actual más rápida y segura, que optimiza el proceso de negociación (*handshake*) y elimina cifrados obsoletos.

### 27. ¿Qué es MIME?
MIME (Multipurpose Internet Mail Extensions) es una especificación utilizada en HTTP para indicar la naturaleza y el formato de los datos transmitidos. El servidor incluye esta información en la cabecera `Content-Type` para que el navegador sepa cómo procesar el archivo.

*Ejemplos comunes:* `text/html`, `application/pdf`, `image/jpeg`, `application/json`.

<!-- PAGEBREAK -->

### 28. Explique cómo es una solicitud HTTP.
Una solicitud (Request) HTTP enviada por un cliente se compone de:

1. **Línea de petición (Request-Line):** Contiene el método HTTP, la URI del recurso y la versión del protocolo.
2. **Cabeceras (Headers):** Pares clave-valor con metadatos sobre la petición (Host, User-Agent, Accept, etc.).
3. **Línea en blanco:** Separador obligatorio que indica el fin de las cabeceras.
4. **Cuerpo del mensaje (Body):** Opcional, utilizado para enviar datos al servidor (por ejemplo en métodos POST o PUT).

```http
GET /index.html HTTP/1.1
Host: www.ejemplo.com
User-Agent: Mozilla/5.0
Accept: text/html
```

### 29. ¿Cuáles son los métodos de HTTP? Enumere y describa el funcionamiento de cada uno.
- **GET:** Solicita un recurso al servidor. Es un método seguro e idempotente (no altera el estado del servidor).
- **POST:** Envía datos al servidor para crear un nuevo recurso o procesar información de formularios.
- **PUT:** Crea o reemplaza completamente el recurso ubicado en la URL especificada.
- **PATCH:** Aplica modificaciones parciales a un recurso existente.
- **DELETE:** Solicita la eliminación del recurso especificado.
- **HEAD:** Similar a GET, pero solicita únicamente las cabeceras sin el cuerpo de la respuesta.
- **OPTIONS:** Consulta los métodos HTTP permitidos o soportados por el servidor para una URL dada.