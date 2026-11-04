# Stock Almacén

MVP de un sistema de stock de ropa hecho con **Django 6.1.3**, **SQLite** y **LocMemCache**. La interfaz está construida únicamente con plantillas de Django, HTML y CSS puro: sin Bootstrap, Tailwind, frameworks de JavaScript ni servicios externos.

El objetivo del proyecto es doble: cubrir un flujo real de inventario (catálogo → variantes → movimientos → indicadores) y servir como ejemplo legible para aprender cómo se organiza un proyecto Django por aplicaciones.

---

## 1. Inicio rápido

### Requisitos

- Python 3.12 o superior (probado con **Python 3.14.3**).
- Django 6.1.3, la única dependencia.
- No hace falta Redis, Celery, Memcached ni ningún servicio aparte.

### Opción A: el proyecto ya está listo

Esta entrega incluye `db.sqlite3` migrada, el superusuario y los datos de demostración. Solo hay que activar el entorno y arrancar:

```powershell
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

Abre <http://127.0.0.1:8000/>.

**Credenciales de demostración**

| Usuario | Contraseña | Acceso |
|---|---|---|
| `admin` | `Admin12345!` | Panel completo + `/admin/` |

> Cambia esa contraseña si vas a usar el proyecto fuera de tu equipo local:
> `python manage.py changepassword admin`

### Opción B: instalar desde cero

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install django
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo
python manage.py runserver
```

Si PowerShell bloquea la activación:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

También puedes instalar la versión exacta usada:

```powershell
pip install -r requirements.txt
```

### Recrear la base de datos desde cero

Con el servidor detenido:

```powershell
Remove-Item db.sqlite3
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo
```

---

## 2. Estructura de carpetas

```text
Stock-Almacen/
├── manage.py
├── db.sqlite3                  # SQLite (ya migrada y con datos demo)
├── requirements.txt
├── README.md
├── .gitignore
│
├── config/                     # Configuración global del proyecto
│   ├── settings.py             # Apps, idioma, zona horaria, caché, login
│   ├── urls.py                 # Rutas raíz y títulos del admin
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/                   # Autenticación
│   ├── forms.py                # LoginForm con textos en español
│   ├── urls.py                 # LoginView y LogoutView
│   ├── templates/accounts/
│   │   └── login.html
│   └── ...
│
├── catalog/                    # Catálogo de productos
│   ├── models.py               # Category, Product, Variant
│   ├── forms.py                # ProductForm, VariantForm
│   ├── views.py                # CRUD + búsqueda + filtro
│   ├── urls.py
│   ├── admin.py
│   ├── signals.py              # Invalida la caché del dashboard
│   ├── templates/catalog/
│   │   ├── product_list.html
│   │   ├── product_detail.html
│   │   ├── product_form.html
│   │   ├── product_confirm_delete.html
│   │   ├── variant_form.html
│   │   └── variant_confirm_delete.html
│   └── ...
│
├── inventory/                  # Movimientos y cálculo de stock
│   ├── models.py               # StockMovement
│   ├── stock.py                # Regla de cálculo del stock
│   ├── services.py             # Registrar movimiento en transacción
│   ├── forms.py                # Movimiento + filtros del historial
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── signals.py              # Invalida la caché al mover stock
│   ├── management/commands/
│   │   └── seed_demo.py        # Datos de demostración
│   ├── templates/inventory/
│   │   ├── movement_list.html
│   │   └── movement_form.html
│   └── ...
│
├── dashboard/                  # Página de inicio e indicadores
│   ├── views.py                # cache.get / cache.set
│   ├── urls.py
│   ├── templates/dashboard/
│   │   └── home.html
│   └── ...
│
├── templates/                  # Plantillas globales
│   ├── base.html               # Layout con sidebar, topbar y mensajes
│   └── partials/
│       └── form_fields.html    # Campos de formulario reutilizables
│
├── static/
│   └── css/
│       └── app.css             # Todo el diseño, sin frameworks
│
└── venv/                       # Entorno virtual (no versionar)
```

---

## 3. Qué hace cada app

### `accounts`

Gestiona la entrada y salida de usuarios usando el sistema de autenticación de Django.

- `LoginView` y `LogoutView` oficiales, sin registro público.
- Los usuarios se crean desde `/admin/`.
- Todas las vistas del MVP usan `LoginRequiredMixin`; el dashboard usa `login_required`.
- `LOGIN_URL`, `LOGIN_REDIRECT_URL` y `LOGOUT_REDIRECT_URL` están en `config/settings.py`.
- El logout se envía por **POST** desde el menú lateral, como exige Django.

### `catalog`

Contiene el catálogo y sus combinaciones vendibles.

