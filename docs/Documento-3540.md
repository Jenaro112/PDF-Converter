---
coverConfig:
  showCover: false
  title: Administración de Proyectos (Gestión)
  subtitle: Trabajo Nro. 10
  materia: Ing. de Software II
  coverStyle: academic_elegant
  showLogo: true
  integrantes:
    - Galdini Jenaro
  profesores:
    - Dr. Pedro E. Colla
    - Lic. Lucía Blanc
    - ''
  sigla: ''
  fecha: ''
  showHeader: false
  showFooter: true
activeTheme: minimal
---
# Aventura 360 — Planificación del desarrollo

## 1. Objetivo

Organizar el desarrollo del ecommerce de Aventura 360 mediante un enfoque Kanban, utilizando fases funcionales para ordenar el alcance y estimar el trabajo, e historias de usuario para representar incrementos funcionales verificables.

El sistema permitirá consultar y buscar equipamiento de camping y trekking, administrar productos e inventario, realizar compras mediante Mercado Pago y gestionar los pedidos. También se contemplan funcionalidades de personalización y supervisión comercial.

## 2. Metodología de trabajo

Se utilizará **Kanban**, con un flujo continuo de trabajo y sin sprints obligatorios.

### Organización del trabajo

* **Fase:** agrupación funcional de historias de usuario relacionadas.
* **Caso de uso (UC):** especificación de referencia que describe actores, precondiciones, flujo principal, alternativas, postcondiciones y reglas de negocio.
* **Historia de usuario (HU):** incremento funcional derivado de uno o varios casos de uso.
* **Issue de GitHub:** cada HU implementable tendrá su propio Issue.
* **Sub-issues:** se utilizarán únicamente cuando una HU necesite descomponerse en tareas coordinadas.
* **GitHub Projects:** tablero general para visualizar y gestionar el flujo de trabajo.
* **Milestones:** se utilizarán para representar entregas o hitos temporales relevantes, no necesariamente una fase por milestone.

Las fases no constituyen sprints ni implican que deban finalizar por completo antes de iniciar la siguiente. Podrán existir tareas en paralelo cuando sus dependencias lo permitan.

### Flujo Kanban inicial

`Backlog → Ready → In Progress → Review / Testing → Done`

Reglas iniciales:

* Una HU debe cumplir la Definition of Ready (DoR) antes de pasar a `Ready`.
* Cada integrante debe tomar trabajo según la capacidad disponible y las prioridades.
* Se establecerá un límite inicial de trabajo en curso (WIP) de 1 HU por integrante en `In Progress`; se podrá ajustar a partir de la experiencia del equipo.
* Las HU terminadas deberán cumplir los criterios de aceptación y la Definition of Done (DoD).
* Los cambios de alcance, bloqueos y dependencias se registrarán en los Issues.
* Se revisará periódicamente el tiempo de ciclo, los bloqueos y la cantidad de HU terminadas.

## 3. Convención de identificación y trazabilidad

Se utilizarán identificadores provisionales para planificar las historias. Los números definitivos serán los que asigne GitHub al crear los Issues.

| Identificador | Significado                            |
| ------------- | -------------------------------------- |
| RF            | Requerimiento funcional o no funcional |
| UC            | Caso de uso existente en Notion        |
| HU            | Historia de usuario                    |
| F             | Fase funcional                         |

Los identificadores HU-XX son referencias de planificación, no números reales de Issues de GitHub.

Cada Issue de HU deberá incluir:

* Título de la historia.
* Descripción en formato de historia de usuario.
* Requerimientos y casos de uso relacionados.
* Criterios de aceptación verificables.
* Prioridad.
* Dependencias y bloqueos.
* Estimación inicial.
* Evidencia de pruebas o validación.

## 4. Fase 0 — Relevamiento, definición y decisión tecnológica

**Objetivo:** validar el alcance, resolver las cuestiones pendientes de los requerimientos y elegir una solución tecnológica sostenible para el equipo.

