---
name: Stock Almacén
description: Sistema de inventario de ropa por variante, con el historial como única fuente de verdad.
colors:
  indigo-ink: "#4f46e5"
  indigo-ink-deep: "#4338ca"
  indigo-wash: "#eef2ff"
  indigo-hairline: "#c7d2fe"
  canvas: "#f5f6fa"
  surface: "#ffffff"
  surface-muted: "#f9fafb"
  surface-tint: "#fafbff"
  hairline: "#e7e9ef"
  hairline-strong: "#d6dae3"
  hairline-hover: "#c2c8d4"
  ink: "#141824"
  ink-soft: "#4b5563"
  muted: "#5f6674"
  muted-faint: "#6b7280"
  success: "#047857"
  success-strong: "#065f46"
  success-hairline: "#c7f0df"
  success-wash: "#ecfdf5"
  warning: "#b45309"
  warning-strong: "#92400e"
  warning-hairline: "#fde68a"
  warning-hairline-deep: "#f3dfa8"
  warning-surface: "#fffdf5"
  warning-wash: "#fffbeb"
  danger: "#dc2626"
  danger-strong: "#991b1b"
  danger-deep: "#b91c1c"
  danger-hairline: "#fecaca"
  danger-wash: "#fef2f2"
typography:
  headline:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"
    fontSize: "27px"
    fontWeight: 680
    lineHeight: 1.15
    letterSpacing: "-0.03em"
  headline-compact:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"
    fontSize: "24px"
    fontWeight: 680
    lineHeight: 1.15
    letterSpacing: "-0.03em"
  title:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"
    fontSize: "21px"
    fontWeight: 680
    lineHeight: 1.2
    letterSpacing: "-0.025em"
  metric:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"
    fontSize: "34px"
    fontWeight: 680
    lineHeight: 1
    letterSpacing: "-0.035em"
  heading-sm:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"
    fontSize: "20px"
    fontWeight: 680
    lineHeight: 1.25
    letterSpacing: "-0.02em"
  stat:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"
    fontSize: "18px"
    fontWeight: 680
    lineHeight: 1.2
  subhead:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"
    fontSize: "16px"
    fontWeight: 650
    lineHeight: 1.3
    letterSpacing: "-0.015em"
  section-title:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"
    fontSize: "15px"
    fontWeight: 650
    lineHeight: 1.3
    letterSpacing: "-0.01em"
  body:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.5
  data:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"
    fontSize: "13.5px"
    fontWeight: 400
    lineHeight: 1.5
  control:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"
    fontSize: "13px"
    fontWeight: 500
    lineHeight: 1.4
  nav:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"
    fontSize: "14px"
    fontWeight: 600
    lineHeight: 1.3
  caption:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"
    fontSize: "12px"
    fontWeight: 600
    lineHeight: 1.35
  label:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"
    fontSize: "11px"
    fontWeight: 650
    lineHeight: 1.25
    letterSpacing: "0.1em"
  mono:
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
    fontSize: "11.5px"
    fontWeight: 400
    lineHeight: 1.4
  wordmark:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"
    fontSize: "10px"
    fontWeight: 650
    lineHeight: 1.1
    letterSpacing: "0.14em"
  wordmark-micro:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, Helvetica Neue, Arial, sans-serif"
    fontSize: "9px"
    fontWeight: 650
    lineHeight: 1.1
    letterSpacing: "0.14em"
rounded:
  control: "9px"
  small: "8px"
  chip: "6px"
  xs: "7px"
  nav: "10px"
  icon: "11px"
  brand: "12px"
  md: "14px"
  avatar: "15px"
  lg: "20px"
  pill: "999px"
  bar: "3px"
  circle: "50%"
spacing:
  space-1: "4px"
  space-2: "8px"
  space-3: "12px"
  space-4: "16px"
  space-5: "20px"
  space-6: "24px"
  space-7: "32px"
  space-8: "36px"
