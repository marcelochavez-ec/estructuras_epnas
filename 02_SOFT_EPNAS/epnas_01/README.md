# EPNAS 01

Proyecto Django + Unfold + PostgreSQL + Gunicorn + Nginx para la **Sección S03: Acceso y Movilización**.

## 1. Arquitectura incluida

- Django 5.2 LTS.
- Django Unfold para el panel `/admin/`.
- PostgreSQL: base `productos_bm`, schema `epnas`.
- Modelo relacional normalizado con PK, FK, `UNIQUE`, `CHECK` y relación 1:1 cabecera/respuesta.
- Formulario web S03 con listas desplegables leídas desde `formulario_opcion`.
- Autenticación Django.
- Gunicorn como servidor WSGI.
- Nginx como reverse proxy.
- Docker / Docker Compose.
- Comando idempotente `cargar_catalogo_s03` para poblar catálogos.

## 2. Configuración PostgreSQL

La conexión se lee desde variables de entorno para evitar publicar credenciales en GitHub. Use `.env.example` como plantilla y cree un archivo local `.env`:

```bash
cp .env.example .env
```

Variables principales:

- `EPNAS_DB_NAME`: base PostgreSQL, por defecto `productos_bm`.
- `EPNAS_DB_SCHEMA`: schema PostgreSQL, por defecto `epnas`.
- `EPNAS_DB_USER`: usuario PostgreSQL.
- `EPNAS_DB_PASSWORD`: clave PostgreSQL.
- `EPNAS_DB_HOST`: host PostgreSQL.
- `EPNAS_DB_PORT`: puerto PostgreSQL, por defecto `5432`.
- `DJANGO_SECRET_KEY`: clave interna de Django.

## 3. Modelo ER implementado

```text
formulario_seccion 1 ── N formulario_variable
formulario_variable 1 ── N formulario_opcion
formulario_variable 1 ── N formulario_validacion
AUTH_USER 1 ── N epnas_formulario
epnas_formulario 1 ── 1 respuesta_s03
respuesta_s03 N ── 1 formulario_opcion (para cada variable select)
```

Tablas de negocio:

1. `formulario_seccion`
2. `formulario_variable`
3. `formulario_opcion`
4. `formulario_validacion`
5. `epnas_formulario`
6. `respuesta_s03`

Además, Django crea sus tablas internas de autenticación, sesiones, permisos y migraciones dentro del `search_path` configurado.

## 4. Levantar con Docker

Desde la carpeta raíz:

```bash
docker compose up --build -d
```

Abrir:

```text
http://localhost:8080/
```

El arranque realiza automáticamente:

1. creación/verificación del schema `epnas`;
2. `python manage.py migrate`;
3. carga/actualización del catálogo S03;
4. `collectstatic`;
5. arranque de Gunicorn;
6. Nginx expone el sistema en el puerto `8080`.

## 5. Crear usuario administrador

```bash
docker compose exec web python manage.py createsuperuser
```

Luego ingresar a:

```text
http://localhost:8080/admin/
```

## 6. Ejecución local sin Docker

Crear un entorno virtual e instalar dependencias:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/init_db.py
python manage.py migrate
python manage.py cargar_catalogo_s03
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

## 7. Flujo de datos

1. Django consulta `formulario_seccion` y `formulario_variable`.
2. Para cada variable `select`, consulta sus opciones activas en `formulario_opcion`.
3. El usuario registra la cabecera en `epnas_formulario`.
4. Las respuestas S03 se almacenan en `respuesta_s03`.
5. Los campos de selección guardan FK reales hacia `formulario_opcion`.
6. `s03_am05` se guarda como `NUMERIC(6,2)` y tiene restricción `>= 0`.

## 8. Catálogo S03 incluido

- `s03_am01`: Medio de transporte.
- `s03_am02`: Frecuencia de transporte.
- `s03_am03`: Número de proveedores de transporte.
- `s03_am04`: Costo mensual de pasajes.
- `s03_am05`: Tiempo de traslado en horas.
- `s03_am06`: Orden de vía principal.

Los catálogos son parametrizables desde PostgreSQL o desde el admin de Unfold. El formulario no tiene las opciones cerradas codificadas directamente en el HTML.

## 9. Punto importante de red

El contenedor debe tener conectividad hacia `10.64.100.191:5432`. Si el equipo donde se ejecuta Docker no está en la red institucional/VPN o PostgreSQL bloquea ese origen, la aplicación no podrá migrar ni iniciar.

## 10. Próximo crecimiento

La arquitectura está preparada para agregar S01, S02, S04, etc. Para cada sección se puede conservar la misma capa de catálogos y crear su tabla de respuesta operacional específica (`respuesta_s01`, `respuesta_s02`, ...), manteniendo integridad referencial y evitando una tabla extremadamente ancha.