Esta fase incluye tareas de análisis que no son necesariamente historias de usuario del producto.

### Tareas de planificación

* [ ] Revisar los 23 requerimientos registrados y los 19 casos de uso.
* [ ] Verificar la trazabilidad entre RF, UC e historias de usuario.
* [ ] Identificar inconsistencias, reglas incompletas y dependencias.
* [ ] Definir qué funcionalidades son obligatorias para la primera entrega.
* [ ] Evaluar el stack propio, un CMS ecommerce y una alternativa híbrida.
* [ ] Determinar el alcance de la personalización del panel administrativo.
* [ ] Estimar el esfuerzo considerando la experiencia, disponibilidad y capacidad del equipo.
* [ ] Definir arquitectura, estrategia de pruebas y despliegue.

### Decisión de stack y CMS

Se compararán tres alternativas:

1. **Desarrollo propio:** frontend, backend y PostgreSQL, con un panel administrativo desarrollado específicamente para el negocio.
2. **CMS ecommerce:** una plataforma que proporcione catálogo, gestión de pedidos y administración desde el inicio.
3. **Solución híbrida:** experiencia de compra personalizada con servicios o herramientas existentes para la gestión comercial.

La decisión se documentará considerando:

* Tiempo de implementación y complejidad.
* Integración con Mercado Pago.
* Personalización de la tienda y del panel administrativo.
* Gestión de productos, variantes, stock, descuentos y pedidos.
* Autenticación y permisos.
* Seguridad y mantenimiento.
* Costos de infraestructura y licencias.
* Capacidad del equipo para desarrollar y mantener la solución.
* Posibilidad de desplegar, probar y mantener el sistema.

**Criterio de salida:** existe una decisión tecnológica documentada, con sus motivos, limitaciones y consecuencias para el plan. No se comenzará a implementar funcionalidades dependientes de una arquitectura aún sin definir.

## 5. Fase 1 — Base técnica, diseño y calidad transversal

**Objetivo:** preparar la infraestructura necesaria para implementar las funcionalidades sin duplicar trabajo ni comprometer la calidad.

### Tareas

* [ ] Configurar el repositorio, las ramas de trabajo y los Pull Requests.
* [ ] Definir estructura del proyecto y convenciones de código.
* [ ] Preparar los entornos de desarrollo y prueba.
* [ ] Definir el modelo de datos inicial.
* [ ] Establecer el diseño visual y los componentes reutilizables.
* [ ] Configurar validaciones, manejo de errores y registro técnico.
* [ ] Definir el procedimiento de despliegue y configuración por entorno.

### Requerimientos no funcionales transversales

* **RNF-001 — Diseño responsive:** definir los tamaños y comportamientos esperados en dispositivos móviles, tablets y escritorio.
* **RNF-002 — Disponibilidad 24/7:** definir el objetivo de disponibilidad, la infraestructura y el procedimiento de recuperación.
* **RNF-003 — Seguridad:** completar el requerimiento pendiente con criterios verificables de autenticación, autorización, protección de datos y validación de entradas.
* **RNF-004 — Rendimiento:** reemplazar la descripción genérica por métricas y condiciones de prueba acordadas.

Los criterios de disponibilidad y rendimiento deberán ser definidos y validados con el equipo antes de considerarse cumplidos.

## 6. Fase 2 — Identidad y acceso

**Objetivo:** permitir que los compradores creen y administren sus cuentas y que los administradores accedan de manera autorizada al sistema.

### HU-01 — Registrar una cuenta

**Como** visitante, **quiero** crear una cuenta de comprador, **para** guardar mis preferencias y gestionar mis compras.

* Referencias: RF-18, UC-18.
* Prioridad: Must.

Criterios de aceptación:

* Se puede completar el formulario con los campos obligatorios definidos.
* El sistema valida los datos ingresados y el formato del correo electrónico.
* No se permite registrar una dirección de correo ya utilizada.
* La contraseña debe cumplir los requisitos de seguridad acordados.
* Una vez completado el registro, el sistema confirma el resultado y aplica el comportamiento de autenticación definido.

