---
coverConfig:
  showCover: false
  title: Resumen de BBDD
  subtitle: 'SQL, Vistas, Funciones y Triggers'
  materia: Bases de Datos
  coverStyle: blanca_simple
  showLogo: true
  integrantes: []
  profesores: []
  sigla: BBDD
  fecha: '2026'
  showHeader: false
  showFooter: true
  headerLeft: '{sigla} - {titulo}'
  headerCenter: ''
  headerRight: '{fecha}'
  headerShowLine: true
  footerLeft: '{materia}'
  footerCenter: ''
  footerRight: ''
  footerNumbering: pagina_x_de_y
  footerShowLine: true
activeTheme: minimal
---

# **Resumen de Base de Datos — SQL, Vistas, Funciones y Triggers**

---

## **1. Introducción al Lenguaje SQL**

### **1.1 Concepto, Origen y Evolución Histórica**

- **Definición formal:** SQL (==Structured Query Language==(celeste) o Lenguaje de Consulta Estructurado) es el lenguaje estándar utilizado para definir, consultar, manipular y controlar el acceso a bases de datos relacionales.
- **Origen y desarrollo inicial:**  
  Las bases conceptuales de los sistemas de bases de datos relacionales fueron introducidas por **Edgar F. Codd (E. F. Codd)** en **1970**. A partir de estos fundamentos, **IBM Research** desarrolló a mediados de la década de 1970 el primer prototipo experimental denominado **SYSTEM R**, dando origen al lenguaje ==SEQUEL==(naranja) (*Structured English Query Language*). Más tarde, el nombre se simplificó a **SQL** por razones de registro de marca.
- **Factor clave del éxito:** SQL se convirtió en el estándar universal gracias a su sintaxis declarativa (cercana al lenguaje humano), su portabilidad entre diferentes motores y su completa independencia de las estructuras físicas de almacenamiento en disco.

---

### **1.2 El Estándar SQL**

Con el surgimiento de múltiples sistemas administradores de bases de datos comerciales, se formalizó su estandarización para garantizar la portabilidad:

- **1986 (SQL-86 o SQL-1):** Primer estándar formal publicado por **ANSI** (*American National Standards Institute*) y adoptado por **ISO** (*International Organization for Standardization*).
- **1992 (SQL-92 o SQL-2):** Incorporó uniones avanzadas de tablas (`JOIN`), nuevas funciones y mayores restricciones de integridad.
- **1999 (SQL:1999 o SQL-3):** Agregó características procedimentales, tipos estructurados y soporte para triggers.
- **Portabilidad entre DBMS:** Permite migrar sentencias y esquemas entre diferentes sistemas gestores (PostgreSQL, MySQL, Oracle, SQL Server), aunque cada motor puede incorporar extensiones particulares o ciertas variaciones sintácticas.
- **Conexión con lenguajes de programación:** SQL se integra de forma directa con lenguajes de propósito general como **C++**, **Java**, **Python**, **C#**, entre otros, a través de drivers y librerías de conectividad.

---

### **1.3 Clasificación de Sublenguajes en SQL**

SQL se divide estructuralmente en dos grandes subsistemas complementarios:

- ==DDL (Data Definition Language — Lenguaje de Definición de Datos)==(celeste):
  - Conjunto de sentencias orientadas a **definir, modificar o eliminar la estructura del esquema** de la base de datos (bases de datos, tablas, columnas, índices y restricciones).
  - Comandos principales: `CREATE`, `DROP`, `ALTER`.

- ==DML (Data Manipulation Language — Lenguaje de Manipulación de Datos)==(rosa):
  - Conjunto de sentencias destinadas a **operar con los datos** almacenados en las tablas: consultar registros, insertar nuevas filas, actualizar campos y eliminar datos.
  - Comandos principales: `SELECT` (formalmente categorizado como DQL o lenguaje de consulta), `INSERT`, `UPDATE`, `DELETE`.

---

### **1.4 Estructura y Componentes de una Tabla en SQL**

En la teoría de bases de datos y en SQL existen equivalencias concretas para cada elemento que conforma una tabla:

| Concepto Teórico | Denominación en SQL | Descripción Operativa |
| :--- | :--- | :--- |
| **Relación** | ==Table (Tabla)==(celeste) | Estructura bidimensional en filas y columnas con nombre único. |
| **Atributo** | ==Column (Columna)==(amarillo) | Propiedad o campo con nombre que describe a la entidad. |
| **Tupla** | ==Fila / Registro / Row==(verde) | Instancia individual de datos concretos que conforma una fila. |
| **Dominio** | ==Tipo de Dato / Data Type==(naranja) | Conjunto válido de valores atómicos permitidos para una columna. |
| **Clave Primaria** | ==Primary Key (PK)==(rojo) | Atributo que identifica de manera única a cada fila de la tabla. |
| **Grado** | **Cantidad de Columnas** | Número total de atributos o columnas que componen la tabla. |
| **Cardinalidad** | **Cantidad de Filas** | Número total de registros o tuplas cargados actualmente en la tabla. |

#### **Representación Gráfica de una Tabla (Ejemplo de Clase — `Proveedor`):**

