# Sistema de Gestión de Inventario

Aplicación web académica para registrar y administrar productos, desarrollada para la actividad de Arquitectura y Aseguramiento de Calidad de Software. El proyecto aplica la arquitectura MVT de Django, persistencia en SQLite y validaciones del lado del servidor.

## Funcionalidades

- Registrar productos con código, nombre, descripción, categoría, precio y stock.
- Listar el inventario y buscar por coincidencias parciales de nombre o código.
- Consultar el detalle de un producto y su fecha de registro.
- Editar los datos de productos existentes.
- Eliminar productos mediante una pantalla de confirmación y envío por POST.
- Administrar categorías y productos desde Django Admin.
- Interfaz adaptable con Bootstrap: listado, creación, detalle, edición y eliminación.

El CRUD de productos no requiere inicio de sesión. El panel `/admin/` sí requiere un usuario administrador. No se implementan roles ni autenticación adicional para el CRUD.

## Tecnologías y requisitos del entorno

| Componente | Uso |
| --- | --- |
| Python 3.14 | Versión disponible en el entorno actual |
| Django 5.2.10 | Framework y ORM; versión fijada en `requirements.txt` |
| SQLite | Base de datos local en `db.sqlite3` |
| Bootstrap 5.3.8 | Estilos mediante CDN |
| HTML y CSS | Plantillas y personalización visual |