### HU-02 — Iniciar sesión

**Como** usuario registrado, **quiero** iniciar sesión, **para** acceder a las funcionalidades correspondientes a mi cuenta.

* Referencias: RF-16, UC-1.
* Prioridad: Must.

Criterios de aceptación:

* Se puede iniciar sesión con credenciales válidas.
* Las credenciales incorrectas no permiten acceder.
* La sesión respeta el tiempo de expiración definido.
* Las rutas y operaciones administrativas requieren los permisos correspondientes.
* El sistema comunica los errores sin exponer información sensible.

### HU-03 — Recuperar contraseña

**Como** usuario registrado, **quiero** recuperar mi contraseña, **para** volver a acceder a mi cuenta si la olvidé.

* Referencias: RF-17, UC-17.
* Prioridad: Must.

Criterios de aceptación:

* El usuario puede solicitar la recuperación mediante su correo electrónico.
* Se utiliza un enlace o mecanismo seguro, temporal y de un solo uso.
* Una vez validado el mecanismo, se puede establecer una contraseña nueva.
* Los enlaces expirados o utilizados no permiten restablecer nuevamente la contraseña.
* La respuesta no revela si una dirección de correo está registrada.

## 7. Fase 3 — Catálogo y descubrimiento de productos

**Objetivo:** permitir que los visitantes y compradores conozcan la oferta de equipamiento disponible y encuentren productos de interés.

### HU-04 — Consultar el catálogo

**Como** visitante o comprador, **quiero** visualizar los productos disponibles en el catálogo, **para** conocer la oferta de Aventura 360.

* Referencias: RF-001, UC-4.
* Prioridad: Must.

Criterios de aceptación:

* El catálogo muestra los productos correspondientes al alcance acordado.
* Cada producto presenta imagen, nombre, marca, precio y estado de disponibilidad.
* Los productos sin stock siguen visibles con una indicación clara.
* Los productos con una sola unidad disponible muestran el distintivo correspondiente.
* La información presentada coincide con los datos registrados.

### HU-05 — Buscar productos

**Como** visitante o comprador, **quiero** buscar productos por palabras clave, **para** encontrar equipamiento específico.

* Referencias: RF-002, UC-2.
* Prioridad: Must.

Criterios de aceptación:

* El usuario puede ingresar un término de búsqueda.
* El sistema muestra los productos que coinciden con el criterio acordado.
* Se informa cuando no existen resultados.
* Las palabras clave se registran para las métricas comerciales, según las reglas de privacidad definidas.

### HU-06 — Filtrar productos

**Como** visitante o comprador, **quiero** filtrar los productos del catálogo, **para** reducir los resultados según mis necesidades.

* Referencias: RF-003, UC-3.
* Prioridad: Must.

Criterios de aceptación:

* Se pueden aplicar los filtros definidos por el equipo.
* Los resultados respetan los filtros seleccionados.
* Se puede restablecer la selección de filtros.
* Si no existen coincidencias, se muestra un mensaje claro.
* La lista filtrada mantiene la información de precio y disponibilidad.

**Bloqueo previo:** se debe cerrar la definición de filtros contemplada en RF-003. La primera versión puede priorizar categorías y agregar otros filtros si el alcance lo requiere.

## 8. Fase 4 — Administración de productos, inventario y ofertas

**Objetivo:** permitir que el administrador mantenga actualizado el catálogo y gestione la disponibilidad comercial.

Esta fase depende de la decisión tecnológica y de la disponibilidad de autenticación y permisos administrativos.

### HU-07 — Registrar y modificar productos

**Como** administrador, **quiero** crear, editar y deshabilitar productos, **para** mantener actualizado el catálogo.

* Referencias: RF-011, UC-15.
* Prioridad: Must.

Criterios de aceptación:

* Se puede registrar un producto con los atributos obligatorios definidos.
* El SKU debe ser válido y único.
* Se puede modificar la información de un producto existente.
* Se puede deshabilitar un producto sin eliminar indebidamente el historial asociado.
* Los cambios se reflejan en el catálogo público.
* Solo los usuarios autorizados pueden realizar estas operaciones.

### HU-08 — Consultar y actualizar el stock

**Como** administrador, **quiero** consultar y actualizar el stock, **para** mantener un inventario consistente.

* Referencias: RF-012, UC-13.
* Prioridad: Must.

Criterios de aceptación:

* Se visualizan las cantidades disponibles.
* Se identifican los productos con stock bajo o sin stock según las reglas acordadas.
* Se pueden registrar ajustes de inventario.
* No se aceptan cantidades inválidas o negativas.
* Los cambios se reflejan en la tienda.
* Las ventas confirmadas actualizan el inventario según las reglas transaccionales definidas.

### HU-09 — Administrar ofertas

**Como** administrador, **quiero** crear, modificar y desactivar ofertas, **para** gestionar las promociones de la tienda.

* Referencias: RF-013, UC-14.
* Prioridad: Must.

Criterios de aceptación:

* Se puede definir el descuento y los productos o categorías alcanzados.
* Se pueden establecer las fechas de vigencia cuando corresponda.
* El sistema valida los valores permitidos.
* El catálogo muestra el precio promocional y el precio original cuando corresponda.
* Al desactivar una oferta, deja de aplicarse el descuento.
* Los precios finales se calculan de forma consistente durante la compra.

## 9. Fase 5 — Carrito y preparación de compra

**Objetivo:** permitir que el comprador seleccione productos, ajuste las cantidades y prepare su pedido.

### HU-10 — Agregar productos al carrito

**Como** comprador, **quiero** agregar productos al carrito, **para** reunir el equipamiento que deseo comprar.

* Referencias: RF-004, UC-10.
* Prioridad: Must.

Criterios de aceptación:

* Se puede agregar un producto desde los puntos de acceso definidos.
* El carrito refleja los productos seleccionados.
* Se actualizan el contador y el resumen del carrito.
* No se permite agregar cantidades superiores a las disponibles.

### HU-11 — Modificar el carrito

**Como** comprador, **quiero** cambiar cantidades o eliminar productos del carrito, **para** ajustar mi compra antes de pagar.

* Referencias: RF-004, UC-10.
* Prioridad: Must.

Criterios de aceptación:

* Se pueden incrementar y decrementar cantidades.
* Se pueden eliminar productos.
* El sistema recalcula subtotales, descuentos y total.
* El carrito vacío muestra un mensaje y una forma de volver al catálogo.
* Antes de iniciar el pago, se vuelve a validar la disponibilidad y los precios.

### HU-12 — Confirmar los datos de la compra

**Como** comprador, **quiero** revisar mi pedido e ingresar los datos de entrega, **para** confirmar qué estoy comprando y dónde recibirlo.

* Referencias: RF-004, UC-6.
* Prioridad: Must.

Criterios de aceptación:

* Se muestra el resumen de productos, cantidades, precios y total.
* Se solicitan los datos de entrega definidos para el proyecto.
* Se validan los campos obligatorios.
* El comprador puede volver al carrito antes de confirmar.
* No se inicia el pago si el pedido no cumple las condiciones necesarias.

## 10. Fase 6 — Pago, confirmación y comprobantes

**Objetivo:** integrar Mercado Pago y completar el registro de una compra de forma segura y consistente.

### HU-13 — Pagar mediante Mercado Pago

**Como** comprador, **quiero** pagar mi pedido mediante Mercado Pago, **para** completar la compra de los productos seleccionados.

* Referencias: RF-007, UC-6.
* Prioridad: Must.

Criterios de aceptación:

* El sistema inicia el flujo de pago con el importe correcto.
* La confirmación de pago se verifica mediante el mecanismo seguro que corresponda a la integración.
* No se considera pagado un pedido únicamente por regresar desde la página del proveedor.
* Se contemplan pagos aprobados, rechazados, pendientes, cancelados y sesiones expiradas.
* El procesamiento de una misma notificación no genera ventas ni descuentos de stock duplicados.
* El pedido y el inventario se actualizan según el estado definitivo del pago.

### HU-14 — Registrar la compra y actualizar el pedido

**Como** comprador, **quiero** que mi compra quede registrada cuando corresponda, **para** disponer de una referencia de mi pedido.

* Referencias: RF-007, UC-6.
* Prioridad: Must.

Criterios de aceptación:

* Cada pedido tiene un identificador único.
* Se registra el detalle de los productos, cantidades, importe y estado.
* Se mantiene la relación entre el pedido y su comprador.
* Se descuenta el stock una sola vez cuando se cumple la condición de negocio definida.
* Los pagos pendientes o rechazados no se tratan como pagos aprobados.
* Las actualizaciones de pago y stock mantienen la consistencia de los datos.

### HU-15 — Recibir el comprobante de compra

**Como** comprador, **quiero** recibir el comprobante de mi compra por correo electrónico, **para** conservar constancia de la operación.

* Referencias: RF-008, UC-5.
* Prioridad: Must.

Criterios de aceptación:

* Se genera el comprobante correspondiente a una compra confirmada.
* Se envía al correo asociado a la compra según la regla definida.
* El comprobante incluye los datos acordados del pedido y el importe.
* Un fallo de envío no duplica la compra ni altera su estado de pago.
* El sistema registra el resultado del envío para poder diagnosticar fallos.

## 11. Fase 7 — Pedidos, historial y seguimiento

**Objetivo:** permitir que compradores y administradores consulten y gestionen los pedidos después de iniciar una compra.

### HU-16 — Consultar el historial de compras

**Como** comprador, **quiero** consultar mis compras anteriores, **para** revisar sus detalles y estados.

* Referencias: RF-006, UC-7.
* Prioridad: Should.

Criterios de aceptación:

* Se listan los pedidos asociados al comprador autenticado.
* Cada pedido muestra fecha, identificador, productos, importe y estado.
* Se puede consultar el detalle de una compra.
* Se informa cuando no existen compras registradas.
* Un comprador no puede consultar el historial de otro usuario.

### HU-17 — Consultar el seguimiento de un pedido

**Como** comprador, **quiero** consultar el estado de mi pedido, **para** conocer el avance de la entrega.

* Referencias: RF-009, UC-9.
* Prioridad: Must.

Criterios de aceptación:

* Se puede acceder al seguimiento desde el historial o mediante el mecanismo definido.
* Se muestra el estado actual del pedido y una secuencia de sus etapas.
* Se informa cuando el identificador no es válido.
* Solo se muestran datos de pedidos autorizados para el comprador.
* Se documenta si la actualización del seguimiento es manual o depende de un servicio externo.

### HU-18 — Administrar pedidos

**Como** administrador, **quiero** consultar y actualizar los pedidos, **para** gestionar su preparación y entrega.

* Referencias: RF-015, UC-16.
* Prioridad: Must.

Criterios de aceptación:

* Se listan los pedidos con sus datos principales.
* Se puede consultar el detalle y la dirección de entrega.
* Se puede actualizar el estado respetando las transiciones permitidas.
* Se puede registrar el código de seguimiento cuando corresponda.
* Los cambios se reflejan en el seguimiento del comprador.
* Las cancelaciones aplican las reglas acordadas para reintegrar stock y conservar la trazabilidad.

## 12. Fase 8 — Personalización de la experiencia de compra

**Objetivo:** incorporar funcionalidades que faciliten la selección de equipamiento y mejoren la experiencia del comprador.

### HU-19 — Gestionar favoritos