A continuación se representa la relación de proveedores utilizada en clase con sus dimensiones y elementos:

| P# ==[PK]==(rojo) | Proveedor (Nombre) | Status | Ciudad | Tupla / Registro |
| :---: | :--- | :---: | :--- | :---: |
| **1** | Nahuel | 20 | Bariloche | Fila 1 |
| **2** | SiderArgen | 10 | San Nicolás | Fila 2 |
| **3** | Autopartes Rubén | 30 | Gualeguaychú | Fila 3 |
| **4** | Frenos Litoral | 20 | C. del Uruguay | Fila 4 |
| **5** | Tecbolsa | 30 | Ciudad de Bs As | Fila 5 |

- ==Grado de la tabla==(celeste) $\mathbf{= 4}$: Representa el número total de columnas o atributos (`P#`, `Proveedor`, `Status`, `Ciudad`).
- ==Cardinalidad de la tabla==(verde) $\mathbf{= 5}$: Representa la cantidad total de filas o tuplas registradas actualmente.
- ==Clave Primaria (PK)==(rojo) $\mathbf{= P\#}$: Columna designada para asegurar que no existan tuplas duplicadas.
- ==Dominios==(amarillo): El tipo de dato y rango de valores permitidos para cada atributo (por ejemplo: `P#` y `Status` admiten enteros, mientras que `Proveedor` y `Ciudad` admiten cadenas de caracteres).

---

### **1.5 Tipos de Datos en SQL**

Los tipos de datos establecen el formato de almacenamiento y las operaciones válidas sobre cada columna:

1. **Numéricos:**
   - `INTEGER` / `INT`: Números enteros estándar con signo.
   - `SMALLINT`: Números enteros de menor rango (ahorro de espacio).
   - `FLOAT` / `REAL`: Números en punto flotante de precisión variable.
   - `DECIMAL(i, j)` / `NUMERIC(i, j)`: Números de precisión fija y exacta, donde $i$ es la cantidad total de dígitos y $j$ es la cantidad de decimales.
2. **Caracteres:**
   - `CHAR(n)`: Cadena de longitud fija de exactamente $n$ caracteres.
   - `VARCHAR(n)` / `CHARACTER VARYING(n)`: Cadena de longitud variable de hasta un máximo de $n$ caracteres.
   - `TEXT`: Cadena de texto de longitud variable sin límite estricto predefinido.
3. **Bits:**
   - `BIT(n)`: Cadena de bits de longitud fija.
   - `BIT VARYING(n)`: Cadena de bits de longitud variable.
4. **Booleanos:**
   - `BOOLEAN`: Admite los valores lógicos `TRUE`, `FALSE` o `NULL` (desconocido).
5. **Fechas y Horas:**
   - `DATE`: Fecha calendario (`AAAA-MM-DD`).
   - `TIME`: Hora del día (`HH:MM:SS`).
   - `TIME WITH TIME ZONE`: Hora incluyendo la zona horaria.
   - `TIMESTAMP`: Marca temporal completa combinando fecha y hora.

\newpage

---

## **2. DDL — Lenguaje de Definición de Datos**

Las sentencias DDL estructuran el catálogo de la base de datos, administrando la creación, modificación y eliminación de objetos.

### **2.1 Gestión de Bases de Datos (`DATABASE`)**

- **Crear una base de datos:**
  ```sql
  CREATE DATABASE nombredb;
  -- Ejemplo de cátedra:
  CREATE DATABASE facultad;
  ```
- **Borrar una base de datos:**
  ```sql
  DROP DATABASE nombredb;
  -- Ejemplo de cátedra:
  DROP DATABASE facultad;
  ```

---

### **2.2 Creación de Tablas (`CREATE TABLE`) y Restricciones de Integridad**

Define una nueva tabla especificando sus columnas, tipos de datos y ==restricciones de integridad==(verde):

```sql
CREATE TABLE alumno (
    dni       INTEGER NOT NULL,
    apellido  VARCHAR(30),
    nombres   VARCHAR(40),
    tipodni   CHAR NOT NULL,
    PRIMARY KEY (dni),
    FOREIGN KEY (tipodni) REFERENCES tipo(tipodni)
        ON DELETE RESTRICT 
        ON UPDATE CASCADE
);
```

#### **Desglose de Restricciones:**
- `NOT NULL`: Obliga a que la columna contenga siempre un valor (prohíbe nulos).
- `PRIMARY KEY (atributo)`: Establece la clave primaria de la tabla, asegurando unicidad y no nulidad.
- `FOREIGN KEY (atributo) REFERENCES tabla_padre(atributo_padre)`: Establece una clave foránea vinculando la columna con la clave primaria de otra tabla.
- **Acciones Referenciales:**
  - `ON DELETE RESTRICT`: **Impide** eliminar una fila en la tabla referenciada si existen registros hijos asociados en la tabla actual (evita dejar tuplas huérfanas).
  - `ON UPDATE CASCADE`: Si se actualiza el valor de la clave en la tabla padre, la modificación **se propaga automáticamente en cascada** a las filas hijas relacionadas.

---

### **2.3 Modificación y Eliminación de Tablas (`ALTER TABLE` y `DROP TABLE`)**

- **Eliminar una tabla:**
  ```sql
  DROP TABLE alumno;
  ```
  *(Borra completamente la tabla del catálogo junto con todos sus datos).*

- **Modificar la estructura de una tabla (`ALTER TABLE`):**
  Permite realizar cambios sobre las columnas sin tener que recrear la tabla:
  ```sql
  -- 1. Agregar una nueva columna:
  ALTER TABLE alumno ADD COLUMN mail VARCHAR(50);

  -- 2. Eliminar una columna existente:
  ALTER TABLE alumno DROP COLUMN nombre;

  -- 3. Modificar el tipo de dato de una columna:
  ALTER TABLE alumno ALTER COLUMN nombre TYPE VARCHAR(100);
  ```

\newpage

---

## **3. DML — Lenguaje de Manipulación de Datos**

Las sentencias DML permiten gestionar los datos cargados en las tablas.

### **3.1 Inserción de Datos (`INSERT INTO`)**

Agrega nuevos registros a una tabla:

```sql
INSERT INTO tabla (lista_de_atributos) 
VALUES (valores_para_cada_atributo);
```

- **Inserción con lista explícita de columnas:**
  ```sql
  INSERT INTO auto (id, marca, modelo, combustible, puertas) 
  VALUES (500, 'AUDI', 'A4', 'NAFTA', 4);
  ```
- **Inserción omitiendo la lista de atributos:**
  Si no se detallan las columnas, los valores deben suministrarse obligatoriamente en el mismo orden posicional en el que fueron creadas en el `CREATE TABLE`:
  ```sql
  INSERT INTO auto 
  VALUES (500, 'AUDI', 'A4', 'NAFTA', 4);
  ```

---

### **3.2 Modificación de Datos (`UPDATE`)**

Modifica los valores de una o más columnas en las filas que satisfagan una condición:

```sql
UPDATE tabla
SET atributo = nuevo_valor
WHERE condicion;
```

- **Ejemplo de cátedra:** Incrementar un 20% el precio de los artículos de perfumería:
  ```sql
  UPDATE producto
  SET precio = precio * 1.20
  WHERE tipo = 'PERFUMERIA';
  ```
- > [!CAUTION] **Advertencia de examen:**  
  > La cláusula `WHERE` es opcional, pero si se omite, la actualización afectará a **todas las filas de la tabla**.

---

### **3.3 Eliminación de Registros (`DELETE FROM`)**

Elimina una o más filas de una tabla:

```sql
DELETE FROM tabla WHERE condicion;
```

- **Ejemplo con condición:**
  ```sql
  DELETE FROM alumno WHERE idcarrera = 3;
  ```
- **Ejemplo sin condición `WHERE`:**
  ```sql
  DELETE FROM auto;
  ```
  - **Efecto de `DELETE FROM auto;`:**  
    Elimina **todas las filas** de la tabla `auto`.  
    *Diferencia con `DROP TABLE`:* `DELETE` vacía los registros pero **mantiene la estructura de la tabla intacta** en la base de datos; `DROP TABLE` destruye tanto los datos como la definición de la tabla en el catálogo.

\newpage

---

## **4. Consultas en SQL (DQL — Data Query Language)**

### **4.1 Estructura Básica de Consulta (`SELECT`)**

La sentencia medular para recuperar información de las tablas está compuesta por tres cláusulas fundamentales:

```sql
SELECT lista_de_atributos
FROM lista_de_tablas_o_subconsultas
WHERE condiciones;
```

- **Ejemplo elemental:**
  ```sql
  SELECT dni, apellido, nombre
  FROM estudiante
  WHERE dni > 30000000;
  ```
  *(La cláusula `WHERE` es opcional; si no se indica, la consulta devuelve las columnas seleccionadas de todas las tuplas).*

---

### **4.2 Opciones y Cláusulas Avanzadas del `SELECT`**

- **Proyección total (`*`):**  
  Devuelve todas las columnas definidas en la tabla:
  ```sql
  SELECT * FROM alumno;
  ```

- **Eliminación de duplicados (`DISTINCT` vs. `ALL`):**  
  Por defecto, `SELECT` opera en modo `ALL` (devuelve todas las filas aunque existan valores repetidos). Si se desea obtener únicamente filas con valores únicos descartando repeticiones, se utiliza `DISTINCT`:
  ```sql
  SELECT DISTINCT ciudad FROM cliente;
  ```

- **Renombrar columnas de salida y expresiones calculadas (`AS`):**  
  Define un alias para el encabezado del resultado.  
  *Punto clave de examen:* `AS` **NO** modifica el nombre de la columna en la tabla original, solo en la visualización de la consulta.
  ```sql
  SELECT dni AS documento, apell AS apellido, (sueldo * 1.10) AS aumento
  FROM empleado;
  ```

- **Alias de tablas en la cláusula `FROM`:**  
  Permite asignar un nombre abreviado a las tablas para simplificar la redacción y desambiguar columnas con el mismo nombre mediante `tabla.columna`:
  ```sql
  SELECT a.dni, a.apellido, m.nombre
  FROM alumno a, materia m, carrera c
  WHERE a.dni = m.dni_alumno AND m.id_carrera = c.id;
  ```

- **Condiciones y filtros en `WHERE`:**  
  Permite operadores de comparación (`=`, `<>`, `!=`, `<`, `<=`, `>`, `>=`) combinados con operadores lógicos (`AND`, `OR`, `NOT`):
  ```sql
  WHERE sueldo >= 5000 AND (departamento = 'VENTAS' OR departamento = 'SISTEMAS')
  ```

- **Filtro por rango inclusivo (`BETWEEN`):**  
  Selecciona valores comprendidos dentro de un intervalo cerrado $[v_1, v_2]$:
  ```sql
  SELECT apellido, nombre
  FROM empleado
  WHERE sueldo BETWEEN 10000 AND 15000;
  ```

- **Comparación de patrones de texto (`LIKE`):**  
  Se utiliza en la cláusula `WHERE` junto con caracteres comodín para filtrar cadenas de texto:
  - `%` (porcentaje): Representa **cualquier secuencia de caracteres de cualquier longitud** (cero o más caracteres).
  - `_` (guión bajo): Representa **exactamente una única posición de carácter**.

  **Ejemplos de aplicación vistos en clase:**
  ```sql
  -- 1. Nombres que comienzan con la letra 'D':
  SELECT * FROM personas WHERE nombre LIKE 'D%';

  -- 2. Nombres que contengan 'cor' en cualquier parte de la cadena:
  SELECT * FROM personas WHERE nombre LIKE '%cor%';

  -- 3. CUIT que empiece con 27 seguido de exactamente 9 caracteres:
  SELECT * FROM personas WHERE cuit LIKE '27_________';
  ```

- **Ordenamiento de resultados (`ORDER BY`):**  
  Ordena las filas del conjunto resultante:
  - `ASC`: Orden ascendente (es el criterio aplicado **por defecto**).
  - `DESC`: Orden descendente.
  ```sql
  SELECT dni, apellido, nombre, cp
  FROM estudiante
  WHERE cp = 3260
  ORDER BY apellido, nombre DESC;
  ```

---

### **4.3 Resolución de los Casos Prácticos de Clase**

A partir del siguiente esquema:
- `Usuario (dni, genero, apellido, nombre, cp)`
- `Ciudad (cp, nombre)`
- `Prestamo (dni, idlibro, fechaprestamo, fechadevolucion)`

#### **1. Listar los usuarios de Concordia:**
```sql
SELECT u.dni, u.apellido, u.nombre
FROM Usuario u, Ciudad c
WHERE u.cp = c.cp AND c.nombre = 'Concordia';
```

#### **2. Listar las usuarias que hayan retirado algún libro:**
```sql
SELECT DISTINCT u.dni, u.apellido, u.nombre
FROM Usuario u, Prestamo p
WHERE u.dni = p.dni AND u.genero = 'F';
```

#### **3. Listar los libros que no fueron devueltos:**
```sql
SELECT DISTINCT p.idlibro
FROM Prestamo p
WHERE p.fechadevolucion IS NULL;
```

\newpage

---

## **5. Funciones de Agregación y Agrupamiento**

### **5.1 Las 5 Funciones de Agregación Principales**

Procesan un conjunto de tuplas y devuelven un **único valor resumen**:

| Función de Agregación | Descripción | Tipos de Datos Admitidos | Comportamiento con Valores `NULL` |
| :--- | :--- | :--- | :--- |
| `MAX(columna)` | Devuelve el valor máximo registrado. | Numérico, Fecha, Carácter | Ignora los valores nulos |
| `MIN(columna)` | Devuelve el valor mínimo registrado. | Numérico, Fecha, Carácter | Ignora los valores nulos |
| `AVG(columna)` | Calcula el promedio aritmético. | Exclusivamente Numérico | Ignora los valores nulos |
| `SUM(columna)` | Calcula la sumatoria de los valores. | Exclusivamente Numérico | Ignora los valores nulos |
| `COUNT(columna)` | Cuenta las filas donde la columna no es nula. | Cualquier tipo | Ignora valores nulos en esa columna |
| `COUNT(*)` | Cuenta el **total absoluto de filas**. | Toda la fila | **Cuenta todas las tuplas**, tengan o no nulos |

#### **Ejemplos de Agregación de Clase:**
```sql
-- Máximo, mínimo, suma y promedio de sueldos de SISTEMAS:
SELECT MAX(sueldo), MIN(sueldo), SUM(sueldo), AVG(sueldo)
FROM empleado e, departamento d
WHERE e.dpto = d.dpto AND d.nombre = 'SISTEMAS';

-- Cantidad total de inscripciones realizadas en 2016:
SELECT COUNT(*)
FROM alumno a, inscripcion i
WHERE a.dni = i.dni AND i.anio = 2016;
```

---

### **5.2 Agrupamiento con `GROUP BY`**

Organiza las filas resultantes en grupos que comparten valores idénticos en columnas designadas, permitiendo calcular funciones de agregación por cada subgrupo:

```sql
SELECT departamento_id, COUNT(*), AVG(sueldo)
FROM empleado
GROUP BY departamento_id;
```

> [!IMPORTANT] **Regla obligatoria de `GROUP BY`:**  
> Cualquier columna que aparezca en el `SELECT` y **no forme parte de una función de agregación**, **DEBE** incluirse obligatoriamente en la cláusula `GROUP BY`.

---

### **5.3 Filtrado de Grupos (`HAVING`) vs. Filtrado de Filas (`WHERE`)**

- La cláusula ==WHERE==(amarillo) filtra **filas individuales ANTES** de que se agrupen los datos. **No puede contener funciones de agregación**.
- La cláusula ==HAVING==(verde) filtra **los grupos DESPUÉS** de haberse ejecutado el `GROUP BY`. Está diseñada específicamente para evaluar condiciones basadas en funciones de agregación.

```sql
-- Contar empleados por departamento sólo para departamentos donde el promedio salarial supere 15.000:
SELECT departamento.id, COUNT(*)
FROM empleado, departamento
WHERE empleado.dpto = departamento.id
GROUP BY departamento.id
HAVING AVG(sueldo) > 15000;
```

| Criterio Comparativo | Cláusula `WHERE` | Cláusula `HAVING` |
| :--- | :--- | :--- |
| **Ámbito de aplicación** | Filas o registros individuales | Grupos ya consolidados |
| **Momento de evaluación** | **Antes** de agrupar (`GROUP BY`) | **Después** de agrupar (`GROUP BY`) |
| **Uso de funciones de agregación** | **No permitido** (produce error de sintaxis) | **Permitido y necesario** (`AVG`, `COUNT`, `SUM`, etc.) |

\newpage

---

## **6. Vistas (Views)**

### **6.1 Concepto y Naturaleza de las Vistas**

- **Definición:** Una vista es un objeto de base de datos que encapsula una consulta `SELECT`.
- Se la define como una ==tabla virtual==(celeste): tiene filas y columnas accesibles como una tabla común, pero **no almacena los datos físicamente en disco por defecto**.
- **Ejecución dinámica:** Cada vez que una aplicación o usuario consulta la vista, el motor de la base de datos **ejecuta en tiempo real la sentencia `SELECT` subyacente** sobre las tablas base.
- **Transparencia:** Para quien realiza la consulta, la vista se utiliza con la misma sintaxis que una tabla normal (`SELECT * FROM vista`).

---

### **6.2 Las 3 Ventajas Fundamentales**

1. ==Simplificación de Consultas==(amarillo):  
   Oculta la complejidad de consultas extensas (con múltiples `JOIN`, cálculos o filtros complejos), permitiendo que el usuario acceda a la información con un simple `SELECT * FROM vista`.
2. ==Seguridad y Control de Acceso==(verde):  
   Permite conceder permisos sobre columnas o filas específicas de una vista sin otorgar acceso directo a toda la tabla base, protegiendo datos confidenciales (como sueldos o claves).
3. ==Mantenimiento Centralizado==(naranja):  
   Centraliza la lógica de negocio en la propia base de datos. Si la estructura interna de las tablas base cambia, solo se modifica la vista sin necesidad de reprogramar los sistemas clientes que la consumen.

---

### **6.3 Sintaxis y Ejemplo Práctico**

```sql
CREATE VIEW nombre_vista AS
SELECT atributo1, atributo2
FROM tabla
WHERE condicion = 1;
```

#### **Ejemplo de Aplicación:**
```sql
-- Creación de la vista para consultar alumnos aprobados:
CREATE VIEW vista_alumnos_aprobados AS
SELECT a.dni, a.apellido, a.nombres, c.nombre AS carrera
FROM alumno a
JOIN inscripcion i ON a.dni = i.dni
JOIN carrera c ON i.idcarrera = c.id
WHERE i.nota_final >= 6;

-- Uso de la vista como si fuera una tabla común:
SELECT * 
FROM vista_alumnos_aprobados 
WHERE carrera = 'Licenciatura en Sistemas';
```

\newpage

---

## **7. Funciones Definidas por el Usuario (UDF)**

### **7.1 Concepto y Propósito**

- **Definición:** Son bloques de código reutilizables almacenados en el servidor de base de datos que encapsulan lógica personalizada para realizar cálculos, consultas o modificaciones de datos.
- **Extensibilidad:** Extienden el lenguaje SQL estándar para resolver requerimientos de procesamiento complejos.
- **Ejecución en el servidor:** Al ejecutarse directamente donde residen físicamente los datos, se reduce notablemente el tráfico de red y la latencia entre las aplicaciones y la base de datos.

---

### **7.2 Ventajas Clave**

- **Desacoplamiento:** Al residir la lógica en el servidor, ante cualquier modificación de reglas de negocio no es necesario actualizar ni redistribuir los programas clientes.
- **Mayor eficiencia:** El motor optimiza y ejecuta la lógica de procesamiento en el servidor.
- **Menor tráfico de red:** Se envían únicamente los parámetros necesarios y el servidor responde con el resultado procesado.
- **Pre-compilación:** Las funciones se analizan y compilan previamente, almacenando su plan de ejecución en memoria para acelerar llamadas sucesivas.

---

### **7.3 Lenguajes Soportados en PostgreSQL**

1. ==SQL puro==(celeste): Indicado para encapsular consultas atómicas y cálculos directos sin estructuras de control complejas.
2. ==PL/pgSQL==(amarillo): Lenguaje procedural que incorpora declaración de variables locales, estructuras condicionales (`IF/THEN/ELSE`), bucles (`LOOP`, `FOR`, `WHILE`) y control de excepciones.
3. ==Lenguajes externos==(verde): Soporta lenguajes como **Python** (`PL/Python`), **C**, **Perl**, entre otros, según las extensiones habilitadas en el servidor.

---

### **7.4 Sintaxis y Estructura en PL/pgSQL**

#### **Estructura General del Bloque:**
```sql
CREATE [OR REPLACE] FUNCTION nombre_funcion(argumentos) 
RETURNS tipo_de_retorno 
AS $cuerpo$
DECLARE
    -- Declaración de variables locales
    variable tipo_dato;
BEGIN
    -- Cuerpo de la función con lógica procedural
    < logica de ejecucion >;
    
    RETURN { variable | valor };
END; 
$cuerpo$ 
LANGUAGE language_name;
```

- **Parámetros posicionales:** Si no se indican nombres para los parámetros en el encabezado, se accede a ellos dentro del cuerpo mediante ==`$1`, `$2`, ..., `$n`==(naranja).
- **Delimitadores `$$`:** El mecanismo de *dollar-quoting* permite encerrar el bloque de código sin tener que escapar las comillas simples internas.

---

### **7.5 Tipos de Retorno Soportados**

- **Tipos simples / escalares:** `INTEGER`, `VARCHAR`, `TEXT`, `REAL`, `NUMERIC(10,2)`, `BOOLEAN`, `DATE`.
- **Tipos compuestos:** Definidos previamente mediante `CREATE TYPE`.
- **Conjuntos de valores:** `RETURNS SETOF tipo_retorno`.
- **Tablas estructuradas:** `RETURNS TABLE (columna1 tipo1, columna2 tipo2, ...)` utilizando la sentencia `RETURN QUERY SELECT ...`.

---

### **7.6 Análisis de los Ejemplos de Clase**

#### **Ejemplo 1: Función Aritmética Simple (`addNumbers`)**
Toma dos parámetros enteros, los suma y retorna el valor escalar:
```sql
CREATE FUNCTION addNumbers(val1 integer, val2 integer) 
RETURNS integer 
AS $$
BEGIN
    RETURN val1 + val2;
END; 
$$ 
LANGUAGE plpgsql;

-- Invocación:
SELECT addNumbers(5, 6); -- Retorna: 11
```

#### **Ejemplo 2: Conteo con Variable Local (`get_stocks`)**
Dada una tabla de acciones `public."Stocks" (stock_id, stock_name, stock_price)`, calcula la cantidad de acciones cuyo precio es menor a un tope:
```sql
CREATE FUNCTION get_stocks(price_cap int) 
RETURNS int 
LANGUAGE plpgsql 
AS $$
DECLARE
    stock_count integer; -- Variable local
BEGIN
    SELECT count(*)
    INTO stock_count
    FROM public."Stocks"
    WHERE stock_price < price_cap;
    
    RETURN stock_count;
END; 
$$;

-- Invocación:
SELECT get_stocks(1000); -- Retorna: 3
```

#### **Ejemplo 3: Retorno de una Tabla Completa (`get_allStocks`)**
Retorna múltiples filas y columnas que cumplan la condición usando `RETURNS TABLE` y `RETURN QUERY`:
```sql
CREATE OR REPLACE FUNCTION get_allStocks(price_cap int) 
RETURNS TABLE (
    stock_serial_no int,
    stock varchar,
    price_of_stock bigint
) 
AS $$
BEGIN
    RETURN QUERY 
    SELECT stock_id, stock_name, stock_price
    FROM public."Stocks"
    WHERE stock_price < price_cap;
END; 
$$ 
LANGUAGE plpgsql;

-- Invocación:
SELECT get_allStocks(1000);
```

\newpage

---

## **8. Triggers (Disparadores)**

### **8.1 Concepto y Filosofía de los Triggers**

- **Definición formal:** Un ==TRIGGER==(celeste) o disparador es un procedimiento almacenado que se **ejecuta (dispara) de manera automática e implícita** ante una operación de modificación de datos (`INSERT`, `UPDATE` o `DELETE`) sobre una tabla determinada.
- **Función asociada:** Consiste en un bloque de código procedimental vinculado a una función disparadora.
- **Propósito fundamental:** Se utiliza para **comprobar la integridad de los datos**, forzar reglas de negocio complejas y asegurar que la base de datos quede en un **estado consistente al finalizar una transacción**.

---

### **8.2 Ventajas Principales**

- **Garantía absoluta de integridad:** Se ejecuta directamente en el motor, asegurando que ninguna aplicación ni usuario pueda evadir las restricciones de datos.
- **Ejecución garantizada:** Se activa en cada operación DML realizada sobre la tabla intervenida.
- **Facilidad de mantenimiento:** Si las políticas de negocio se modifican, basta con actualizar el trigger sin tocar las aplicaciones clientes.
- **Independencia de los datos:** Centraliza la lógica de control en la capa de datos.

---

### **8.3 Tuplas Virtuales: `NEW` y `OLD`**

Durante la ejecución de un trigger, el motor genera automáticamente dos ==tuplas virtuales==(naranja) para consultar los datos de la fila afectada:

- `NEW`: Contiene los valores de los atributos del **nuevo registro que se intenta insertar o modificar** (`INSERT` o `UPDATE`).
- `OLD`: Contiene los valores de los atributos **actualmente almacenados en la tabla** antes de ser modificados o eliminados (`UPDATE` o `DELETE`).
- **Acceso a atributos:** Se utiliza la notación de punto: `NEW.columna` u `OLD.columna`.

#### **Matriz de Disponibilidad de Tuplas Virtuales:**

| Operación DML | `OLD` (Valor previo) | `NEW` (Valor entrante) | Justificación Operativa |
| :--- | :---: | :---: | :--- |
| `INSERT` | **No disponible** (*NULL*) | **Disponible** | Es una fila nueva; no existe registro previo en la tabla. |
| `UPDATE` | **Disponible** | **Disponible** | `OLD` tiene los datos anteriores y `NEW` los nuevos valores propuestos. |
| `DELETE` | **Disponible** | **No disponible** (*NULL*) | Se elimina un registro existente (`OLD`); no se genera una fila nueva. |

---

### **8.4 Momento de Ejecución: `BEFORE` vs. `AFTER`**

Al declarar un disparador se debe establecer el momento temporal de disparo:

| Momento | Descripción | ¿Cuándo utilizarlo? |
| :--- | :--- | :--- |
| ==BEFORE==(amarillo) | Se dispara **ANTES** de que la operación (`INSERT`, `UPDATE`, `DELETE`) se aplique efectivamente sobre la tabla. | - Validar reglas de negocio y restricciones.<br>- Modificar o ajustar los datos entrantes de `NEW` antes de guardarlos.<br>- Abortar la operación lanzando excepciones (`RAISE EXCEPTION`). |
| ==AFTER==(verde) | Se dispara **DESPUÉS** de que la operación fue aplicada y validada sobre la tabla. | - Registrar logs en tablas de auditoría.<br>- Actualizar en cascada balances o tablas secundarias dependientes. |

---

### **8.5 Granularidad: `FOR EACH ROW`**

- `FOR EACH ROW`: El trigger se ejecuta **una vez por cada fila afectada** por la sentencia SQL. Permite acceder a las tuplas virtuales `NEW` y `OLD`.
- `FOR EACH STATEMENT`: El trigger se ejecuta **una sola vez por toda la sentencia**, con independencia de la cantidad de filas afectadas.

---

### **8.6 Creación en Dos Pasos en PostgreSQL**

En PostgreSQL, implementar un trigger requiere siempre dos pasos separados:

#### **Paso 1: Crear la Función Disparadora (Retorna `TRIGGER`)**
```sql
CREATE FUNCTION nombre_funcion() 
RETURNS TRIGGER 
AS $$
BEGIN
    -- Validaciones y sentencias
    RETURN NEW; -- (o RETURN OLD; en triggers de eliminación)
END;
$$ 
LANGUAGE plpgsql;
```

#### **Paso 2: Crear el Disparador Asociando Tabla y Función**
```sql
CREATE TRIGGER nombre_trigger
BEFORE INSERT ON tabla
FOR EACH ROW 
EXECUTE PROCEDURE nombre_funcion();
```

---

### **8.7 Caso Práctico Completo de Clase**

#### **Definición de la Tabla:**
```sql
CREATE TABLE emplea (
    dni       INT NOT NULL,
    apellido  CHARACTER VARYING(32),
    nombre    CHARACTER VARYING(25),
    fecNac    DATE,
    CONSTRAINT emplea_pkey PRIMARY KEY (dni)
);
```

#### **Reglas de Negocio a Implementar:**
1. El atributo `apellido` no puede ser nulo ni estar vacío.
2. El empleado debe ser estrictamente **mayor de 18 años** (calculado a partir de su fecha de nacimiento `fecNac`).

#### **Implementación de la Función Disparadora:**
```sql
CREATE OR REPLACE FUNCTION func_e() 
RETURNS TRIGGER 
AS $funcemp$
DECLARE
    edad SMALLINT;
BEGIN
    -- Cálculo de la edad con funciones nativas de PostgreSQL:
    edad := date_part('year', age(NEW.fecNac));
    
    -- Restricción 1: Apellido no nulo
    IF NEW.apellido IS NULL THEN
        RAISE EXCEPTION 'no puede tener apellido vacío';
    END IF;
    
    -- Restricción 2: Mayor de 18 años
    IF edad <= 18 THEN
        RAISE EXCEPTION 'no puede ser menor de 18 años';
    END IF;
    
    -- Si cumple las condiciones, autoriza la operación retornando la tupla:
    RETURN NEW;
END; 
$funcemp$ 
LANGUAGE plpgsql;
```

#### **Creación del Trigger:**
```sql
CREATE TRIGGER trigger_e
BEFORE INSERT OR UPDATE ON emplea
FOR EACH ROW 
EXECUTE PROCEDURE func_e();
```

#### **Pruebas de Validación:**

1. **Intento 1 — Empleado menor de edad:**
   ```sql
   INSERT INTO emplea VALUES ('11111111', 'GONZALEZ', 'JUAN', '2008-11-10');
   ```
   - **Resultado:** `ERROR: no puede ser menor de 18 años` *(Operación cancelada)*.

2. **Intento 2 — Apellido nulo:**
   ```sql
   INSERT INTO emplea VALUES ('11111111', NULL, 'JUAN', '1950-11-10');
   ```
   - **Resultado:** `ERROR: no puede tener apellido vacío` *(Operación cancelada)*.

3. **Intento 3 — Registro válido:**
   ```sql
   INSERT INTO emplea VALUES ('11111111', 'GONZALEZ', 'JUAN', '1978-11-10');
   ```
   - **Resultado:** `Query returned successfully: one row affected.` *(Inserción exitosa)*.

\newpage

---

## **9. Cuadros Comparativos y Resumen Rápido para el Parcial**

### **9.1 DDL vs. DML**

| Aspecto | DDL (Definición de Datos) | DML (Manipulación de Datos) |
| :--- | :--- | :--- |
| **Objetivo** | Definir o alterar el esquema y estructuras del catálogo | Operar sobre los datos y registros almacenados |
| **Comandos Principales** | `CREATE`, `ALTER`, `DROP`, `TRUNCATE` | `SELECT`, `INSERT`, `UPDATE`, `DELETE` |
| **Nivel de Afectación** | Estructuras de tablas, esquemas y vistas | Filas y registros de las tablas |

### **9.2 Cláusula `WHERE` vs. Cláusula `HAVING`**

| Criterio | `WHERE` | `HAVING` |
| :--- | :--- | :--- |
| **¿Sobre qué opera?** | Filas individuales de las tablas base | Grupos de registros consolidados |
| **Momento de filtrado** | Previo al agrupamiento (`GROUP BY`) | Posterior al agrupamiento (`GROUP BY`) |
| **Funciones agregadas** | No permite (`COUNT`, `AVG`, etc. dan error) | Diseñado específicamente para evaluar agregaciones |

\newpage

### **9.3 Vistas vs. Funciones vs. Triggers**

| Característica | Vista (`VIEW`) | Función (`FUNCTION`) | Trigger (`TRIGGER`) |
| :--- | :--- | :--- | :--- |
| **Invocación** | Explícita en `SELECT` (como tabla) | Explícita (`SELECT func()` o en expresiones) | **Implícita y automática** ante eventos DML |
| **Parámetros** | No recibe | Sí recibe argumentos de entrada | No recibe argumentos directos del usuario |
| **Lógica Procedural** | No (solo `SELECT` declarativo) | Sí (variables, condicionales, bucles PL/pgSQL) | Sí (implementada en su función asociada) |
| **Tuplas `NEW` / `OLD`** | No | No | **Sí** (valores entrantes y previos) |
| **Objetivo Principal** | Simplificar consultas y dar seguridad | Encapsular cálculos y reutilizar algoritmos | **Imponer integridad y validar reglas de negocio** |

### **9.4 Matriz de Tuplas `OLD` y `NEW` en Triggers**

| Operación DML | ¿Existe `OLD`? | ¿Existe `NEW`? | ¿Qué representa cada una? |
| :---: | :---: | :---: | :--- |
| `INSERT` | $\times$ (*NULL*) | $\checkmark$ | `NEW` contiene los datos de la fila a insertar. |
| `UPDATE` | $\checkmark$ | $\checkmark$ | `OLD` contiene la fila original; `NEW` la fila modificada. |
| `DELETE` | $\checkmark$ | $\times$ (*NULL*) | `OLD` contiene los datos de la fila eliminada. |

### **9.5 5 Puntos Clave "No Olvidar" para el Examen**

1. **`DELETE` sin `WHERE`:** Vacía la tabla eliminando todas sus tuplas, pero la estructura de la tabla se mantiene intacta en el catálogo (`DROP TABLE` elimina tanto los datos como la definición de la tabla).
2. **`SELECT DISTINCT`:** Por defecto SQL retorna todas las filas incluyendo duplicados (`ALL`); para filtrar filas repetidas y dejar solo valores únicos en el resultado debe especificarse explícitamente `DISTINCT`.
3. **`WHERE` vs. `HAVING`:** `WHERE` filtra filas individuales *antes* del agrupamiento y no admite funciones agregadas; `HAVING` filtra grupos consolidados *después* del `GROUP BY` y opera directamente sobre condiciones con funciones de agregación (`AVG`, `COUNT`, `SUM`, etc.).
4. **Comodines en `LIKE`:** `%` reemplaza cero o múltiples caracteres continuos; `_` reemplaza exactamente un único carácter posicional.
5. **Estructura de Triggers en PostgreSQL:** Siempre requiere crear primero una función con `RETURNS TRIGGER` escrita en `plpgsql`, y luego la sentencia `CREATE TRIGGER ... ON tabla FOR EACH ROW EXECUTE PROCEDURE nombre_funcion()`.
