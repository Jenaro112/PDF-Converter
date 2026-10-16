---
coverConfig:
  showCover: false
  title: Sistema de Gestión Judicial
  subtitle: Modelo Lógico y Normalización a Tercera Forma Normal (3FN)
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

# Entregable 1: Modelo Lógico y Normalización a 3FN

## 1. Parte A: Modelo Lógico de la Base de Datos

### 1.1 Diagrama de Clases del Dominio (Modelo Original)

El modelo de partida corresponde al diagrama de clases estructurado a partir del relevamiento de requerimientos del fuero penal:

![Diagrama de Clases Original](/uploads/img_1792114144959.png)

El diagrama se compone de **11 entidades/clases** (9 entidades independientes y 2 clases asociativas) junto a **5 tipos enumerados (dominios restringidos)**.

### 1.2 Diccionario de Datos y Especificación de Atributos

A continuación se detalla la especificación de atributos para cada entidad, incluyendo su dominio de valores, rol dentro del esquema y restricciones de integridad:

#### 1. Persona
Representa a todo individuo registrado en el sistema judicial (acusados, familiares, etc.).

| Atributo | Tipo / Dominio | Rol / Restricción | Descripción |
| :--- | :--- | :--- | :--- |
| `dni` | `VARCHAR(20)` | **PK**, NOT NULL | Documento Nacional de Identidad (identificador unívoco). |
| `nombres` | `VARCHAR(100)` | NOT NULL | Nombres de pila de la persona. |
| `apellidos` | `VARCHAR(100)` | NOT NULL | Apellidos de la persona. |
| `fechaNacimiento` | `DATE` | NOT NULL, `<= CURRENT_DATE` | Fecha de nacimiento de la persona. |
| `edad` | `INT` | Opcional, `CHECK (edad >= 0)` | Edad en años (atributo derivado sujeto a revisión). |
| `nacionalidad` | `VARCHAR(50)` | NOT NULL | País de origen o nacionalidad. |
| `estadoCivil` | `EstadoCivil` | NOT NULL (Enumeración) | Estado civil legal de la persona. |
| `nivelEducacion` | `NivelEducacion` | NOT NULL (Enumeración) | Máximo nivel educativo alcanzado. |
| `profesion` | `VARCHAR(100)` | Opcional | Ocupación o profesión declarada. |

#### 2. Acusado
Especialización del rol de una persona cuando es formalmente vinculada a una causa judicial.

| Atributo | Tipo / Dominio | Rol / Restricción | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `VARCHAR(20)` | **PK**, NOT NULL | Identificador unívoco del registro de imputación. |
| `dni` | `VARCHAR(20)` | **FK**, NOT NULL | Referencia a la persona imputada (`Persona.dni`). |
| `numeroInternoRegistro` | `VARCHAR(50)` | **FK**, NOT NULL | Referencia a la causa judicial en que está imputado. |
| `estadoActual` | `EstadoAcusado` | NOT NULL (Enumeración) | Situación procesal vigente del imputado. |

#### 3. CausaJudicial
Expediente o proceso penal tramitado en la jurisdicción.

| Atributo | Tipo / Dominio | Rol / Restricción | Descripción |
| :--- | :--- | :--- | :--- |
| `numeroInternoRegistro` | `VARCHAR(50)` | **PK**, NOT NULL | Identificador judicial unívoco de la causa. |
| `nombreJuez` | `VARCHAR(100)` | NOT NULL | Nombre y apellido del magistrado a cargo. |
| `nombreSecretario` | `VARCHAR(100)` | Opcional | Nombre del secretario (atributo redundante sujeto a 3FN). |
| `fechaAlta` | `DATE` | NOT NULL | Fecha formal de radicación de la causa. |
| `fechaResolucion` | `DATE` | Opcional, `>= fechaAlta` | Fecha de cierre o sentencia definitiva. |
| `secretaria_id` | `VARCHAR(20)` | **FK**, NOT NULL | Secretaría judicial actuante. |
| `fiscalia_id` | `VARCHAR(20)` | **FK**, NOT NULL | Fiscalía interviniente en la causa. |