**Como** comprador, **quiero** guardar y quitar productos de favoritos, **para** conservar una lista de equipamiento de mi interés.

* Referencias: RF-005, UC-8.
* Prioridad: Should.

Criterios de aceptación:

* Se puede agregar un producto a favoritos.
* Se puede quitar un producto previamente guardado.
* El estado del control visual coincide con la lista persistida.
* Si el usuario no está autenticado, se le solicita iniciar sesión o registrarse.
* La lista corresponde exclusivamente al comprador autenticado.

### HU-20 — Obtener recomendaciones mediante el asistente

**Como** comprador, **quiero** responder preguntas sobre mi actividad y necesidades, **para** recibir recomendaciones de equipamiento adecuadas.

* Referencias: RF-010, UC-11.
* Prioridad: Must.

Criterios de aceptación:

* El asistente permite seleccionar criterios definidos, como actividad, duración, clima y cantidad de personas.
* Las recomendaciones se obtienen a partir de reglas y características disponibles de los productos.
* Se muestran productos compatibles con los criterios seleccionados.
* Los resultados incluyen características y precios.
* Se informa cuando no hay productos compatibles.
* El comprador puede acceder al detalle o agregar los productos sugeridos al carrito.

El alcance inicial debe priorizar un sistema de recomendaciones basado en reglas explícitas. No se presupone la necesidad de inteligencia artificial generativa.

## 13. Fase 9 — Métricas y auditoría administrativa

**Objetivo:** ofrecer información comercial útil y trazabilidad de las acciones administrativas.

### HU-21 — Consultar métricas comerciales

**Como** administrador, **quiero** consultar estadísticas comerciales, **para** evaluar el desempeño de la tienda y tomar decisiones.

* Referencias: RF-014, UC-12.
* Prioridad: Should.

Criterios de aceptación:

* Se muestran las métricas acordadas, como ventas, ingresos, pedidos y productos más vendidos.
* Se puede filtrar por rango de fechas y categoría cuando corresponda.
* Las cifras coinciden con los registros del sistema y las definiciones de cada indicador.
* Se informa cuando no hay datos para el período seleccionado.
* Las búsquedas registradas se utilizan de acuerdo con las reglas de privacidad definidas.

### HU-22 — Consultar logs administrativos

**Como** administrador autorizado, **quiero** consultar el registro de actividades administrativas, **para** auditar modificaciones y detectar acciones relevantes.

* Referencias: RF-020, UC-19.
* Prioridad: Should.

Criterios de aceptación:

* Se registran las acciones administrativas relevantes definidas por el equipo.
* Cada evento contiene fecha, actor, acción y entidad afectada.
* Se permite filtrar por período, administrador, tipo de acción o módulo.
* Cuando corresponda, se conserva información suficiente para identificar los cambios.
* Los logs no pueden ser modificados por usuarios sin autorización.
* No se almacenan contraseñas, secretos ni datos sensibles innecesarios.

## 14. Fase 10 — Integración, seguridad, pruebas y entrega

**Objetivo:** validar el funcionamiento integral de las funcionalidades y preparar una versión desplegable.

### Tareas

* [ ] Verificar la trazabilidad entre requerimientos, casos de uso, HU y pruebas.
* [ ] Ejecutar pruebas funcionales de los flujos principales y alternativos.
* [ ] Probar registro, inicio de sesión, recuperación y permisos.
* [ ] Validar el comportamiento de carrito, stock y pagos.
* [ ] Probar pagos aprobados, rechazados, pendientes y notificaciones repetidas.
* [ ] Verificar la consistencia de pedidos, comprobantes e historial.
* [ ] Realizar pruebas responsive en los dispositivos acordados.
* [ ] Medir el rendimiento con las condiciones definidas para RNF-004.
* [ ] Verificar los controles de seguridad definidos en RNF-003.
* [ ] Validar el procedimiento de despliegue y recuperación.
* [ ] Preparar documentación de instalación, configuración y uso.
* [ ] Realizar una validación final con los interesados del proyecto.