- **Category**: nombre único.
- **Product**: nombre, SKU único, categoría, marca opcional, precio, activo y fecha de creación.
- **Variant**: producto, talla, color y stock mínimo.
- Restricción única `producto + talla + color`.
- CRUD completo de productos y variantes.
- Búsqueda por nombre, SKU o marca y filtro por categoría.
- Las categorías se crean y editan desde el admin de Django; el MVP no incluye un CRUD público de categorías.
- Ficha de producto con stock por variante, alerta de stock bajo e historial reciente.

### `inventory`

Es la fuente de verdad del stock.

- **StockMovement**: variante, tipo (`ENTRADA`, `SALIDA`, `AJUSTE`), cantidad, nota, usuario y fecha.
- El stock **no se guarda ni se edita a mano**: se calcula recorriendo los movimientos.
- Una salida se rechaza si dejaría stock negativo.
- Vista para registrar movimientos y historial con filtros por fecha, tipo y producto.
- Cada movimiento invalida la caché del dashboard mediante una señal.

### `dashboard`

Página de inicio posterior al login.

Indicadores:

1. Productos activos.
2. Unidades totales en stock.
3. Variantes en o por debajo de su stock mínimo.
4. Últimos 10 movimientos.

Los indicadores se guardan 60 segundos en `LocMemCache` y se invalidan cuando cambia un producto, una variante o un movimiento.

---

## 4. Modelo de datos

```text
Category 1 ──── N Product 1 ──── N Variant 1 ──── N StockMovement N ──── 1 User
```

- Borrar un producto elimina en cascada sus variantes y sus movimientos.
- La categoría está protegida (`PROTECT`): no se puede borrar si tiene productos.
- El usuario de un movimiento está protegido (`PROTECT`) para conservar el historial.

### Reglas de stock

`inventory/stock.py` recorre los movimientos en orden cronológico:

| Tipo | Efecto |
|---|---|
| `ENTRADA` | Suma `cantidad`. |
| `SALIDA` | Resta `cantidad`. |
| `AJUSTE` | Fija el stock exacto a `cantidad` (conteo físico). |

Ejemplo:

```text
ENTRADA 10  → stock 10
SALIDA   4  → stock 6
AJUSTE   9  → stock 9
```

`StockMovement.clean()` calcula el stock disponible antes de aceptar una salida. Además, `StockMovement.save()` llama a `full_clean()` para que la regla se respete también desde el admin, el shell o un comando.

Una variante tiene **stock bajo** cuando:

```text
stock_actual <= stock_minimo
```

---

## 5. Caché local e invalidación

En `config/settings.py`:

```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "stock-almacen",
        "TIMEOUT": 60,
    }
}

DASHBOARD_CACHE_KEY = "dashboard:resumen"
DASHBOARD_CACHE_TIMEOUT = 60
```

El dashboard hace `cache.get(...)`; si no hay datos, calcula el resumen y hace `cache.set(..., timeout=60)`. La plantilla muestra si los datos vienen de caché o si se acaban de calcular.

Las señales de `catalog/signals.py` e `inventory/signals.py` borran la clave cuando se guarda o elimina un producto, una variante o un movimiento. Así los indicadores se actualizan de inmediato sin esperar los 60 segundos.

> `LocMemCache` vive en la memoria del proceso. Es ideal para un MVP de desarrollo y un solo proceso; si algún día se despliega con varios workers habría que revisar esa decisión.

---

## 6. Rutas principales

| URL | Vista | Descripción |
|---|---|---|
| `/accounts/login/` | `LoginView` | Inicio de sesión |
| `/accounts/logout/` | `LogoutView` | Cierre de sesión (POST) |
| `/` | Dashboard | Indicadores y últimos movimientos |
| `/catalogo/` | Catálogo | Búsqueda y filtro por categoría |
| `/catalogo/nuevo/` | Crear producto | Formulario de producto |
| `/catalogo/<id>/` | Detalle | Variantes, stock e historial |
| `/catalogo/<id>/variantes/nueva/` | Crear variante | Talla, color y mínimo |
| `/inventario/` | Historial | Filtros por fecha, tipo y producto |
| `/inventario/registrar/` | Registrar movimiento | Entrada, salida o ajuste |
| `/admin/` | Admin Django | Todos los modelos registrados |

---

## 7. Panel de administración

Todos los modelos están registrados con:

- `list_display`
- `list_filter`
- `search_fields`
- `VariantInline` dentro de `Product`
- `date_hierarchy` en productos y movimientos
- Títulos en español:

```python
admin.site.site_header = "Stock Almacén · Administración"
admin.site.site_title = "Stock Almacén"
admin.site.index_title = "Panel de administración"
```

Accede en <http://127.0.0.1:8000/admin/> con el superusuario.

---

## 8. Diseño

