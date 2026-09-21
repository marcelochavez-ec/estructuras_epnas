# Modulo EPNAS 01

## 1. Nombre del modulo

EPNAS 01 - Aplicacion web Django para la seccion S03.

## 2. Objetivo funcional

1. Registrar formularios de la seccion S03: Acceso y Movilizacion.
2. Leer catalogos desde PostgreSQL para renderizar listas desplegables.
3. Guardar cabecera y respuesta S03 con integridad relacional.
4. Exponer la aplicacion con Django, Gunicorn y Nginx mediante Docker.

## 3. Ubicacion de archivos modificados o creados

1. `02_SOFT_EPNAS/epnas_01/epnas_01/settings.py`
2. `02_SOFT_EPNAS/epnas_01/docker-compose.yml`
3. `02_SOFT_EPNAS/epnas_01/.env.example`
4. `02_SOFT_EPNAS/epnas_01/README.md`
5. `02_SOFT_EPNAS/epnas_01/docs/modulos/epnas_01.md`

## 4. Flujo general paso a paso

1. El usuario inicia sesion con autenticacion Django.
2. La vista de inicio lista los formularios registrados por el usuario autenticado.
3. El usuario abre el formulario S03 para crear o editar un registro.
4. El formulario carga opciones activas desde `formulario_opcion`.
5. Al guardar, se crea o actualiza la cabecera en `epnas_formulario`.
6. La respuesta operacional se guarda en `respuesta_s03`.
7. El usuario puede revisar el detalle del formulario guardado.

## 5. Entradas del modulo

1. Variables de entorno Django: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`.
2. Variables de entorno PostgreSQL: `EPNAS_DB_NAME`, `EPNAS_DB_USER`, `EPNAS_DB_PASSWORD`, `EPNAS_DB_HOST`, `EPNAS_DB_PORT`, `EPNAS_DB_SCHEMA`.
3. Tablas de catalogo en PostgreSQL: `epnas.formulario_seccion`, `epnas.formulario_variable`, `epnas.formulario_opcion`, `epnas.formulario_validacion`.
4. Usuario autenticado de Django.
5. Campos S03 enviados desde el formulario web.

## 6. Salidas del modulo

1. Registros en `epnas.epnas_formulario`.
2. Registros en `epnas.respuesta_s03`.
3. Pantalla de inicio con formularios recientes.
4. Pantalla de detalle de formulario.
5. Panel administrativo Django Unfold.
6. Logs normales de Django, Gunicorn y Nginx.

## 7. Fuentes de datos utilizadas

1. PostgreSQL, base configurada en `EPNAS_DB_NAME`.
2. Schema configurado en `EPNAS_DB_SCHEMA`, por defecto `epnas`.
3. Tablas principales: `epnas.formulario_opcion`, `epnas.epnas_formulario`, `epnas.respuesta_s03`.

## 8. Reglas de negocio aplicadas

1. Cada formulario pertenece al usuario autenticado que lo crea.
2. Los campos catalogados deben apuntar a opciones existentes y activas.
3. La respuesta S03 mantiene relacion uno a uno con la cabecera del formulario.
4. `s03_am05` admite valores numericos no negativos.
5. La aplicacion usa `search_path` PostgreSQL con el schema EPNAS y `public`.

## 9. Logica UI

1. `templates/base.html` define navegacion, autenticacion y layout general.
2. `templates/registration/login.html` muestra el acceso al sistema.
3. `templates/epnas/inicio.html` lista formularios recientes del usuario.
4. `templates/epnas/s03_form.html` contiene el formulario de captura S03.
5. `templates/epnas/s03_detalle.html` muestra la revision del registro guardado.
6. `static/epnas/css/app.css` concentra los estilos visuales.

## 10. Logica server

1. `epnas/views.py` controla inicio, creacion, edicion, detalle y healthcheck.
2. `epnas/forms.py` define campos y validaciones del formulario S03.
3. `epnas/services.py` encapsula el guardado transaccional.
4. `epnas/models.py` define catalogos, cabecera y respuesta.
5. `epnas/management/commands/cargar_catalogo_s03.py` carga catalogos de forma idempotente.
6. `scripts/init_db.py` prepara el schema configurado.

## 11. Consultas SQL o logica ETL relevante

1. `sql/estructura_epnas.sql` documenta la estructura relacional esperada.
2. Django ORM consulta opciones activas para poblar los campos `select`.
3. Las migraciones crean tablas, llaves foraneas, restricciones y relaciones.
4. El comando `cargar_catalogo_s03` inserta o actualiza seccion, variables, opciones y validaciones.

## 12. Dependencias

1. Python y Django 5.2 LTS.
2. `django-unfold`.
3. `psycopg`.
4. `gunicorn`.
5. `whitenoise`.
6. Docker, Docker Compose y Nginx para despliegue local contenerizado.

## 13. Validaciones realizadas

1. Se reviso que las credenciales no queden escritas directamente en `settings.py`.
2. Se agrego `.env.example` sin valores sensibles.
3. Se agregaron variables de entorno en `docker-compose.yml`.
4. Se mantuvo el schema por variable `EPNAS_DB_SCHEMA`.

## 14. Pruebas sugeridas o ejecutadas

1. Ejecutada: revision estatica de archivos y busqueda de cadenas sensibles antes de preparar el commit.
2. Sugerida: crear `.env` local con credenciales reales.
3. Sugerida: ejecutar `docker compose up --build -d`.
4. Sugerida: ejecutar `docker compose exec web python manage.py test`.
5. Sugerida: validar ingreso, creacion y edicion de un formulario S03.

## 15. Riesgos, supuestos y consideraciones de rendimiento

1. Si `.env` no contiene credenciales reales, la aplicacion inicia configurada pero no podra conectarse a PostgreSQL.
2. El contenedor requiere conectividad hacia el host PostgreSQL institucional.
3. Las consultas de catalogos deben mantenerse filtradas por opciones activas para evitar listas innecesarias.
4. La carga de catalogos es idempotente y debe ejecutarse despues de migraciones.

## 16. Cambios realizados en esta tarea

1. Se reemplazaron credenciales hardcodeadas por variables de entorno.
2. Se creo `.env.example` como plantilla segura.
3. Se actualizo `docker-compose.yml` para pasar configuracion desde el entorno.
4. Se actualizo el README con el nuevo esquema de configuracion.
5. Se documento el modulo para la sincronizacion completa del proyecto en GitHub.

## 17. Pendientes o recomendaciones futuras

1. Rotar las credenciales que estuvieron expuestas en commits previos.
2. Evaluar limpieza de historial Git si el repositorio se comparte fuera del entorno autorizado.