Esta fase puede desarrollarse parcialmente en paralelo con las fases funcionales. Las pruebas no deben concentrarse únicamente al final: cada HU deberá verificarse durante su implementación.

## 15. Dependencias generales

La siguiente secuencia representa dependencias principales, no un cronograma rígido:

1. La decisión tecnológica habilita la implementación de la arquitectura y el entorno.
2. La autenticación y los permisos habilitan las operaciones administrativas y las funcionalidades de cuenta.
3. El catálogo permite comenzar las funcionalidades de búsqueda, filtros y selección de productos.
4. La gestión de productos e inventario habilita la operación consistente del catálogo.
5. El carrito y la preparación de compra habilitan el checkout.
6. La integración de pagos habilita la confirmación de compras y los comprobantes.
7. Los pedidos registrados habilitan el historial y el seguimiento.
8. Los datos operativos habilitan las métricas comerciales y los logs.
9. Las pruebas de integración y seguridad validan el conjunto de funcionalidades antes de la entrega.

Siempre que sea posible, el catálogo puede desarrollarse inicialmente con datos de prueba mientras se completa el panel administrativo. Las tareas que dependan de la elección de CMS o arquitectura deben permanecer bloqueadas hasta tomar esa decisión.

## 16. Definition of Ready (DoR)

Una HU estará lista para comenzar cuando:

* [ ] Tiene un título y una descripción claros.
* [ ] Está relacionada con los RF y UC correspondientes.
* [ ] Sus criterios de aceptación son verificables.
* [ ] El alcance está suficientemente definido.
* [ ] Se identificaron sus dependencias y bloqueos.
* [ ] Tiene una prioridad acordada.
* [ ] El equipo comprende el resultado funcional esperado.
* [ ] Tiene una estimación inicial.
* [ ] No depende de una decisión tecnológica pendiente que impida implementarla.

## 17. Definition of Done (DoD)

Una HU se considerará terminada cuando:

* [ ] Cumple todos sus criterios de aceptación.
* [ ] La implementación está integrada en el repositorio.
* [ ] Se realizaron las pruebas correspondientes.
* [ ] Se revisó el código mediante Pull Request.
* [ ] No quedan defectos bloqueantes conocidos.
* [ ] Se respetan los controles de seguridad y permisos aplicables.
* [ ] La documentación necesaria está actualizada.
* [ ] El cambio está integrado en la rama acordada.
* [ ] El Issue contiene evidencia de validación y queda cerrado.

## 18. Convenciones para GitHub

### Labels sugeridas

**Por tipo de trabajo**

* `type: user-story`
* `type: bug`
* `type: technical`
* `type: research`
* `type: documentation`

**Por fase**

* `phase: architecture`
* `phase: identity`
* `phase: catalog`
* `phase: administration`
* `phase: checkout`
* `phase: orders`
* `phase: personalization`
* `phase: analytics`
* `phase: delivery`

**Por prioridad**

* `priority: must`
* `priority: should`
* `priority: could`

**Por estado especial**

* `blocked`
* `needs-definition`

### Ramas y Pull Requests

Se propone utilizar ramas cortas asociadas a cada Issue, por ejemplo:

* `feat/hu-04-catalogo`
* `feat/hu-13-mercado-pago`
* `fix/hu-08-validacion-stock`

Cada Pull Request debe explicar el cambio, relacionarlo con el Issue y documentar las pruebas realizadas. Al integrarlo, se utilizará `Closes #N` cuando corresponda cerrar el Issue asociado.

### Estructura de un Issue de HU

```markdown
## Historia de usuario

Como [actor], quiero [funcionalidad], para [beneficio].

## Referencias
- RF:
- UC:

## Criterios de aceptación
- [ ] Criterio verificable 1.
- [ ] Criterio verificable 2.
- [ ] Criterio verificable 3.

## Dependencias
- Ninguna / #N

## Pruebas
- [ ] Flujo principal.
- [ ] Alternativas y errores relevantes.

## Definition of Done
- [ ] Implementación integrada.
- [ ] Pruebas realizadas.
- [ ] Pull Request revisado.
- [ ] Documentación actualizada.
```

