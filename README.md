# Proyecto Abastecimiento

## 1. Descripcion general

Este repositorio contiene el script ETL para consultar informacion nacional de abastecimiento desde la API PresUP y cargarla en PostgreSQL para analitica institucional en salud.

La solucion mantiene una estructura simple: configuracion local externa, script Python lineal, documentacion tecnica por modulo y carga directa a PostgreSQL.

## 2. Alcance funcional

El repositorio cubre actualmente:

1. Lectura de configuracion local desde `03_configuraciones/config.yml`.
2. Consulta de la tabla API `abastecimiento_nacional`.
3. Validacion basica de respuesta HTTP y respuesta JSON.
4. Conversion de tipos para identificadores, fechas, porcentajes y notas.
5. Creacion del esquema PostgreSQL `presidencia` si no existe.
6. Carga de datos en la tabla `presidencia.medicamentos`.
7. Documentacion tecnica del modulo.

## 3. Estructura del repositorio

```text
.
+-- 01_scripting/
|   +-- LecturaAPI_PresUP.py
+-- 03_configuraciones/
|   +-- config.example.yml
+-- docs/
|   +-- modulos/
|       +-- abastecimiento.md
+-- .gitignore
+-- README.md
```

## 4. Carpetas y archivos no versionados

El archivo `03_configuraciones/config.yml` no se sube al repositorio porque contiene credenciales y parametros reales de conexion. El repositorio incluye `03_configuraciones/config.example.yml` como plantilla segura.

Elementos excluidos por `.gitignore`:

1. `02_data/`
2. `03_configuraciones/config.yml`
3. `__pycache__/`
4. Archivos compilados de Python.
5. Archivos temporales comunes de R y entorno local.
6. `.env`

## 5. Configuracion local requerida

Para ejecutar el ETL en una maquina autorizada, crear el archivo:

```text
03_configuraciones/config.yml
```

Puede tomarse como base:

```text
03_configuraciones/config.example.yml
```

La estructura esperada es:

```yaml
default:
  postgresql_dneaisns:
    user: "usuario"
    password: "password"
    host: "host"
    port: 5432

  presup_api:
    url: "https://aplicaciones.presup.com.ec/app/msp/planificacion/api/v1.php"
    apikey: "apikey"
```

El archivo real debe completarse solo en el entorno local autorizado. No debe subirse a GitHub.

## 6. ETL de abastecimiento

Archivo:

```text
01_scripting/LecturaAPI_PresUP.py
```

Objetivo:

1. Consultar la API PresUP.
2. Descargar registros de `abastecimiento_nacional`.
3. Convertir la respuesta JSON en `DataFrame`.
4. Normalizar tipos de datos.
5. Cargar la tabla final en PostgreSQL.

Tabla destino:

```text
presidencia.medicamentos
```

## 7. Reglas de negocio aplicadas

1. La carga se ejecuta solo si la API responde correctamente.
2. La ejecucion se detiene si la API devuelve error o no retorna registros.
3. La tabla destino se reemplaza completamente en cada ejecucion.
4. La clave de API se administra mediante configuracion local no versionada.

## 8. Pruebas y validaciones

Validaciones realizadas antes de sincronizar:

1. Revision de archivos versionables.
2. Retiro de la clave de API hardcodeada.
3. Intento de compilacion local del script Python; no se ejecuto porque este host no tiene Python disponible en PATH.
4. Verificacion de que `03_configuraciones/config.yml` permanece ignorado por Git.

Pruebas sugeridas:

1. Validar sintaxis y ejecutar el script en un entorno autorizado con Python y credenciales reales.
2. Verificar el conteo de registros cargados en `presidencia.medicamentos`.
3. Confirmar si el parametro `records = 10` debe mantenerse o ampliarse.