components:
  button-primary:
    backgroundColor: "{colors.indigo-ink}"
    textColor: "{colors.surface}"
    rounded: "{rounded.control}"
    padding: "9px 14px"
    typography: "{typography.data}"
  button-primary-hover:
    backgroundColor: "{colors.indigo-ink-deep}"
    textColor: "{colors.surface}"
    rounded: "{rounded.control}"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink-soft}"
    rounded: "{rounded.control}"
    padding: "9px 14px"
    typography: "{typography.data}"
  button-secondary-hover:
    backgroundColor: "{colors.surface-muted}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
  button-ghost:
    backgroundColor: transparent
    textColor: "{colors.muted}"
    rounded: "{rounded.control}"
    padding: "9px 14px"
  field-input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "9px 12px"
    height: "40px"
    typography: "{typography.data}"
  nav-link-active:
    backgroundColor: "{colors.indigo-wash}"
    textColor: "{colors.indigo-ink-deep}"
    rounded: "{rounded.nav}"
    padding: "10px 12px"
    typography: "{typography.data}"
  badge-warning:
    backgroundColor: "{colors.warning-wash}"
    textColor: "{colors.warning}"
    rounded: "{rounded.pill}"
    padding: "4px 9px"
    typography: "{typography.label}"
  freshness-chip:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.muted}"
    rounded: "{rounded.pill}"
    padding: "6px 10px"
    typography: "{typography.label}"
  search-input:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "9px 12px 9px 34px"
    height: "40px"
    typography: "{typography.data}"
  card:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.md}"
    padding: "22px"
  metric-card:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.md}"
    padding: "20px"
---

# Design System: Stock Almacén

## Overview

**Creative North Star: "El Mostrador Ordenado"**

El sistema se comporta como un mostrador bien llevado: nada decorativo compite con el dato, todo lo que se necesita para responder "¿cuánto hay?" está a la vista, y la superficie no finge ser otra cosa. La densidad es media-alta y deliberada: tablas de 13.5px, etiquetas de 11px en mayúsculas, filas de 14px de padding vertical y una sola acción primaria por pantalla. El espacio en blanco no se usa para respirar por respirar, sino para separar bloques de información que se leen en orden.

El color es un recurso escaso. Un único índigo de tinta marca la acción principal, la navegación activa y el ajuste; los estados hablan en tríadas teñidas (fondo suave + borde + texto oscuro) en lugar de bloques saturados. El resto del sistema es gris: un lienzo frío casi blanco, superficies blancas, hairlines de 1px y sombras tan bajas que se leen más como textura que como profundidad.

La tipografía no tiene familia propia: usa la del sistema operativo y se afina con peso y tracking negativo en los números grandes, tabular en toda cifra. Ese detalle —la pila del sistema, los números alineados, las micro-etiquetas en mayúsculas— es lo que separa la interfaz de una plantilla de dashboard genérica: se siente herramienta, no producto de marketing. La única excepción expresiva es la pantalla de acceso, con sus halos radiales índigo y dos círculos trazados; es el umbral, y por eso puede permitirse el gesto.

**Key Characteristics:**
- Un solo acento índigo, usado en menos de una décima parte de cualquier pantalla.
- Estructura por borde de 1px y relleno tonal; sombras casi imperceptibles.
- Cifras siempre tabulares, y siempre el elemento tipográfico más grande de su bloque.
- Radios suaves y anidados: 14px en contenedores, 9px en controles, 6–7px en micro-chips, 999px solo en píldoras y avatares.
- Micro-etiquetas en mayúsculas de 11px con tracking amplio; nunca en cuerpo de texto.
- Cero fuentes web, cero iconos de paquete: SVG en línea con trazo de 1.8.

## Colors

Paleta de un solo acento: índigo de tinta sobre una escala de grises fría, con tres estados semánticos que solo aparecen teñidos.