## 19. Estimación y planificación temporal

No se asignan fechas definitivas en esta versión porque todavía deben validarse la arquitectura, el alcance de la primera entrega y la capacidad semanal del equipo.

La estimación temporal se realizará después de:

1. Resolver la selección del stack y el alcance del panel administrativo.
2. Revisar el tamaño de las HU y dividir las que sean demasiado grandes.
3. Estimar cada HU mediante puntos relativos o tallas de esfuerzo.
4. Identificar dependencias y tareas que pueden desarrollarse en paralelo.
5. Estimar la capacidad semanal del equipo a partir de las horas disponibles.
6. Construir una previsión inicial y actualizarla según el flujo real de trabajo.

Se utilizarán el tiempo de ciclo, el throughput y los bloqueos para mejorar las estimaciones a medida que avance el proyecto.

## 20. Trazabilidad de los requerimientos

| Requerimiento                         | HU propuesta        | Fase    |
| ------------------------------------- | ------------------- | ------- |
| RF-001 Consultar catálogo             | HU-04               | F3      |
| RF-002 Buscar productos               | HU-05               | F3      |
| RF-003 Filtrar productos              | HU-06               | F3      |
| RF-004 Gestionar carrito              | HU-10, HU-11, HU-12 | F5      |
| RF-005 Gestionar favoritos            | HU-19               | F8      |
| RF-006 Consultar historial            | HU-16               | F7      |
| RF-007 Realizar pago                  | HU-13, HU-14        | F6      |
| RF-008 Recibir comprobante            | HU-15               | F6      |
| RF-009 Seguimiento de pedido          | HU-17               | F7      |
| RF-010 Asistente de recomendaciones   | HU-20               | F8      |
| RF-011 Gestionar productos            | HU-07               | F4      |
| RF-012 Gestionar stock                | HU-08               | F4      |
| RF-013 Gestionar ofertas              | HU-09               | F4      |
| RF-014 Gestionar métricas             | HU-21               | F9      |
| RF-015 Gestionar pedidos              | HU-18               | F7      |
| RF-16 Iniciar sesión                  | HU-02               | F2      |
| RF-17 Recuperar contraseña            | HU-03               | F2      |
| RF-18 Registrarse                     | HU-01               | F2      |
| RF-020 Consultar logs administrativos | HU-22               | F9      |
| RNF-001 Diseño responsive             | Transversal         | F1, F10 |
| RNF-002 Disponibilidad 24/7           | Transversal         | F1, F10 |
| RNF-003 Seguridad                     | Transversal         | F1, F10 |
| RNF-004 Rendimiento                   | Transversal         | F1, F10 |

La trazabilidad deberá actualizarse cuando se ajusten los requerimientos, se redefinan los casos de uso o se modifiquen los criterios de aceptación.

## 21. Observaciones pendientes de validación

* Definir los filtros exactos de RF-003.
* Precisar los controles y criterios de seguridad de RNF-003.
* Establecer métricas medibles para RNF-004.
* Definir los objetivos y mecanismos operativos para RNF-002.
* Confirmar las reglas de autenticación requeridas para comprar.
* Determinar el alcance de los datos de entrega y el mecanismo de seguimiento de envíos.
* Confirmar cómo se resolverán los estados pendientes, cancelados y rechazados de Mercado Pago.
* Determinar el alcance de los logs, métricas y recomendaciones para la primera entrega.
* Validar las prioridades con los interesados y ajustar las HU según el alcance acordado.

Esta planificación constituye una primera versión de trabajo. Las historias propuestas deben validarse contra las especificaciones completas de los casos de uso, las reglas de negocio y la selección tecnológica antes de convertirse en el backlog definitivo.