#### 4. Secretaria y Fiscalia
Órganos auxiliares y del Ministerio Público que intervienen en los procesos.

| Atributo | Tipo / Dominio | Rol / Restricción | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `VARCHAR(20)` | **PK**, NOT NULL | Identificador unívoco de la secretaría o fiscalía. |
| `nombre` | `VARCHAR(100)` | NOT NULL, UNIQUE | Denominación formal del organismo. |

#### 5. Condena
Pena impuesta por sentencia judicial firme a un acusado en una causa determinada.

| Atributo | Tipo / Dominio | Rol / Restricción | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `VARCHAR(20)` | **PK**, NOT NULL | Identificador unívoco de la condena dictada. |
| `acusado_id` | `VARCHAR(20)` | **FK**, NOT NULL, UNIQUE | Referencia unívoca al acusado condenado (relación 1:1). |
| `fechaInicio` | `DATE` | NOT NULL | Fecha efectiva de cómputo de la pena. |
| `duracionMeses` | `INT` | NOT NULL, `> 0` | Plazo total de la pena expresado en meses. |
| `fechaFinEstimada` | `DATE` | Opcional | Fecha calculada de finalización de pena. |
| `esPrisionDomiciliaria` | `BOOLEAN` | NOT NULL | Indicador de modalidad (derivable en 3FN). |
| `fechaBajaLibertad` | `DATE` | Opcional | Fecha efectiva de concesión de libertad. |
| `domicilio_id` | `VARCHAR(20)` | **FK**, Opcional | Domicilio asignado si la condena es domiciliaria. |
| `unidadCarcelaria_id` | `VARCHAR(20)` | **FK**, Opcional | Penal asignado si la condena es en prisión. |

#### 6. CambioCondena
Modificaciones, prórrogas, reducciones o traslados sufridos por una condena durante su ejecución.

| Atributo | Tipo / Dominio | Rol / Restricción | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `VARCHAR(20)` | **PK**, NOT NULL | Identificador unívoco del acto de modificación. |
| `condena_id` | `VARCHAR(20)` | **FK**, NOT NULL | Condena sobre la cual se aplica el cambio. |
| `fechaCambio` | `DATE` | NOT NULL | Fecha en que se dicta o entra en vigencia el cambio. |
| `tipoCambio` | `TipoCambioCondena` | NOT NULL (Enumeración) | Categoría del cambio penal otorgado. |
| `razon` | `VARCHAR(200)` | NOT NULL | Fundamentación jurídica o fáctica de la modificación. |

#### 7. Domicilio y UnidadCarcelaria
Lugares físicos donde residen personas o donde se cumplen las penas privativas de la libertad.

| Atributo | Tipo / Dominio | Rol / Restricción | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | `VARCHAR(20)` | **PK**, NOT NULL | Identificador unívoco del domicilio o unidad penal. |
| `direccion / nombre` | `VARCHAR(200)` | NOT NULL | Dirección física o nombre de la unidad carcelaria. |
| `domicilio_id` | `VARCHAR(20)` | **FK**, UNIQUE | Dirección física donde se emplaza la unidad carcelaria. |

#### 8. PropiedadDomicilio (Clase Asociativa)
Historial y vigencia de vinculación entre personas físicas y domicilios.

| Atributo | Tipo / Dominio | Rol / Restricción | Descripción |
| :--- | :--- | :--- | :--- |
| `persona_dni` | `VARCHAR(20)` | **PK, FK**, NOT NULL | Documento de la persona residente o titular. |
| `domicilio_id` | `VARCHAR(20)` | **PK, FK**, NOT NULL | Domicilio ocupado o declarado. |
| `fechaDesde` | `DATE` | **PK**, NOT NULL | Fecha de inicio de ocupación en el domicilio. |
| `fechaHasta` | `DATE` | Opcional, `>= fechaDesde` | Fecha de cese; `NULL` indica vigencia actual. |
| `esPrincipal` | `BOOLEAN` | NOT NULL, DEFAULT FALSE | Indica si es el domicilio legal/principal vigente. |

