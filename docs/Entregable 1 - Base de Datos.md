---
coverConfig:
  showCover: false
  title: Normalización a 3FN - Sistema de Justicia
  subtitle: 'Modelo Relacional y Formas Normales'
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

# Normalización a 3FN - Sistema de Justicia

## 1. Punto de partida

El modelo original proviene de un diagrama de clases compuesto por 15 elementos: **10 clases** (`Persona`, `Acusado`, `CausaJudicial`, `Secretaria`, `Fiscalia`, `Condena`, `CambioCondena`, `Domicilio`, `UnidadCarcelaria`, `PropiedadDomicilio`, `RelacionFamiliar`) y **5 enumeraciones** (`EstadoCivil`, `NivelEducacion`, `TipoParentesco`, `EstadoAcusado`, `TipoCambioCondena`).

### 1.1 Modelo relacional antes de la normalización

A partir de la transformación directa del diagrama de clases a relaciones, se obtiene el siguiente esquema relacional base:

```sql
VAR BASE RELATION Persona(
  dni varchar(20),
  nombres varchar(100),
  apellidos varchar(100),
  fechaNacimiento date,
  edad int,
  nacionalidad varchar(50),
  estadoCivil varchar(20),
  nivelEducacion varchar(20),
  profesion varchar(100),
  PRIMARY KEY (dni)
);
```

```sql
VAR BASE RELATION CausaJudicial(
  numeroInternoRegistro varchar(50),
  nombreJuez varchar(100),
  nombreSecretario varchar(100),
  fechaAlta date,
  fechaResolucion date,
  PRIMARY KEY (numeroInternoRegistro),
  FOREIGN KEY (nombreSecretario)
    REFERENCES Secretaria(nombre)
);
```

```sql
VAR BASE RELATION Domicilio(
  id varchar(20),
  direccion varchar(200),
  PRIMARY KEY (id)
);
```

```sql
VAR BASE RELATION Fiscalia(
  id varchar(20),
  nombre varchar(100),
  PRIMARY KEY (id)
);
```

```sql
VAR BASE RELATION Secretaria(
  id varchar(20),
  nombre varchar(100),
  PRIMARY KEY (id)
);
```

```sql
VAR BASE RELATION Acusado(
  id varchar(20),
  estadoActual varchar(20),
  dni varchar(20),
  numeroInternoRegistro varchar(50),
  PRIMARY KEY (id),
  FOREIGN KEY (dni)
    REFERENCES Persona(dni),
  FOREIGN KEY (numeroInternoRegistro)
    REFERENCES CausaJudicial(numeroInternoRegistro)
);
```

```sql
VAR BASE RELATION Condena(
  id varchar(20),
  fechaInicio date,
  duracionMeses int,
  fechaFinEstimada date,
  esPrisionDomiciliaria boolean,
  fechaBajaLibertad date,
  acusado_id varchar(20),
  unidadCarcelaria_id varchar(20),
  domicilio_id varchar(20),
  PRIMARY KEY (id),
  FOREIGN KEY (acusado_id)
    REFERENCES Acusado(id),
  FOREIGN KEY (unidadCarcelaria_id)
    REFERENCES UnidadCarcelaria(id),
  FOREIGN KEY (domicilio_id)
    REFERENCES Domicilio(id)
);
```

```sql
VAR BASE RELATION CambioCondena(
  id varchar(20),
  fechaCambio date,
  tipoCambio varchar(30),
  razon varchar(200),
  condena_id varchar(20),
  PRIMARY KEY (id),
  FOREIGN KEY (condena_id)
    REFERENCES Condena(id)
);
```

```sql
VAR BASE RELATION UnidadCarcelaria(
  id varchar(20),
  nombre varchar(100),
  domicilio_id varchar(20),
  PRIMARY KEY (id),
  FOREIGN KEY (domicilio_id)
    REFERENCES Domicilio(id)
);
```

```sql
VAR BASE RELATION PropiedadDomicilio(
  persona_dni varchar(20),
  domicilio_id varchar(20),
  fechaDesde date,
  fechaHasta date,
  esPrincipal boolean,
  PRIMARY KEY (persona_dni, domicilio_id, fechaDesde),
  FOREIGN KEY (persona_dni)
    REFERENCES Persona(dni),
  FOREIGN KEY (domicilio_id)
    REFERENCES Domicilio(id)
);
```

```sql
VAR BASE RELATION RelacionFamiliar(
  persona_dni varchar(20),
  familiar_dni varchar(20),
  tipo varchar(20),
  PRIMARY KEY (persona_dni, familiar_dni),
  FOREIGN KEY (persona_dni)
    REFERENCES Persona(dni),
  FOREIGN KEY (familiar_dni)
    REFERENCES Persona(dni)
);
```

### 1.2 Diagnóstico inicial de formas normales

| Forma normal | ¿Se cumplía en el original? | ¿Se aplicó algo? |
| :---: | :---: | :---: |
| **1FN** | Sí | No |
| **2FN** | Sí | No |
| **3FN** | No | Sí |

