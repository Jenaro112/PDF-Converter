# Resumen de Bases de Datos

# Resumen por temas

## Diseño Conceptual con UML

El diseño conceptual sirve como un auxiliar de alto nivel para identificar conceptos semánticos importantes, independientemente del Sistema Gestor de Bases de Datos (DBMS) que se utilice. Aunque el diagrama Entidad-Relación (E/R) es ampliamente difundido, el Diagrama de Clases de UML es una generalización que permite modelar tanto datos como comportamiento, facilitando la comunicación en todo el sistema.

**Estructura de una clase:** Se representa mediante una caja con tres divisiones: nombre de la clase, atributos y operaciones.  
**Propiedades y visibilidad:** Las clases abstractas se indican con fuente itálica. La visibilidad se define con prefijos: \`+\` (público), \`-\` (privado), \`\#\` (protegido). Las claves primarias se indican convencionalmente con la propiedad \`{OID}\` y las alternativas con \`{alternate OID}\`. El estereotipo \`\<\<persistent\>\>\` indica que la clase representa una estructura en la base de datos.  
**Relaciones:** Agregan semántica y definen la cardinalidad (ej. \`0..1\`, \`1\`, \`\*\`).  
*Asociación simple:* Relación estándar entre clases.  
*Agregación:* La parte tiene sentido sin el todo.  
*Composición:* La parte no tiene sentido sin el todo; indica una estructura subyacente fuerte.  
*Generalización:* Relación de herencia entre un supertipo y subtipos. Los subtipos sin atributos carecen de significado en la transformación relacional.  
**Clases de Asociación:** Cuando una relación muchos a muchos requiere almacenar historial o atributos propios (como la nota de un alumno en una materia cursada repetidas veces), la clase de asociación debe promoverse a una "Clase Completa" con existencia propia.  
**Relaciones N-arias:** Utilizadas para resolver problemas que las relaciones binarias no pueden, como especificar en qué equipo jugó un jugador en un campeonato específico. Se representan con un rombo.

## Modelo Relacional

Propuesto por Edgar Codd en 1970, basa la representación de datos en el concepto matemático de relación. Destaca por su sencillez, uniformidad, sólida fundamentación teórica e independencia de la interfaz.  
Consta de tres partes: estructura de datos, integridad de los datos y manipulación de los datos.  
**Propiedades de las relaciones:** No existen tuplas duplicadas, el orden de las tuplas y de los atributos no importa, y los atributos son siempre atómicos.

## Pasaje Lógico a Relacional

Transformación del diagrama conceptual a un esquema implementable.  
**Sintaxis base:** \`VAR BASE RELATION nombre (atributo1 dominio1, ... PRIMARY KEY(x))\`.  
**Reglas de correspondencia:**  
Relación 1:1 \--\> El campo clave de una tabla aparece en la otra.  
Relación 1:M \--\> El campo clave de la tabla (1) aparece en la tabla (M).  
Relación M:M o N-aria \--\> Se crea una nueva tabla (relación extra) que contiene los campos clave de las tablas involucradas.  
Agregación y Dependencia \--\> Se transforman de la misma manera que una asociación simple.

## Reglas de Codd

Restricciones que un DBMS debe cumplir para considerarse genuinamente relacional.  
**Regla 0 (Fundacional):** El DBMS debe manejar datos usando únicamente sus capacidades relacionales.  
**Regla 1 (Información):** Toda información debe representarse de una única forma: como valores en una tabla.  
**Regla 2 (Acceso Garantizado):** Todo dato atómico es accesible por la combinación de tabla, clave primaria y atributo.  
**Regla 3 (Valores Nulos):** Tratamiento sistemático de valores nulos (distintos de cero o espacios) para información faltante.  
**Regla 4 (Catálogo Dinámico):** La base de datos se describe lógicamente igual que los datos comunes, accesible vía el mismo lenguaje relacional.  
**Regla 5 (Sublenguaje Completo):** Debe existir al menos un lenguaje con sintaxis definida que soporte definición, manipulación, vistas, integridad, seguridad y transacciones.  
**Regla 6 (Actualización de vistas):** Toda vista teóricamente actualizable debe ser actualizable por el sistema.  
**Regla 7 (Operaciones de alto nivel):** Inserción, modificación y eliminación se aplican a conjuntos (relaciones), no solo a registros individuales.  
**Reglas 8, 9 y 10:** Independencia física de datos, independencia lógica de datos e independencia de integridad (almacenada en el catálogo, no en aplicaciones).  
**Regla 11 (Distribución):** Transparencia de localización, fragmentación y replicación.  
**Regla 12 (No subversión):** Lenguajes de bajo nivel no pueden evadir reglas de integridad del lenguaje de alto nivel.

## Dependencias Funcionales y Anomalías

El nivel de implementación evalúa cómo se almacenan las tuplas. Un mal diseño genera anomalías estructurales.  
**Anomalías de Inserción:** Incapacidad de almacenar hechos si faltan datos de otras entidades (ej. registrar un alumno sin que tenga una nota en una materia).  
**Anomalías de Modificación:** Datos redundantes generan inconsistencias al actualizar (ej. dos teléfonos distintos para el mismo DNI en distintas filas).  
**Anomalías de Eliminación:** Borrar un dato implica la pérdida involuntaria de información esencial (ej. al borrar una cursada se borran los datos personales del alumno).

**Dependencia Funcional (DF):** Restricción semántica. \`X \--\> Y\` indica que para cada valor de X existe un único valor de Y asociado. Son válidas en todo momento.  
**Clausura de dependencias:** Derivación lógicas calculadas mediante los Axiomas de Armstrong.  
**Conjunto Irreducible de DFs:** Un conjunto equivalente simplificado donde: 1\) El dependiente involucra un solo atributo. 2\) El determinante es irreducible a izquierda. 3\) Ninguna DF es redundante.

## Normalización

Proceso de descomposición sin pérdida (usando el álgebra relacional, específicamente el \*join\* y proyecciones dictadas por el Teorema de Heath).  
**Objetivos:** Minimizar redundancia, conservar información, conservar dependencias y eliminar anomalías.

# 

# Conceptos clave para estudiar

**Variable relacional vs. Relación:** La *variable relacional* es la estructura (el encabezado o esquema), mientras que la *relación* es el valor específico o instancia de datos en un momento dado (el cuerpo).  
**Tupla:** Fila de la tabla.  
**Atributo:** Columna de la tabla.  
**Grado:** Número de atributos de la relación.  
**Cardinalidad:** Número de tuplas de la relación.  
**Dominio:** Tipo de dato (definido por el sistema o usuario).  
**Tipos de Claves:**  
*Candidata:* Conjunto único y minimal de atributos.  
*Primaria:* Clave candidata elegida por el diseñador.  
*Alternativa:* Clave candidata no seleccionada como primaria.  
*Foránea (Relacional):* Referencia a una clave primaria en otra relación, bajo regla estricta de integridad referencial (no nulos sin concordancia).  
**Axiomas de Armstrong:** Herramientas de inferencia para DFs.  
*Básicos:* Reflexibilidad, Aumentación, Transitividad.  
*Derivados:* Autodeterminación, Descomposición, Unión, Composición, Pseudotransitividad.

# 

# Relaciones y dependencias

Las dependencias determinan la estructura de los esquemas. Según la teoría, "Y depende funcionalmente de X si para cada valor de X solo existe un posible valor de Y".

**Dependencia Trivial:** \`X \--\> Y\` (cuando Y es un subconjunto de X).  
**Ejemplo Estructural General:** \`Clave\_Primaria \--\> Atributo\_No\_Clave\`.

**Dependencias Funcionales Extraídas del Ejemplo "CURSA"**:  
\`Legajo, Materia \--\> Nota\`  
\`Legajo \--\> Nombre, CP, Localidad\`  
\`CP \--\> Localidad\`

**Dependencias Funcionales Extraídas del Ejemplo "FACTURA"**:  
\`nro\_factura, sucursal \--\> fecha, forma\_pago, cod\_cliente, total\`  
\`cod\_cliente \--\> nombre\_cliente\`  
\`cod\_articulo \--\> nombre\_articulo, precio\_unitario\`  
\`nro\_factura, sucursal, cod\_articulo \--\> cantidad, subtotal\`

# 

# Normalización

Proceso paso a paso guiado por las dependencias funcionales y el Teorema de Heath.

## Primera Forma Normal (1FN)

**Regla:** Una relación está en 1FN si cada valor válido contiene exactamente un valor atómico para cada atributo.  
**Qué se elimina:** Grupos repetitivos y campos multivaluados.

## Segunda Forma Normal (2FN)

**Regla:** Está en 1FN y todos los atributos que no son clave dependen *irreduciblemente* (completamente) de las claves candidatas.  
**Qué se elimina:** Dependencias parciales. Se aplica el Teorema de Heath sobre las flechas que salen "desde adentro" de una clave compuesta.  
**Esquema de transformación (Ejemplo CURSA):**  
*Problema:* \`Legajo, Materia \--\> Nombre, CP, Localidad\` (Dependencia parcial de Legajo).  
*Solución:* Descomponer en dos esquemas:  
Esquema A: \`\[Legajo, Materia\] \--\> Nota\`  
Esquema B: \`\[Legajo\] \--\> Nombre, CP, Localidad\`

## Tercera Forma Normal (3FN)

**Regla:** Está en 2FN y todos los atributos no clave dependen en forma *no transitiva* de la clave candidata.  
**Qué se elimina:** Dependencias transitivas (flechas que no salen de una clave primaria).  
**Esquema de transformación (Ejemplo ALUMNO derivado de CURSA):**  
*Problema:* \`Legajo \--\> CP\` y \`CP \--\> Localidad\` (Localidad depende transitivamente de Legajo).  
*Solución:* Aplicar Teorema de Heath aislando la DF problemática:  
Esquema A: \`\[Legajo\] \--\> Nombre, CP\`  
Esquema B: \`\[CP\] \--\> Localidad\`  