#### 9. RelacionFamiliar (Clase Asociativa)
Vínculos de consanguinidad o afinidad declarados entre dos personas físicas.

| Atributo | Tipo / Dominio | Rol / Restricción | Descripción |
| :--- | :--- | :--- | :--- |
| `persona_dni` | `VARCHAR(20)` | **PK, FK**, NOT NULL | Persona titular del registro vincular. |
| `familiar_dni` | `VARCHAR(20)` | **PK, FK**, NOT NULL | Persona con quien se posee el lazo familiar. |
| `tipo` | `TipoParentesco` | NOT NULL (Enumeración) | Grado y tipo de parentesco legal. |

### 1.3 Dominios y Enumeraciones

Las cinco enumeraciones del modelo definen dominios discretos y cerrados de valores válidos:

| Enumeración | Valores Válidos Permitidos | Semántica de Aplicación |
| :--- | :--- | :--- |
| `EstadoCivil` | SOLTERO, CASADO, DIVORCIADO, VIUDO, CONVIVIENTE | Situación conyugal legal de la persona. |
| `NivelEducacion` | SIN_INSTRUCCION, PRIMARIO, SECUNDARIO, TERCIARIO, UNIVERSITARIO | Nivel formativo acreditado por la persona. |
| `TipoParentesco` | MADRE, PADRE, HERMANO, HIJO | Grado de afinidad y parentesco consanguíneo. |
| `EstadoAcusado` | INDAGADO, PROCESADO, CONDENADO, SOBRESEIDO | Etapa procesal penal del imputado en la causa. |
| `TipoCambioCondena` | EXTENSION_CONDENA, REDUCCION_CONDENA, CAMBIO_UNIDAD_CARCELARIA, PRISION_DOMICILIARIA | Tipo de resolución de ejecución penal. |

### 1.4 Cardinalidad y Restricciones de las Relaciones

La siguiente matriz describe las asociaciones del modelo lógico, sus extremos de participación, cardinalidades y restricciones semánticas:

| Relación | Entidades Vinculadas | Cardinalidad | Semántica y Reglas de Negocio |
| :--- | :--- | :---: | :--- |
| **Imputación** | `Persona` → `Acusado` | `1 : 0..*` | Una persona puede tener 0 o múltiples imputaciones. Cada acusado corresponde a una única persona física. |
| **Integración Causa** | `CausaJudicial` → `Acusado` | `1 : 1..*` | Una causa debe tener al menos un acusado. Cada acusado está vinculado a una única causa. |
| **Dictado de Pena** | `Acusado` → `Condena` | `1 : 0..1` | Un acusado en una causa puede tener como máximo una condena dictada. Cada condena es de un solo acusado. |
| **Asignación Secretaría** | `Secretaria` → `CausaJudicial` | `1 : 0..*` | Toda causa pertenece obligatoriamente a una secretaría actuante. |
| **Asignación Fiscalía** | `Fiscalia` → `CausaJudicial` | `1 : 0..*` | Toda causa cuenta con la intervención de una fiscalía asignada. |
| **Ejecución de Pena** | `Condena` → `CambioCondena` | `1 : 0..*` | Una condena puede registrar sucesivas modificaciones durante su cumplimiento. |
| **Sede Penitenciaria** | `UnidadCarcelaria` → `Domicilio` | `0..1 : 1` | Cada unidad carcelaria posee una sede física unívoca. |
| **Prisión Domiciliaria** | `Condena` → `Domicilio` | `0..* : 0..1` | Si la condena es domiciliaria, se asocia a un domicilio específico de cumplimiento. |
| **Prisión Efectiva** | `Condena` → `UnidadCarcelaria` | `0..* : 0..1` | Si la condena es carcelaria, se asigna una unidad penitenciaria concreta. |
| **Residencia Habitacional** | `Persona` ↔ `Domicilio` | `1..* : 0..*` | Mapeada mediante `PropiedadDomicilio`. Historial de domicilios por persona. |
| **Parentesco Familiar** | `Persona` ↔ `Persona` | `0..* : 0..*` | Mapeada mediante `RelacionFamiliar`. Vínculos reflexivos n:m entre personas. |