Django 5.2.10 es compatible con Python 3.14. Consulta la [documentación oficial de compatibilidad](https://docs.djangoproject.com/en/5.2/faq/install/).

Se necesita conexión a internet para instalar dependencias y cargar Bootstrap desde el CDN. SQLite no requiere instalar un servidor de base de datos separado.

## Arquitectura

El sistema es un **monolito modular**: un único proyecto Django con la aplicación interna `inventario` y una base de datos SQLite. Las carpetas del proyecto y de la aplicación no representan microservicios.

Se utiliza el patrón **MVT (Model–View–Template)**:

- **Model:** `models.py` define categorías, productos y sus reglas de validación.
- **View:** `views.py` procesa solicitudes mediante vistas genéricas de Django y consultas del ORM.
- **Template:** las plantillas HTML presentan los datos y formularios.
- **Formularios:** `forms.py` contiene un `ModelForm` reutilizado para crear y editar productos.
- **Rutas:** las URLs principales incluyen las de la app mediante el namespace `inventario`.

```text
gestion-inventario-django/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3
├── gestion_inventario/          # Configuración global
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── inventario/                 # Funcionalidad del inventario
    ├── models.py
    ├── forms.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    ├── tests.py
    ├── migrations/
    ├── templates/inventario/
    └── static/inventario/css/
```

## Modelo de datos

### Categoría

Tiene un nombre obligatorio y único, de hasta 100 caracteres, y una descripción opcional. Una categoría puede estar asociada a varios productos.

### Producto

| Campo | Regla |
| --- | --- |
| `codigo` | Obligatorio, único y de hasta 20 caracteres |
| `nombre` | Obligatorio, de hasta 150 caracteres |
| `descripcion` | Obligatoria en el formulario |
| `categoria` | Relación obligatoria con una categoría existente |
| `precio` | Decimal, hasta 10 dígitos totales y 2 decimales; mínimo 0.01 |
| `stock` | Entero mayor o igual que 0 |
| `fecha_creacion` | Fecha y hora automáticas al crear el registro |

Ambos modelos tienen un identificador automático `id`. Los productos se ordenan por fecha de creación descendente. La relación con categoría usa `on_delete=CASCADE`: eliminar una categoría también elimina sus productos asociados.

La migración `0002_producto_descripcion` agrega la descripción y deja vacía la de los productos que ya existían. Esos registros se pueden completar desde la edición.

## Instalación y ejecución

Descarga o clona el repositorio y abre una terminal en su carpeta raíz, donde se encuentra `manage.py`.

### Windows (PowerShell)

Estos comandos usan directamente el ejecutable del entorno virtual, sin necesidad de activar scripts de PowerShell:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

### Linux o macOS

```bash
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py createsuperuser
.venv/bin/python manage.py runserver
```

`createsuperuser` solicita las credenciales de forma interactiva; el proyecto no define credenciales predeterminadas. Si ya cuentas con un administrador, puedes omitir ese paso.

Abre el listado en [http://127.0.0.1:8000/](http://127.0.0.1:8000/). Para detener el servidor, presiona `Ctrl + C`.

### Preparar las categorías

Antes de registrar el primer producto:

1. Ingresa a [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) con el superusuario.
2. En **Categorías**, crea al menos una categoría.
3. Regresa al listado y selecciona **Nuevo producto**.

Las categorías creadas estarán disponibles en el selector del formulario. No existe una pantalla pública independiente para gestionar categorías.

## Rutas principales

| Ruta | Función |
| --- | --- |
| `/` | Listado de productos |
| `/?q=texto` | Búsqueda por nombre o código |
| `/productos/nuevo/` | Crear producto |
| `/productos/<id>/` | Consultar detalle |
| `/productos/<id>/editar/` | Editar producto |
| `/productos/<id>/eliminar/` | Confirmar eliminación; POST realiza el borrado |
| `/admin/` | Administración de Django |

Reemplaza `<id>` por el identificador real de un producto.

## Calidad y seguridad

- Consultas mediante el ORM, sin SQL construido manualmente.
- Formularios `ModelForm` con validación de campos y unicidad.
- Tokens CSRF en los formularios POST y middleware CSRF habilitado.
- Confirmación previa a la eliminación; visitar la pantalla con GET no borra registros.
- Respuesta 404 para productos inexistentes mediante las vistas genéricas.
- Escape automático de contenido en las plantillas de Django.
- Reutilización de plantilla base y formulario de creación/edición.
- `select_related("categoria")` en el listado para evitar una consulta adicional por categoría de cada producto.

La configuración actual corresponde al desarrollo local: incluye `DEBUG=True` y una clave de desarrollo en `settings.py`. El CRUD público y esta configuración no constituyen una configuración lista para publicación en internet.

## Requisitos y estado

| Requisito | Implementación o verificación pendiente |
| --- | --- |
| RF01: registrar productos | Formulario con los campos definidos, incluida descripción |
| RF02: consultar e inventariar | Listado, detalle y búsqueda por nombre o código |
| RF03: actualizar productos | Formulario de edición con datos precargados |
| RF04: eliminar productos | Confirmación y eliminación por POST |
| RNF01: validar precio y stock | Precio mínimo 0.01; stock permite 0. El equipo debe confirmar si “positivo” exige stock estrictamente mayor que 0 |
| RNF02: mantenibilidad y MVT | Separación entre modelos, vistas, formularios, rutas y plantillas |
| RNF03: respuesta inferior a 2 segundos | Listado optimizado con `select_related`; el umbral aún debe medirse con datos y entorno definidos |
| RNF04: portabilidad | SQLite y entorno virtual; requiere una versión de Python compatible con Django, no cualquier versión |

## Comprobaciones y pruebas

Desde la raíz del proyecto en Windows:

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py showmigrations
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe manage.py test inventario
```

En Linux/macOS, reemplaza `.\.venv\Scripts\python.exe` por `.venv/bin/python`.

El archivo `inventario/tests.py` contiene seis pruebas: listado, creación válida, rechazo de precio cero, edición, búsqueda por código y eliminación con confirmación. Django ejecuta estas pruebas en una base de datos de prueba separada.

Estado de verificación al redactar este README:

- `check` no reportó problemas y no se detectaron cambios de modelo sin migración.
- Se aplicó la migración de descripción a la base local.
- Se comprobó la resolución de rutas y el renderizado de las plantillas, incluidos los errores visuales del formulario.
- La compatibilidad de Django 5.2.10 con Python 3.14 permite ejecutar el administrador y la suite de pruebas en el entorno actual.
- Quedan pendientes la verificación completa en navegador, las capturas y la medición del tiempo de respuesta.

### Recorrido manual sugerido

1. Crear una categoría desde el administrador.
2. Registrar un producto con datos válidos y comprobar que aparece en el listado.
3. Buscarlo por nombre y por código.
4. Abrir su detalle y verificar todos los datos.
5. Editarlo, guardar y recargar para comprobar la persistencia.
6. Intentar enviar campos vacíos, código duplicado, precio cero y stock negativo.
7. Abrir la confirmación de eliminación, cancelar y comprobar que el producto permanece.
8. Confirmar la eliminación y verificar que desaparece del listado.
9. Consultar una URL con un identificador inexistente y comprobar la respuesta 404.

## Referencias técnicas

- [Documentación de Django 5.0](https://docs.djangoproject.com/en/5.0/)
- [ModelForm de Django](https://docs.djangoproject.com/en/5.0/topics/forms/modelforms/)
- [Pruebas en Django](https://docs.djangoproject.com/en/5.0/topics/testing/)
- [Bootstrap 5.3](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
- [Documentación de SQLite](https://www.sqlite.org/docs.html)