## 2. Primera Forma Normal (1FN)

**Regla:** todos los atributos deben ser atómicos (un solo valor por celda), no puede haber grupos repetidos ni listas dentro de una columna, y cada fila debe poder identificarse con una clave unívoca.

**Estado del diagrama original: ya cumple la 1FN, por eso no se aplica ninguna transformación.**

### 2.1 Verificación

- **Atributos atómicos:** `dni`, `nombres`, `apellidos`, `fechaNacimiento`, `direccion`, `duracionMeses`, etc. guardan un único valor cada uno. Ninguno guarda listas ni estructuras compuestas.
- **Sin grupos repetidos:** los datos que podrían repetirse (varios familiares, varios domicilios, varios cambios de condena) ya están modelados como clases separadas (`RelacionFamiliar`, `PropiedadDomicilio`, `CambioCondena`) y no como columnas `familiar1`, `familiar2`, etc.
- **Identificación de filas:** cada clase tiene un identificador propio (`id`, `dni` o `numeroInternoRegistro`). Las dos excepciones, `RelacionFamiliar` y `PropiedadDomicilio`, son tablas asociativas cuya clave se define al pasar a relacional (ver 2FN).

**Resultado:** sin cambios. El modelo cumple la 1FN.

## 3. Segunda Forma Normal (2FN)

**Regla:** la tabla debe estar en 1FN y todo atributo que no es clave debe depender de la clave completa, no solo de una parte. Solo puede violarse en tablas con clave compuesta.

**Estado del diagrama original: ya cumple la 2FN, por eso no se aplica ninguna transformación de dependencias.**

### 3.1 Verificación

- **Tablas con clave simple:** las tablas con clave simple (`Persona`, `Domicilio`, `Acusado`, `Condena`, `CausaJudicial`, `Secretaria`, `Fiscalia`, `UnidadCarcelaria`, `CambioCondena`) cumplen la 2FN automáticamente, porque una clave de una sola columna no tiene "partes".
- **Tablas con clave compuesta:** se revisaron una por una las tablas asociativas:

| Tabla | Clave primaria | Atributos no clave | ¿Dependen de la clave completa? |
| :--- | :--- | :--- | :--- |
| `PropiedadDomicilio` | (`persona_dni`, `domicilio_id`, `fechaDesde`) | `fechaHasta`, `esPrincipal` | Sí: cada valor describe un período concreto de una persona en un domicilio concreto. |
| `RelacionFamiliar` | (`persona_dni`, `familiar_dni`) | `tipo` | Sí: el parentesco describe el vínculo entre esas dos personas, no a una sola de ellas. |

Lo único que se hizo en este paso fue **definir las claves compuestas** de estas dos tablas, ya que el diagrama de clases no las tenía. Eso es parte de la conversión a relacional y no una corrección de 2FN.

**Resultado:** sin cambios de dependencias. El modelo cumple la 2FN.

## 4. Tercera Forma Normal (3FN)

**Regla:** la tabla debe estar en 2FN y ningún atributo no clave puede depender de otro atributo no clave (no hay dependencias transitivas). Dicho de otra forma, cada atributo debe depender de la clave, de toda la clave y nada más que de la clave.

**Estado del diagrama original: no cumple la 3FN.** Aquí sí se aplicaron correcciones.

### 4.1 Cambios necesarios para cumplir la 3FN

| Tabla | Atributo | Problema detectado | Solución aplicada |
| :--- | :--- | :--- | :--- |
| `Persona` | `edad` | Depende de `fechaNacimiento` (no clave). Además cambia con el tiempo y queda desactualizada. | Se elimina. La edad se calcula en consultas o en una vista. |
| `CausaJudicial` | `nombreSecretario` | Duplica `Secretaria.nombre` (dependencia transitiva vía `secretaria_id`). | Se elimina. Se accede al nombre mediante la FK `secretaria_id`. |
| `Condena` | `fechaFinEstimada` | Redundante: derivable de `fechaInicio` + `duracionMeses` (y de los `CambioCondena`). | Se elimina y se calcula. |
| `Condena` | `esPrisionDomiciliaria` | Redundante: dependiente de `domicilio_id IS NOT NULL`. | Se elimina. Se deduce de la FK `domicilio_id`. |

### 4.2 Mejoras de integridad (recomendadas, no exigidas por la 3FN)

Estas decisiones no corrigen violaciones de la 3FN, pero mejoran la calidad del modelo:

- **Enumeraciones como tablas de catálogo:** `EstadoCivil`, `NivelEducacion`, `TipoParentesco`, `EstadoAcusado` y `TipoCambioCondena` pasan a ser tablas (`id`, `nombre`) referenciadas por FK. Así los valores válidos se administran como datos y no como código. Una alternativa equivalente es usar `ENUM` o `CHECK` si se prefiere simplicidad.
- **Relaciones 0..1 con `UNIQUE`:** `Condena` se vincula a `Acusado` con `acusado_id UNIQUE`, y `UnidadCarcelaria` a `Domicilio` con `domicilio_id UNIQUE`.
- **Exclusión mutua en `Condena`:** un `CHECK` impide tener a la vez `domicilio_id` y `unidadCarcelaria_id`: `NOT (domicilio_id IS NOT NULL AND unidadCarcelaria_id IS NOT NULL)`.
- **`RelacionFamiliar`:** un `CHECK` evita que una persona sea familiar de sí misma: `persona_dni <> familiar_dni`.
- **Domicilio principal:** índice único parcial para permitir un solo domicilio principal vigente por persona (`esPrincipal = true AND fechaHasta IS NULL`).
- **Opcional:** `nombreJuez`, `nacionalidad` y `profesion` podrían pasar a tablas propias (`juez`, `nacionalidad`, `profesion`) para evitar errores de escritura. Se dejaron como columnas simples porque no violan la 3FN.

### 4.3 Modelo relacional normalizado (3FN)

Aplicando las correcciones de dependencias transitivas y atributos derivados, el esquema final en 3FN queda definido así:

```sql
VAR BASE RELATION Persona(
  dni varchar(20),
  nombres varchar(100),
  apellidos varchar(100),
  fechaNacimiento date,
  nacionalidad varchar(50),
  estadoCivil varchar(20),
  nivelEducacion varchar(20),
  profesion varchar(100),
  PRIMARY KEY (dni)
);
```

```sql
VAR BASE RELATION CausaJudicial(
  numeroInternoRegistro varchar(50),
  nombreJuez varchar(100),
  secretaria_id varchar(20),
  fechaAlta date,
  fechaResolucion date,
  PRIMARY KEY (numeroInternoRegistro),
  FOREIGN KEY (secretaria_id)
    REFERENCES Secretaria(id)
);
```

```sql
VAR BASE RELATION Domicilio(
  id varchar(20),
  direccion varchar(200),
  PRIMARY KEY (id)
);
```

```sql
VAR BASE RELATION Fiscalia(
  id varchar(20),
  nombre varchar(100),
  PRIMARY KEY (id)
);
```

```sql
VAR BASE RELATION Secretaria(
  id varchar(20),
  nombre varchar(100),
  PRIMARY KEY (id)
);
```

```sql
VAR BASE RELATION Acusado(
  id varchar(20),
  estadoActual varchar(20),
  dni varchar(20),
  numeroInternoRegistro varchar(50),
  PRIMARY KEY (id),
  FOREIGN KEY (dni)
    REFERENCES Persona(dni),
  FOREIGN KEY (numeroInternoRegistro)
    REFERENCES CausaJudicial(numeroInternoRegistro)
);
```

```sql
VAR BASE RELATION Condena(
  id varchar(20),
  fechaInicio date,
  duracionMeses int,
  fechaBajaLibertad date,
  acusado_id varchar(20),
  unidadCarcelaria_id varchar(20),
  domicilio_id varchar(20),
  PRIMARY KEY (id),
  FOREIGN KEY (acusado_id)
    REFERENCES Acusado(id),
  FOREIGN KEY (unidadCarcelaria_id)
    REFERENCES UnidadCarcelaria(id),
  FOREIGN KEY (domicilio_id)
    REFERENCES Domicilio(id)
);
```

```sql
VAR BASE RELATION CambioCondena(
  id varchar(20),
  fechaCambio date,
  tipoCambio varchar(30),
  razon varchar(200),
  condena_id varchar(20),
  PRIMARY KEY (id),
  FOREIGN KEY (condena_id)
    REFERENCES Condena(id)
);
```

```sql
VAR BASE RELATION UnidadCarcelaria(
  id varchar(20),
  nombre varchar(100),
  domicilio_id varchar(20),
  PRIMARY KEY (id),
  FOREIGN KEY (domicilio_id)
    REFERENCES Domicilio(id)
);
```

```sql
VAR BASE RELATION PropiedadDomicilio(
  persona_dni varchar(20),
  domicilio_id varchar(20),
  fechaDesde date,
  fechaHasta date,
  esPrincipal boolean,
  PRIMARY KEY (persona_dni, domicilio_id, fechaDesde),
  FOREIGN KEY (persona_dni)
    REFERENCES Persona(dni),
  FOREIGN KEY (domicilio_id)
    REFERENCES Domicilio(id)
);
```

```sql
VAR BASE RELATION RelacionFamiliar(
  persona_dni varchar(20),
  familiar_dni varchar(20),
  tipo varchar(20),
  PRIMARY KEY (persona_dni, familiar_dni),
  FOREIGN KEY (persona_dni)
    REFERENCES Persona(dni),
  FOREIGN KEY (familiar_dni)
    REFERENCES Persona(dni)
);
```

**Resultado:** todas las tablas quedan en 3FN.