---

## 2. Parte B: Modelo Relacional y Proceso de Normalización a 3FN

### 2.1 Esquema Relacional de Partida

La transformación objeto-relacional estándar del diagrama de clases inicial genera el siguiente conjunto de relaciones base:

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

### 2.2 Diagnóstico Inicial de Formas Normales

| Forma Normal | Estado en Modelo Inicial | Transformación Requerida | Fundamentación Técnica |
| :---: | :---: | :---: | :--- |
| **1FN** | **Cumple** | Ninguna | Todos los dominios son atómicos; no hay grupos repetitivos ni anidados. |
| **2FN** | **Cumple** | Ninguna | No existen dependencias funcionales parciales en claves compuestas. |
| **3FN** | **No Cumple** | **Sí (Reestructuración)** | Existen dependencias transitivas y atributos derivados redundantes. |

### 2.3 Primera Forma Normal (1FN)

**Definición Teórica:** Una relación $R$ se encuentra en Primera Forma Normal (1FN) si y solo si todos los atributos contienen exclusivamente valores atómicos (indivisibles dentro del dominio del sistema), no existen grupos repetitivos de atributos ni tablas anidadas dentro de columnas, y cada tupla es unívocamente identificable mediante una clave primaria.

**Verificación en el Modelo:**
1. **Atomicidad de dominios:** Los atributos primitivos (`dni`, `nombres`, `fechaNacimiento`, `direccion`, `duracionMeses`, etc.) almacenan un único valor escalar por tupla.
2. **Ausencia de grupos repetidos:** Los datos multiplicativos (múltiples domicilios por persona, sucesivos cambios de condena o múltiples vínculos familiares) se encuentran desacoplados en relaciones independientes (`PropiedadDomicilio`, `CambioCondena`, `RelacionFamiliar`) y no mediante colecciones serializadas ni columnas replicadas (`domicilio1`, `domicilio2`).
3. **Existencia de clave primaria:** Cada relación cuenta con una clave primaria formalmente definida.

> **Conclusión sobre 1FN:** El modelo original cumple estrictamente con la Primera Forma Normal. No se requieren descomposiciones en esta fase.

### 2.4 Segunda Forma Normal (2FN)

**Definición Teórica:** Una relación $R$ se encuentra en Segunda Forma Normal (2FN) si y solo si está en 1FN y ningún atributo no clave depende funcionalmente de un subconjunto propio de una clave candidata compuesta (es decir, todo atributo no clave presenta dependencia funcional completa respecto a la clave primaria).

**Verificación en el Modelo:**
- **Relaciones con clave simple:** Las relaciones `Persona`, `Domicilio`, `Acusado`, `Condena`, `CausaJudicial`, `Secretaria`, `Fiscalia`, `UnidadCarcelaria` y `CambioCondena` poseen claves primarias formadas por un único atributo. Por definición formal, no pueden tener subconjuntos propios, por lo que satisfacen la 2FN de forma inmediata y automática.
- **Relaciones con clave compuesta:** Se analizan las dos tablas asociativas resultantes de relaciones $M:N$:

| Tabla Asociativa | Clave Primaria (PK) | Atributos No Clave | Dependencia Funcional Completa |
| :--- | :--- | :--- | :--- |
| `PropiedadDomicilio` | (`persona_dni`, `domicilio_id`, `fechaDesde`) | `fechaHasta`, `esPrincipal` | **Sí:** Un período temporal concreto y la condición de principal describen la estancia de una persona en un domicilio particular; no dependen de la persona sola ni del domicilio solo. |
| `RelacionFamiliar` | (`persona_dni`, `familiar_dni`) | `tipo` | **Sí:** El tipo de vínculo de parentesco califica a la díada (par de personas), no a una de ellas aislada. |