- Una sola hoja de estilos: `static/css/app.css`.
- Variables CSS en `:root` para color, radios, sombras y tipografía.
- Paleta reducida: índigo como acento, grises neutros y rojo/ámbar/verde solo para estados.
- Tipografía `system-ui`.
- Layout de sidebar fija + contenido principal con CSS Grid.
- Tarjetas, tablas con hover, badges, botones consistentes, formularios con errores visibles y mensajes de Django estilizados.
- Responsive: en móvil la sidebar se convierte en una barra superior con navegación horizontal.
- Login centrado y con el mismo lenguaje visual.
- `templates/base.html` es la base heredada por todas las páginas; `accounts/login.html` la extiende y reemplaza el bloque `layout`.
- Sin JavaScript propio: la navegación y los estados se resuelven con HTML y CSS.

---

## 9. Datos de demostración

```powershell
python manage.py seed_demo
```

El comando es idempotente:

- Crea 4 categorías: Camisas, Pantalones, Chaquetas y Accesorios.
- Crea 7 productos (uno inactivo) y 14 variantes.
- Registra entradas, salidas y un ajuste de ejemplo.
- Si una variante ya tiene movimientos, no vuelve a duplicarlos.

El resultado deja varias variantes en stock bajo para que se vea la alerta visual desde el primer inicio.

---

## 10. Validación

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

La suite incluida comprueba:

- Protección por login.
- Creación de productos y normalización de SKU.
- Unicidad de talla + color por producto.
- Entradas y salidas actualizando el stock.
- Rechazo de salidas que dejarían stock negativo.
- Ajustes que fijan el stock exacto.
- Invalidación de la caché al registrar un movimiento.
- Dashboard usando caché y refrescándose tras un movimiento.

Resultado esperado: **8 tests OK** y `System check identified no issues`.

---

## 11. Cómo se construyó (comandos oficiales)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install django
django-admin startproject config .
python manage.py startapp accounts
python manage.py startapp catalog
python manage.py startapp inventory
python manage.py startapp dashboard
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo
python manage.py check
python manage.py test
python manage.py runserver
```

Las carpetas `templates/`, `static/` y `management/commands/` se crearon a mano porque Django no las genera con `startapp`; son ubicaciones convencionales del framework.

---

## 12. Dónde mirar si quieres aprender

| Quiero entender... | Archivo |
|---|---|
| La configuración global | `config/settings.py` |
| Las rutas y el admin | `config/urls.py` |
| Un CRUD con vistas basadas en clases | `catalog/views.py` |
| Relaciones y restricciones | `catalog/models.py` |
| Una regla de negocio aislada | `inventory/stock.py` |
| Validación de un modelo | `inventory/models.py` |
| Una transacción de escritura | `inventory/services.py` |
| Señales e invalidación de caché | `inventory/signals.py` |
| Caché con `get` / `set` | `dashboard/views.py` |
| Un layout reutilizable | `templates/base.html` |
| Estilos y responsive | `static/css/app.css` |
| Un comando de gestión | `inventory/management/commands/seed_demo.py` |

---

## 13. Problemas frecuentes

**`No module named django`**  
Activa el entorno virtual antes de cualquier comando: `.\venv\Scripts\Activate.ps1`.

**No puedo activar el entorno en PowerShell**  
Ejecuta `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` y vuelve a intentarlo.

**El puerto 8000 está ocupado**

```powershell
python manage.py runserver 8001
```

**Quiero empezar de nuevo con los datos demo**  
Detén el servidor, borra `db.sqlite3`, ejecuta `migrate`, crea el superusuario y corre `seed_demo`.

**Cambié productos y el dashboard tarda en reflejarlo**  
No debería: las señales invalidan la caché. Si modificas datos directamente con SQL, borra la caché reiniciando el servidor o espera 60 segundos.

---

## 14. Nota de alcance

Este proyecto es un **MVP para desarrollo local**. Usa `DEBUG=True`, SQLite y `LocMemCache`; para producción habría que configurar `ALLOWED_HOSTS`, `collectstatic`, un servidor WSGI/ASGI, cookies seguras y una caché compartida si se usan varios procesos. Nada de eso es necesario para el objetivo de aprendizaje de esta entrega.

---

## 15. Checklist de aceptación

- [x] `python manage.py check` sin errores.
- [x] Migraciones aplicadas sobre SQLite.
- [x] Login con superusuario y dashboard operativo.
- [x] CRUD de productos y variantes.
- [x] Registro de entradas, salidas y ajustes.
- [x] Stock calculado y protegido contra negativos.
- [x] Alertas de stock bajo.
- [x] Historial con filtros por fecha, tipo y producto.
- [x] Admin con todos los modelos, filtros, búsquedas e inline.
- [x] Caché LocMemCache de 60 s con invalidación por señales.
- [x] Sin dependencias externas distintas de Django.
- [x] Interfaz responsive con CSS puro.
