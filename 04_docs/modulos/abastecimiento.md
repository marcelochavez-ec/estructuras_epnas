# Modulo Abastecimiento

## 1. Nombre del modulo

Carga de abastecimiento nacional desde la API PresUP hacia PostgreSQL.

## 2. Objetivo funcional

El modulo consulta la tabla `abastecimiento_nacional` de la API PresUP, normaliza tipos de datos y carga el resultado en la tabla `presidencia.medicamentos`.

## 3. Archivos modificados o creados

1. `01_scripting/LecturaAPI_PresUP.py`
2. `03_configuraciones/config.example.yml`
3. `docs/modulos/abastecimiento.md`
4. `README.md`

## 4. Flujo general paso a paso

1. Carga la configuracion local desde `03_configuraciones/config.yml`.
2. Lee los parametros de conexion PostgreSQL desde `default.postgresql_dneaisns`.
3. Lee la clave y URL de la API desde `default.presup_api`.
4. Consulta la API PresUP con `table = abastecimiento_nacional`, `action = list` y `records = 10`.
5. Valida que la respuesta HTTP sea correcta.
6. Valida que la respuesta JSON tenga `success = true`.
7. Convierte la lista `data` en un `DataFrame`.
8. Detiene la ejecucion si la API no devuelve registros.
9. Convierte campos numericos, fechas y fechas con hora.
10. Crea el esquema `presidencia` si no existe.
11. Reemplaza la tabla `presidencia.medicamentos`.

## 5. Entradas del modulo

1. Archivo local `03_configuraciones/config.yml`.
2. Parametros `user`, `password`, `host` y `port` para PostgreSQL.
3. Parametros `url` y `apikey` para la API PresUP.
4. Endpoint de API con tabla `abastecimiento_nacional`.

## 6. Salidas del modulo

1. Tabla PostgreSQL `presidencia.medicamentos`.
2. Mensaje de codigo HTTP impreso durante la ejecucion.

## 7. Fuentes de datos utilizadas

1. API PresUP: `https://aplicaciones.presup.com.ec/app/msp/planificacion/api/v1.php`.
2. Tabla API: `abastecimiento_nacional`.

## 8. Reglas de negocio aplicadas

1. Solo se carga informacion cuando la API responde `success = true`.
2. La ejecucion se detiene si la API no devuelve registros.
3. La tabla destino se reemplaza completamente en cada ejecucion.
4. La base de datos destino es `productos_bm`.
5. La clave de API no se versiona; debe vivir en `03_configuraciones/config.yml`.

## 9. Logica UI

El modulo no tiene interfaz Shiny.

## 10. Logica server

El modulo no tiene logica server Shiny. El procesamiento se ejecuta como script Python lineal.

## 11. Consultas SQL o logica ETL relevante

1. Creacion del esquema:

```sql
CREATE SCHEMA IF NOT EXISTS presidencia;
```

2. Carga de tabla con reemplazo:

```python
df_medicamentos.to_sql(
    name="medicamentos",
    con=engine,
    schema="presidencia",
    if_exists="replace",
    index=False,
    dtype=dtype_postgresql,
    chunksize=400,
    method="multi"
)
```

Campos principales cargados:

1. `id`
2. `fecha_corte`
3. `abast_dispositivos_porcentaje`
4. `abast_medicamentos_porcentaje`
5. `abast_dispositivos_nota`
6. `abast_medicamentos_nota`
7. `fecha_actualizacion`

## 12. Dependencias

1. Python.
2. `requests`
3. `pandas`
4. `pyyaml`
5. `sqlalchemy`
6. `psycopg`
7. PostgreSQL con acceso a la base `productos_bm`.

## 13. Validaciones realizadas

1. Se valido que el repositorio no versiona `03_configuraciones/config.yml`.
2. Se retiro la clave de API hardcodeada del script antes de sincronizar con GitHub.
3. Se intento validar sintaxis Python, pero este host no tiene Python disponible en PATH.

## 14. Pruebas sugeridas o ejecutadas

1. No ejecutada: compilacion local con `py_compile`, porque este host no tiene Python disponible en PATH.
2. Sugerida: validar sintaxis y ejecutar el script en un entorno autorizado con `03_configuraciones/config.yml` completo.
3. Sugerida: verificar en PostgreSQL el conteo y tipos de columnas de `presidencia.medicamentos`.

## 15. Riesgos, supuestos y consideraciones de rendimiento

1. El parametro `records = 10` limita la consulta a diez registros.
2. `if_exists = "replace"` elimina y recrea la tabla en cada ejecucion.
3. La disponibilidad del modulo depende de la API externa PresUP.
4. La clave de API debe permanecer fuera del repositorio.

## 16. Cambios realizados en esta tarea

1. Se configuro el proyecto para apuntar al repositorio GitHub de abastecimiento.
2. Se externalizo la clave de API desde el script hacia `config.yml`.
3. Se creo una plantilla segura de configuracion.
4. Se documento el modulo de abastecimiento.

## 17. Pendientes o recomendaciones futuras

1. Confirmar si la carga debe traer mas de diez registros.
2. Considerar indice o llave en `presidencia.medicamentos` si la tabla se usa para consultas frecuentes.