> **Conclusión sobre 2FN:** Ambas tablas asociativas poseen dependencia funcional total. El modelo satisface plenamente la Segunda Forma Normal.

### 2.5 Tercera Forma Normal (3FN)

**Definición Teórica:** Una relación $R$ se encuentra en Tercera Forma Normal (3FN) si y solo si está en 2FN y ningún atributo no clave depende transitivamente de la clave primaria a través de otro atributo no clave (formalmente: para toda dependencia funcional no trivial $X \to Y$, $X$ es superclave o $Y$ es un atributo primo). En términos prácticos: cada atributo no clave debe depender directa y exclusivamente de la clave primaria.

**Análisis de Violaciones a la 3FN y Soluciones:**

| Tabla | Atributo Afectado | Dependencia Transitiva / Defecto | Corrección Aplicada en 3FN |
| :--- | :--- | :--- | :--- |
| `Persona` | `edad` | Dependencia transitiva: `dni` $\to$ `fechaNacimiento` $\to$ `edad`. Atributo derivado volátil que genera inconsistencia temporal. | **Eliminación:** Se suprime del esquema físico. La edad se computa dinámicamente en consultas mediante `AGE(fechaNacimiento)`. |
| `CausaJudicial` | `nombreSecretario` | Dependencia transitiva: `numeroInternoRegistro` $\to$ `secretaria_id` $\to$ `nombre`. Duplica el nombre almacenado en `Secretaria`. | **Eliminación y Clave Foránea:** Se suprime el nombre y se utiliza la FK `secretaria_id` referenciando a `Secretaria.id`. |
| `CausaJudicial` | *(Relación Fiscalia)* | Omisión de clave foránea formal hacia la fiscalía interviniente. | **Incorporación de FK:** Se incorpora explícitamente `fiscalia_id` referenciando a `Fiscalia.id`. |
| `Condena` | `fechaFinEstimada` | Atributo calculable/redundante derivado de `fechaInicio` + `duracionMeses` más las extensiones registradas en `CambioCondena`. | **Eliminación:** Se computa en tiempo de consulta o vista de liquidación de pena. |
| `Condena` | `esPrisionDomiciliaria` | Atributo redundante dependiente de `domicilio_id IS NOT NULL`. Dependencia funcional entre atributos no clave. | **Eliminación:** Se deduce directamente de si la clave foránea `domicilio_id` está poblada o es `NULL`. |

### 2.6 Diagrama de Clases Normalizado (Esquema en 3FN)

Aplicando las modificaciones señaladas, se obtiene el diagrama de clases normalizado con indicación explícita de claves primarias `{PK}` y claves foráneas `{FK}`:

![Diagrama de Clases Normalizado](/uploads/img_1792114244564.png)

### 2.7 Esquema Relacional Normalizado Final (3FN)

A continuación se detalla la definición formal de las relaciones resultantes en Tercera Forma Normal:

```sql
VAR BASE RELATION Persona(
  dni varchar(20),
  nombres varchar(100),
  apellidos varchar(100),
  fecha_nacimiento date,
  nacionalidad varchar(50),
  profesion varchar(100),
  estado_civil varchar(20),
  nivel_educacion varchar(20),
  PRIMARY KEY (dni)
);
```

```sql
VAR BASE RELATION CausaJudicial(
  numero_interno_registro varchar(50),
  nombre_juez varchar(100),
  fecha_alta date,
  fecha_resolucion date,
  secretaria_id varchar(20),
  fiscalia_id varchar(20),
  PRIMARY KEY (numero_interno_registro),
  FOREIGN KEY (secretaria_id)
    REFERENCES Secretaria(id),
  FOREIGN KEY (fiscalia_id)
    REFERENCES Fiscalia(id)
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
  persona_dni varchar(20),
  causa_numero varchar(50),
  estado_actual varchar(20),
  PRIMARY KEY (id),
  FOREIGN KEY (persona_dni)
    REFERENCES Persona(dni),
  FOREIGN KEY (causa_numero)
    REFERENCES CausaJudicial(numero_interno_registro)
);
```