### Primary
- **Índigo de Tinta** (#4f46e5): el acento operativo. Botón primario, enlace activo, ítem de navegación seleccionado, iconos de indicador y el tipo `AJUSTE`. Es el único color con saturación alta en toda la interfaz.
- **Índigo de Tinta Profundo** (#4338ca): estado hover del botón primario y texto sobre fondos teñidos. Nunca se usa como fondo de área extensa.
- **Aguada Índigo** (#eef2ff): fondo del ítem de navegación activo, del icono de indicador, de la barra lateral de stock y de los badges `accent`. Funciona como "superficie seleccionada", no como decoración.
- **Hairline Índigo** (#c7d2fe): borde de los contenedores teñidos de índigo. Cierra la tríada sin agregar un cuarto tono.

### Neutral
- **Lienzo Frío** (#f5f6fa): fondo de la aplicación; también el fondo translúcido de la barra superior con desenfoque de 10px.
- **Superficie** (#ffffff): tarjetas, sidebar, barra superior sólida, campos de formulario y botones secundarios.
- **Superficie Apagada** (#f9fafb): cabeceras de tabla, pies de formulario, paginación, hover de filas y navegación, checkbox, previews de objeto.
- **Veladura de Fila** (#fafbff): el hover de las filas de tabla. Un blanco con una gota de índigo, apenas perceptible; no se usa en ningún otro sitio.
- **Hairline** (#e7e9ef): separador universal de 1px entre tarjetas, filas y secciones.
- **Hairline Reforzada** (#d6dae3): borde de campos de entrada y de botones secundarios; un paso más oscuro para indicar que el elemento es interactivo.
- **Hairline de Hover** (#c2c8d4): el borde secundario cuando el cursor está encima. Es el único paso de la escala de grises reservado a interacción.
- **Tinta** (#141824): texto principal, títulos y cifras. Es un gris azulado casi negro, nunca negro puro.
- **Tinta Suave** (#4b5563): cuerpo de tabla, etiquetas de formulario y texto de botones secundarios.
- **Gris Medio** (#5f6674): texto secundario, subtítulos, ayudas, cabeceras de tabla y notas. Es el gris funcional por defecto: 5.34:1 sobre el lienzo y 5.9:1 sobre blanco.
- **Gris Tenue** (#6b7280): el peldaño más claro permitido en texto real (4.83:1 sobre blanco); se usa en placeholders y metadatos de menor jerarquía, nunca sobre el lienzo.

### Semantic States
Cada estado es una tríada cerrada de tokens: `wash` (fondo), `hairline` (borde) y `strong` (texto). Nunca se mezclan pasos de familias distintas.

- **Verde Almacén** (#047857) con **Verde Profundo** (#065f46) sobre **Aguada Verde** (#ecfdf5) y **Hairline Verde** (#c7f0df): entradas de stock, estado "Activo"/"Disponible", confirmaciones y mensajes de éxito.
- **Ámbar de Reposición** (#b45309) con **Ámbar Profundo** (#92400e) sobre **Aguada Ámbar** (#fffbeb): stock bajo, stock mínimo y badges de advertencia. La tarjeta de alerta del dashboard añade dos pasos propios del mismo tono: **Hairline Ámbar** (#fde68a) para el borde del mensaje, **Hairline Ámbar Reforzada** (#f3dfa8) para píldoras y tarjeta, y **Superficie Ámbar** (#fffdf5) para el degradado de fondo.
- **Rojo Salida** (#dc2626) con **Rojo Profundo** (#991b1b) sobre **Aguada Roja** (#fef2f2) y **Hairline Roja** (#fecaca): salidas, eliminación, errores de formulario y zona de peligro. **Rojo Hover** (#b91c1c) es exclusivo del hover del botón sólido `danger`, siguiendo el mismo criterio que el índigo profundo en el botón primario.

### Named Rules
**The One Accent Rule.** El índigo se reserva para acción, selección y ajuste. Si un elemento no es clicable, no está seleccionado ni representa un ajuste, no lleva índigo. Su escasez es lo que lo hace legible como "esto se pulsa".

**The Tinted State Rule.** Un estado nunca se pinta como bloque sólido saturado. Siempre es tríada: fondo aguado, borde del mismo tono y texto oscuro del mismo tono. La única excepción son los botones `danger` y el botón primario, que sí son sólidos porque son acciones, no estados.

## Typography

**Display Font:** no existe; la jerarquía se construye con peso y escala.
**Body Font:** pila del sistema (`system-ui`, `-apple-system`, `Segoe UI`, `Roboto`, `Helvetica Neue`, `Arial`, sans-serif).
**Label/Mono Font:** monoespaciada del sistema (`ui-monospace`, `SFMono-Regular`, `Menlo`, `Consolas`), solo para SKU.

**Character:** la voz tipográfica es la del sistema operativo, sin fuentes descargadas. La personalidad viene del contraste entre micro-etiquetas de 11px en mayúsculas y cifras de 34px con tracking negativo: el mismo contraste que hay entre una etiqueta de estantería y el número escrito en ella.

### Hierarchy
La escala es cerrada; no se usan tamaños intermedios. De mayor a menor: 34, 27, 24, 21, 20, 18, 16, 15, 14, 13.5, 13, 12, 11.5, 11, 10 y 9px.

- **Metric** (680, 34px, 1, −0.035em): valor de los indicadores del dashboard y cifra de stock en la ficha de producto. Es la cifra más grande del sistema.
- **Headline** (680, 27px, 1.15, −0.03em): el `h1` de la barra superior, único por pantalla.
- **Headline compacta** (680, 24px): el mismo `h1` a 900px o menos, el `h1` de la tarjeta de acceso y la inicial del avatar de producto. Comparte tamaño porque nunca coinciden en pantalla.
- **Title** (680, 21px, 1.2, −0.025em): nombre del producto en su ficha y `h2` de la tarjeta de acceso.
- **Heading small** (680, 20px, 1.25, −0.02em): `h2` de la confirmación de borrado y el glifo del icono de peligro.
- **Stat** (680, 18px): cifra secundaria del hero de producto a tamaño completo y glifo de los estados vacíos.
- **Subhead** (650, 16px, −0.015em): nombre de la marca en la sidebar, cifra de stock en la lista de reposición y stat del hero a 480px o menos.
- **Section Title** (650, 15px, 1.3, −0.01em): cabecera de tarjeta, título de estado vacío y de nota lateral.
- **Body** (400, 15px, 1.5): párrafos de apoyo y texto corrido.
- **Data** (400–600, 13.5px, 1.5): cuerpo de tabla, campos de formulario y texto de interfaz. Es el tamaño dominante de la aplicación.
- **Nav** (600, 14px): ítems de la navegación lateral y `h3` de las notas laterales. A 900px o menos baja a 13px para convivir con la barra superior.
- **Control** (500, 13px): botones, labels de formulario, píldoras de stock, notas y metadatos de tabla. El escalón que separa "lo que se pulsa" de "lo que se lee".
- **Caption** (600, 12px): botón pequeño, chips y texto auxiliar dentro de tarjetas densas.
- **Label** (650–700, 11px, 0.07–0.14em, mayúsculas): eyebrows, cabeceras de tabla, labels de métrica, labels de filtro, badges y micro-etiquetas de navegación. Es el piso tipográfico del sistema: nada funcional baja de 11px. Máximo una línea; nunca un párrafo.
- **Mono** (400, 11.5px): exclusivamente el SKU dentro de un chip con borde, para que se lea como un código y no como prosa.
- **Excepción de marca**: el título del logo usa 16px (14px a 900px o menos) y el subtítulo "ALMACÉN" usa 10px (9px a 900px o menos). No es texto funcional: es parte del wordmark y no compite con ninguna etiqueta.

### Named Rules
**The Tabular Number Rule.** Toda cifra —stock, cantidades, precios, mínimos, métricas— lleva `font-variant-numeric: tabular-nums`. Los números se comparan en columna; si bailan, la tabla deja de servir.

**The Micro-Label Rule.** Las mayúsculas con tracking solo se usan en etiquetas de 11px que nombran un dato debajo o al lado. Nunca en titulares, botones, enlaces ni frases.

## Layout

El armazón es una rejilla de dos columnas: sidebar fija de 258px y contenido flexible. La sidebar es `sticky` a altura completa, con marca arriba, navegación agrupada por `General` / `Sistema` y usuario + cierre de sesión anclados al pie con `margin-top: auto`. El contenido se centra con un máximo de 1360px y padding de 24px arriba, 36px a los lados.

La barra superior es `sticky`, con fondo translúcido del lienzo al 90% y `backdrop-filter: blur(10px)`, y contiene eyebrow + `h1` + subtítulo a la izquierda y un grupo de acciones a la derecha, alineadas al borde inferior. Ese grupo es una rejilla de columnas `max-content` (buscador de 250px + chips + un único botón primario), no un flex con `wrap`: así el navegador mide el grupo por su contenido real y no parte la fila. Cuando no cabe junto al título, el grupo entero baja a una segunda línea alineada a la derecha. Cada pantalla declara exactamente un `h1`; las tarjetas usan `h2` y las notas laterales `h3`.

Dentro del contenido, las rejillas son de 18px de separación y las tarjetas apiladas de 24px de margen inferior. El dashboard usa `1fr / 340px` (tabla de movimientos + columna de stock bajo); los formularios usan `1fr / 320px` (formulario + notas laterales), y a 1120px ambas colapsan a una columna con las notas laterales en dos columnas. El ritmo de espacio sale de una escala de 4px: 4, 8, 12, 16, 20, 24, 32, 36.

Puntos de quiebre: 1120px (colapsan rejillas laterales), 900px (la sidebar pasa a barra superior horizontal; la navegación fluye en varias filas en lugar de desplazarse, para que ningún destino quede oculto), 760px (métricas y formularios a una columna, barra superior apilada, las tablas ocultan sus columnas secundarias: SKU, categoría, variantes, precio, nota y usuario), 480px (filtros a una columna, el tipo de movimiento se oculta en las tablas —el signo y el color ya lo dicen— y las acciones de confirmación pasan a ancho completo).

### Named Rules
**The 18/24 Rule.** Dentro de una rejilla, la separación es 18px; entre bloques apilados, 24px. No se inventan valores intermedios: si algo necesita más aire, cambia de bloque.

**The Sidebar Owns Navigation Rule.** Ninguna pantalla repite la navegación principal como pestañas o breadcrumbs clicables. El eyebrow (`Catálogo / Producto`) ubica, no navega.

## Elevation & Depth

El sistema es plano por defecto. La profundidad se comunica con borde de 1px y cambio de relleno tonal, no con sombra: una tarjeta es blanca sobre lienzo gris con hairline; una cabecera de tabla es `surface-muted`; un ítem activo es aguada índigo. Las tres sombras existentes son intencionalmente casi invisibles (`0 1px 2px` con 4% de alfa) y funcionan como textura, no como jerarquía.

La única elevación real es el umbral de acceso: la tarjeta de login lleva `0 24px 60px rgba(20, 24, 36, 0.1)` y radio de 20px, porque es una pantalla completa sin sidebar ni barra superior y necesita despegarse del fondo. El botón primario puede elevarse 1px al hover con un halo índigo, y el logo de marca lleva su propio halo fijo; nada más se mueve en Z.

### Shadow Vocabulary
- **Textura** (`box-shadow: 0 1px 2px rgba(20, 24, 36, 0.04)`): tarjetas, indicadores, hero de producto y botón primario en reposo. Se percibe como borde suave, no como sombra.
- **Reposo alto** (`box-shadow: 0 2px 8px rgba(20, 24, 36, 0.05)`): reservada; solo para elementos que deban leerse por encima de una superficie ya elevada.
- **Halo de acción** (`box-shadow: 0 5px 14px rgba(79, 70, 229, 0.22)`): hover del botón primario. Es la única sombra con color.
- **Umbral** (`box-shadow: 0 24px 60px rgba(20, 24, 36, 0.1)`): exclusiva de la tarjeta de login.

### Named Rules
**The Flat-by-Default Rule.** En la aplicación no hay sombras nuevas: si un bloque necesita separarse, se le da borde, fondo o espacio, no elevación. La sombra profunda pertenece al umbral de acceso.

**The Threshold Rule.** Los halos radiales índigo y los dos círculos trazados existen solo en la pantalla de login. Son el único gesto decorativo del sistema y no se trasladan al interior de la aplicación.

## Shapes

Lenguaje de esquina suave y consistente, con radios que se anidan: los contenedores grandes usan 14px, los controles 9px, la navegación 10px, los micro-elementos 6–7px y solo las píldoras y los avatares llegan a 999px o 50%. Las cajas cuadradas escalan con su tamaño (38px de icono → 11px; 40–44px de marca e icono vacío → 12px; 58px de avatar de producto → 15px; 48px de avatar en móvil → 14px), de modo que la curva se lee igual en todos los tamaños. Nada es cuadrado y nada es completamente redondeado salvo lo que representa una etiqueta o una persona.

Los bordes son siempre de 1px y siempre presentes en elementos interactivos; el borde es lo que declara "esto se puede tocar" cuando la sombra no lo hace. Las formas decorativas se limitan a círculos: el avatar de usuario (34px), el avatar de producto (58px), el punto de mensaje (7px) y el punto de caché (6px).

Los iconos son SVG en línea de 18px con trazo de 1.8, esquinas redondeadas y `currentColor`; dentro de botones bajan a 15px. No hay set de iconos externo, ni glifos de fuente, ni emojis salvo los símbolos tipográficos de los estados vacíos (`↕`, `◫`, `✓`), que funcionan como ilustración mínima.

### Named Rules
**The Nested Radius Rule.** El radio interior siempre es menor que el del contenedor: 9px dentro de 14px, 6px dentro de 9px. Un control con el mismo radio que su tarjeta se lee como un bloque pegado, no como un objeto dentro de otro.

## Components

### Buttons
- **Shape:** rectangular suave, 9px de radio (8px en la variante pequeña), padding `9px 14px`, texto de 13px con peso 600, gap de 8px para el icono.
- **Primary:** fondo índigo sólido, texto blanco, sombra de textura. Es la acción que la pantalla existe para permitir. Al hover oscurece a índigo profundo, gana un halo índigo y sube 1px; no cambia de tamaño.
- **Secondary:** fondo blanco, borde hairline reforzado, texto tinta suave. Al hover el fondo pasa a superficie apagada y el texto a tinta.
- **Ghost:** sin fondo ni borde, texto gris medio. Es el botón de las acciones de fila ("Ver", "Editar", "Movimiento") y de la navegación secundaria. Al hover gana fondo apagado.
- **Ghost danger / Danger:** el ghost danger lleva texto rojo y fondo aguado rojo al hover; el danger sólido se reserva para confirmar una eliminación.
- **Small:** `6px 9px`, 12px, radio 8px. Se usa dentro de tarjetas y tablas, nunca en la barra superior.
- **Focus:** `outline: 2px solid` índigo con `outline-offset: 2px` en todos los botones, enlaces, ítems de navegación y filas clicables.

### Badges
- **Style:** píldora de 999px, padding `4px 9px`, texto de 11px con peso 650, borde de 1px del mismo tono que el fondo aguado.
- **Semantics:** `accent` (ajuste, categoría), `success`/`entrada` (verde), `warning` (ámbar), `danger`/`salida` (rojo), `muted` (inactivo). El tipo de movimiento determina el color, no la fila.
- **Constraint:** un badge nunca contiene una acción; si es clicable, es un chip o un botón.

### Chips and Codes
- **Size chip:** talla en caja de 6px de radio, fondo apagado, borde hairline, mínimo 30px de ancho, peso 700. Se centra para que tallas de uno y dos dígitos alineen.
- **Stock pill:** caja de 7px de radio, mínimo 34px, cifra tabular de 12.5px con peso 650; la variante baja cambia a aguada ámbar con borde ámbar.
- **Code:** SKU en monoespaciada de 11.5px dentro de caja de 6px con borde y fondo apagado. Nunca se parte en dos líneas.
- **Freshness chip:** píldora con punto verde de 6px y un `<time>Actualizado HH:MM</time>` en 11px tabular. Declara cuándo se calculó el resumen (no si vino de caché: eso es un detalle de implementación, no información para la tienda).

### Search

- **Topbar search:** campo de 250px con lupa de 16px dentro del área de texto (padding izquierdo de 34px) que envía `GET` a `catalog:product_list` con `q`. Es global y vive en la barra superior de todas las pantallas menos el propio catálogo, donde ya existe el filtro local completo.
- **Filter search:** mismo control dentro de `.filters`; en el catálogo el grupo entero es una rejilla de columnas `max-content` para que "Filtrar" nunca caiga solo a una segunda fila.

### Cards / Containers
- **Corner Style:** 14px; las tarjetas laterales y de formulario comparten el mismo radio.
- **Background:** blanco sobre lienzo; la tarjeta de alerta y la nota de stock usan un degradado vertical muy leve desde su aguada hacia blanco al 70–80%.
- **Shadow Strategy:** textura únicamente (ver Elevation & Depth).
- **Border:** hairline de 1px; la tarjeta de peligro y la de alerta cambian el borde a su tono semántico.
- **Internal Padding:** 22px de cuerpo y 19px 22px de cabecera; en móvil baja a 17px y 16px 17px.

### Inputs / Fields
- **Style:** fondo blanco, borde hairline reforzado, 9px de radio, altura mínima de 40px, padding `9px 12px`, texto de 13.5px. Labels de 12.5px con peso 600 y asterisco rojo para obligatorios.
- **Focus:** el borde pasa a índigo y aparece un anillo de `0 0 0 3px rgba(79, 70, 229, 0.12)`; no se usa `outline`.
- **Error:** borde rojo y, al enfocar, anillo rojo al 10%; el mensaje va debajo en 12px rojo. El error de campo no reemplaza al label.
- **Checkbox:** contenedor propio con borde, fondo apagado y 9px de radio; la casilla va a la derecha del label y usa `accent-color` índigo.

### Navigation
- **Sidebar:** 258px, sticky, fondo blanco con borde derecho. La marca es un cuadrado de 40px con radio 12px, fondo índigo, "SA" en 12px con peso 750 y halo índigo.
- **Nav link:** 14px con peso 500, icono de 18px, 10px 12px de padding, radio 10px. Activo: fondo aguada índigo, texto índigo profundo con peso 650 y una barra de 3px al borde izquierdo.
- **Mobile:** a 900px la sidebar se convierte en barra superior; los labels de grupo desaparecen, los enlaces fluyen en varias filas (sin scroll horizontal, para que "Administración" nunca quede fuera de vista) y el chip de usuario se oculta, dejando marca y cierre de sesión.

### Signature: Metric Card
Tres por fila en el dashboard, 20px de padding. Arriba, un icono de 38px en caja de 11px de radio con fondo aguado y, a la derecha, una micro-etiqueta de contexto ("Catálogo", "Existencias"). Debajo, label de 11.5px en mayúsculas, cifra de 34px tabular y una línea de contexto de 11.5px. La tarjeta de stock bajo cambia a aguada ámbar con degradado y su cifra pasa a ámbar oscuro; la de todo en orden usa verde en el icono.

### Signature: Low-Stock List
Cabecera de tarjeta con el recuento ("5 variantes · 3 unidades por reponer") y un enlace "Volver al dashboard". Cada fila es una rejilla de cuatro zonas separadas por hairline: producto y variante (`talla / color`) a la izquierda; stock actual en píldora ámbar con `mín. N` al lado; un badge de déficit (`faltan N` o `en mínimo`); y un botón secundario pequeño que abre el formulario de movimiento con la variante precargada. En móvil la rejilla se reordena en dos filas (producto + stock, déficit + acción) y la cabecera apila el enlace debajo del recuento.

### Signature: Tables
Cabecera en mayúsculas de 11px con peso 700 sobre fondo apagado; filas de 14px 20px separadas por hairline, sin cebreado, con hover apenas teñido. La primera celda combina un título de 13.5px con peso 600 y un subtítulo de 11.5px gris. Las columnas numéricas se alinean a la derecha con cifras tabulares; las acciones de fila son botones ghost pequeños y nunca primarios. A 760px las columnas secundarias se ocultan por clase (`col-secondary`, `col-tipo`) antes que recurrir al desplazamiento horizontal.

### Signature: Auth Card
420px de ancho máximo, 34px 32px de padding, radio 20px, sombra de umbral, sobre un lienzo con dos halos radiales índigo y dos círculos trazados de 380–420px. La marca se centra, el kicker va en una caja de 6px con aguada índigo y el botón primario ocupa el ancho completo.

## Do's and Don'ts

### Do:
- **Do** mantener exactamente un `btn-primary` por pantalla, dentro de `topbar-actions` (`Registrar movimiento`, `Nuevo producto`, `Editar producto`).
- **Do** expresar estados como tríada teñida: fondo aguado + borde del tono + texto oscuro del tono.
- **Do** aplicar `tabular-nums` a toda cifra y alinear a la derecha las columnas numéricas con `class="num"`.
- **Do** usar las micro-etiquetas en mayúsculas de 11px con tracking de 0.07–0.14em para nombrar datos, nunca para frases.
- **Do** separar con hairline de 1px y relleno tonal antes de recurrir a una sombra.
- **Do** anidar radios: 9px dentro de 14px, 6px dentro de 9px.
- **Do** reutilizar los tokens de `:root` (`var(--accent)`, `var(--space-4)`, `var(--radius)`) en lugar de valores literales nuevos.
- **Do** usar SVG en línea de 18px con trazo 1.8 y `currentColor`; dentro de botones, 15px.
- **Do** dejar que la pantalla de login conserve sus halos y círculos como único gesto decorativo.

### Don't:
- **Don't** introducir un segundo color de acento, ni degradados de marca, ni modo oscuro.
- **Don't** usar sombras por encima de `0 2px 8px rgba(20, 24, 36, 0.05)` dentro de la aplicación; la sombra de 24px 60px es solo del umbral de login.
- **Don't** redondear botones, tarjetas o campos a 999px; la píldora es exclusiva de badges, chips de frescura y avatares.
- **Don't** convertir las acciones de fila en botones primarios o sólidos: son ghost pequeños para que la acción principal siga siendo única. La única excepción es la lista de reposición, donde el botón de fila es secundario porque esa pantalla existe para registrar el movimiento.
- **Don't** cargar fuentes web, paquetes de iconos, frameworks de CSS/JS ni pasos de build; el sistema es una sola hoja y plantillas Django.
- **Don't** usar mayúsculas con tracking en titulares, botones, enlaces o párrafos.
- **Don't** pintar un estado como bloque sólido saturado (salvo los botones de acción).
- **Don't** repetir la navegación principal dentro de la pantalla como pestañas o breadcrumbs clicables.
- **Don't** usar negro puro (`#000`) ni blanco puro como texto: la tinta es `#141824` y el texto claro es `#ffffff` solo sobre fondos sólidos.
