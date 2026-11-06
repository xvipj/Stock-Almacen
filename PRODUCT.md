# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Personal de una tienda de ropa que gestiona el almacén: quien recibe mercancía, atiende el mostrador y hace conteos físicos. Trabaja en un solo local, en español (Colombia), y necesita responder rápido "¿cuánto hay de esta talla y este color?" y "¿qué se movió y quién lo registró?".

Los usuarios entran con una cuenta creada por un administrador; no hay registro público. El superusuario administra cuentas y categorías desde `/admin/`.

*Supuesto derivado del repositorio, no confirmado por el usuario:* el MVP no distingue roles operativos (bodega, vendedor, comprador); toda cuenta autenticada puede crear, editar y eliminar productos, variantes y movimientos.

## Product Purpose

Stock Almacén controla el inventario de una tienda de ropa a nivel de variante (producto + talla + color). Permite mantener el catálogo, registrar entradas, salidas y ajustes por conteo físico, y ver de un vistazo el stock total, las variantes por debajo de su mínimo y los últimos movimientos.

El proyecto tiene además un propósito declarado de ejemplo didáctico: mostrar cómo se organiza una aplicación Django por apps con una UI legible, sin dependencias más allá de Django.

El éxito es que el stock mostrado siempre coincida con la realidad física y que cualquier diferencia se pueda rastrear hasta un movimiento concreto, su usuario, su nota y su fecha.

## Positioning

El stock no se guarda en ninguna columna: se calcula recorriendo el historial cronológico de movimientos de cada variante. Un `AJUSTE` fija el valor absoluto tras un conteo físico; una `SALIDA` que dejaría stock negativo se rechaza. Por eso no existe la deriva típica entre "el número del sistema" y "lo que hay en la bodega": si el número está mal, hay un movimiento equivocado que se puede encontrar y corregir.

## Operating Context

- Tienda de ropa con tallas (S–L, 30–34, "Única") y colores como ejes de inventario; un producto sin variantes no tiene stock.
- Flujo real: catálogo → variantes → movimientos → indicadores.
- Los movimientos llevan nota libre para proveedor, motivo del ajuste o referencia de la venta (mostrador, pedido online, liquidación).
- El historial se consulta con filtros por rango de fechas, tipo y producto, en páginas de 20.
- El dashboard es la pantalla de inicio tras el login y resume productos activos, unidades totales, variantes con stock bajo y los últimos 10 movimientos.
- Uso local en un solo proceso (`runserver`), con SQLite y caché en memoria; el resumen del dashboard se guarda 60 segundos y se invalida por señales al cambiar productos, variantes o movimientos.
- Precios en pesos colombianos, interfaz en español (`es-co`, `America/Bogota`).
- Datos de demostración idempotentes (`seed_demo`): 4 categorías, 7 productos (uno inactivo), 14 variantes y movimientos distribuidos en el tiempo.

## Capabilities and Constraints

Confirmado en el código:

- CRUD de productos y variantes; las categorías solo se crean y editan en el admin de Django.
- Búsqueda de productos por nombre, SKU o marca, filtro por categoría y paginación.
- Ficha de producto con stock por variante, alerta de stock bajo e historial reciente.
- Registro de `ENTRADA`, `SALIDA` y `AJUSTE` en una transacción con bloqueo (`select_for_update`); validación también fuera de los formularios porque `StockMovement.save()` llama a `full_clean()`.
- Stock bajo cuando `stock_actual <= stock_minimo`.
- Login obligatorio en todas las vistas del MVP; logout por POST; sin registro público.
- Admin de Django con todos los modelos, filtros, búsquedas, inline de variantes y títulos en español.
- UI en plantillas Django + una sola hoja CSS; sin Bootstrap, Tailwind, framework de JavaScript, npm ni paso de build; sin JavaScript propio.
- Dirección de imports deliberada (`catalog.models -> inventory.stock`, `inventory.models -> catalog.models`), con `inventory/stock.py` libre de modelos.
- Datos normalizados en formularios: SKU y talla en mayúsculas, color en formato título.

Límites y decisiones abiertas:

- Es un MVP para desarrollo local: `DEBUG=True`, SQLite, `LocMemCache` de un solo proceso, credenciales demo documentadas en el README. No hay compromiso de despliegue ni de producción.
- *Sin decidir:* roles y permisos por función, multi-sucursal, compras/proveedores, códigos de barras, devoluciones, integración con punto de venta, exportación de reportes y endurecimiento de seguridad para producción.

## Brand Commitments

- Nombre del producto: **Stock Almacén**; marca gráfica "SA" en la barra lateral.
- Interfaz, mensajes y nombres de dominio en español; tono operativo y directo, en segunda persona informal ("Hola, …", "tu almacén"), sin jerga técnica en las pantallas.
- Terminología estable: producto, variante, categoría, entrada, salida, ajuste, stock mínimo, stock bajo, movimiento.
- Moneda mostrada con símbolo `$` y dos decimales; fechas en español.

## Evidence on Hand

- `README.md`: flujos, rutas, reglas de stock, modelo de datos, caché, credenciales demo y checklist de aceptación.
- `inventory/management/commands/seed_demo.py`: catálogo de demostración realista (Camisa Oxford, Jean Recto, Chaqueta Cortavientos, etc.) con notas de movimientos verosímiles.
- `db.sqlite3`: base local con datos demo (ignorada por git).
- Sin testimonios, clientes reales, métricas de negocio, prensa ni material de marketing. No fabricar ninguno.

## Product Principles

1. **El historial es la verdad.** El stock se deriva de los movimientos; nunca se almacena ni se edita directamente.
2. **Impedir estados imposibles en la capa de datos.** Las reglas (salidas sin stock, cantidades inválidas, unicidad talla + color) se validan en el modelo, no solo en la interfaz.
3. **Velocidad para la tarea de mostrador.** Responder qué hay, qué falta y qué se movió en pocos segundos, con etiquetas claras y alertas visibles.
4. **Legibilidad y bajo peso.** Django, plantillas y un solo CSS; cada pieza debe seguir sirviendo de ejemplo comprensible.
5. **Honestidad de alcance.** Lo que es demo local se presenta como demo local; no se insinúan capacidades de producción.