```sql
VAR BASE RELATION Condena(
  id varchar(20),
  acusado_id varchar(20),
  fecha_inicio date,
  duracion_meses int,
  fecha_baja_libertad date,
  domicilio_id varchar(20),
  unidad_carcelaria_id varchar(20),
  PRIMARY KEY (id),
  FOREIGN KEY (acusado_id)
    REFERENCES Acusado(id),
  FOREIGN KEY (domicilio_id)
    REFERENCES Domicilio(id),
  FOREIGN KEY (unidad_carcelaria_id)
    REFERENCES UnidadCarcelaria(id),
  CONSTRAINT unq_condena_acusado UNIQUE (acusado_id)
);
```

```sql
VAR BASE RELATION CambioCondena(
  id varchar(20),
  condena_id varchar(20),
  fecha_cambio date,
  tipo_cambio varchar(30),
  razon varchar(200),
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
    REFERENCES Domicilio(id),
  CONSTRAINT unq_unidad_domicilio UNIQUE (domicilio_id)
);
```

```sql
VAR BASE RELATION PropiedadDomicilio(
  persona_dni varchar(20),
  domicilio_id varchar(20),
  fecha_desde date,
  fecha_hasta date,
  es_principal boolean,
  PRIMARY KEY (persona_dni, domicilio_id, fecha_desde),
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
  tipo_parentesco varchar(20),
  PRIMARY KEY (persona_dni, familiar_dni),
  FOREIGN KEY (persona_dni)
    REFERENCES Persona(dni),
  FOREIGN KEY (familiar_dni)
    REFERENCES Persona(dni)
);
```

### 2.8 Restricciones de Integridad y Reglas Semánticas del Modelo

Para garantizar la completitud operativa del modelo de acuerdo a las reglas del negocio judicial, se establecen las siguientes restricciones complementarias:

1. **Unicidad de pena por imputación procesal:** La columna `acusado_id` en la tabla `Condena` posee una restricción `UNIQUE`, implementando la cardinalidad $1:0..1$.
2. **Exclusión mutua de modalidades de condena:** Una persona condenada no puede estar asignada simultáneamente a una unidad carcelaria y a un domicilio. Se asegura mediante la restricción:
   $$\text{CHECK} \ (\text{NOT} \ (domicilio\_id \ \text{IS NOT NULL} \ \text{AND} \ unidad\_carcelaria\_id \ \text{IS NOT NULL}))$$
3. **Restricción no reflexiva de parentesco:** Una persona no puede registrar un vínculo de parentesco consigo misma en `RelacionFamiliar`:
   $$\text{CHECK} \ (persona\_dni \ne familiar\_dni)$$
4. **Domicilio principal único vigente:** Se define un índice único parcial que restringe la existencia de un solo domicilio principal activo por persona:
   $$\text{CREATE UNIQUE INDEX} \ \text{idx\_domicilio\_principal} \ \text{ON} \ PropiedadDomicilio(persona\_dni) \ \text{WHERE} \ (es\_principal = \text{TRUE} \ \text{AND} \ fecha\_hasta \ \text{IS NULL})$$
5. **Consistencia cronológica:** En las tablas con períodos de vigencia temporal, las fechas de finalización deben ser iguales o posteriores a las de inicio:
   - `CausaJudicial`: `fecha_resolucion >= fecha_alta` (cuando no sea nula).
   - `PropiedadDomicilio`: `fecha_hasta >= fecha_desde` (cuando no sea nula).
   - `Condena`: `fecha_baja_libertad >= fecha_inicio` (cuando no sea nula).

---

## 3. Conclusión

El esquema obtenido representa fielmente el dominio de la administración judicial, eliminando redundancias y riesgos de anomalías de inserción, modificación y borrado. Al alcanzar la **Tercera Forma Normal (3FN)**, cada atributo no clave depende estricta y funcionalmente de la clave primaria, garantizando un modelo óptimo, desacoplado y preparado para su implementación física.
