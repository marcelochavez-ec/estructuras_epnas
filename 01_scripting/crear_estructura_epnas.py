# ============================================================
# Autor: Ing. Marcelo Chávez
# Consultor Especialista en Protección Social Banco Mundial
# Email: marcelo_chavez_ec@outlook.com
# ============================================================
#
# Proyecto: EPNAS
# Objetivo:
#   Crear la estructura relacional de la sección S03
#   "Acceso y Movilización" en PostgreSQL.
#
# Base de datos: productos_bm
# Schema: epnas
#
# Requiere:
#   pip install sqlalchemy "psycopg[binary]"
# ============================================================

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


# ============================================================
# 1. CONEXIÓN POSTGRESQL
# ============================================================

DB_USER = "marcelo_chavez"
DB_PASSWORD = "*Marcelo.2025*-"
DB_HOST = "10.64.100.191"
DB_PORT = 5432
DB_NAME = "productos_bm"
DB_SCHEMA = "epnas"


DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)


# ============================================================
# 2. DEFINICIÓN MAESTRA DE S03
# ============================================================

SECCION = {
    "codigo": "s03",
    "nombre": "Acceso y Movilización",
    "descripcion": "Sección S03 del formulario EPNAS.",
    "orden": 3,
}


VARIABLES = [
    {
        "codigo": "s03_am01",
        "etiqueta": "Medio de transporte",
        "tipo_control": "select",
        "tipo_dato": "catalogo",
        "unidad_medida": None,
        "obligatorio": True,
        "orden": 1,
        "validacion_json": '{"tipo":"catalogo"}',
        "opciones": [
            (1, "Terrestre", "Alta accesibilidad"),
            (2, "Fluvial", "Media accesibilidad"),
            (3, "Aéreo", "Baja accesibilidad"),
        ],
    },
    {
        "codigo": "s03_am02",
        "etiqueta": "Frecuencia de transporte",
        "tipo_control": "select",
        "tipo_dato": "catalogo",
        "unidad_medida": None,
        "obligatorio": True,
        "orden": 2,
        "validacion_json": '{"tipo":"catalogo"}',
        "opciones": [
            (1, "Diaria", "Alta accesibilidad"),
            (2, "2 veces al día", "Media accesibilidad"),
            (3, "1–2 veces por semana", "Baja accesibilidad"),
            (4, "Nunca", "Muy baja accesibilidad"),
        ],
    },
    {
        "codigo": "s03_am03",
        "etiqueta": "Número de proveedores de transporte",
        "tipo_control": "select",
        "tipo_dato": "catalogo",
        "unidad_medida": None,
        "obligatorio": True,
        "orden": 3,
        "validacion_json": '{"tipo":"catalogo"}',
        "opciones": [
            (1, "3 o más", "Alta accesibilidad"),
            (2, "2 proveedores", "Media accesibilidad"),
            (3, "1 proveedor", "Baja accesibilidad"),
        ],
    },
    {
        "codigo": "s03_am04",
        "etiqueta": "Costo mensual de pasajes",
        "tipo_control": "select",
        "tipo_dato": "catalogo",
        "unidad_medida": "USD",
        "obligatorio": True,
        "orden": 4,
        "validacion_json": '{"tipo":"catalogo"}',
        "opciones": [
            (1, "≤ USD 121.19", "Alta accesibilidad"),
            (2, "≥ USD 121.20", "Media accesibilidad"),
        ],
    },
    {
        "codigo": "s03_am05",
        "etiqueta": "Tiempo de viaje",
        "tipo_control": "number",
        "tipo_dato": "decimal",
        "unidad_medida": "horas",
        "obligatorio": True,
        "orden": 5,
        "validacion_json": '{"min":0,"precision":2}',
        "opciones": [],
    },
    {
        "codigo": "s03_am06",
        "etiqueta": "Tipo de vía",
        "tipo_control": "select",
        "tipo_dato": "catalogo",
        "unidad_medida": None,
        "obligatorio": True,
        "orden": 6,
        "validacion_json": '{"tipo":"catalogo"}',
        "opciones": [
            (1, "Primer orden", "Alta accesibilidad"),
            (2, "Segundo orden", "Media accesibilidad"),
            (3, "Tercer orden", "Baja accesibilidad"),
        ],
    },
]


# ============================================================
# 3. DDL - CREACIÓN DEL SCHEMA Y TABLAS
# ============================================================

DDL = f"""
CREATE SCHEMA IF NOT EXISTS {DB_SCHEMA};

-- ===========================================================
-- 3.1 TABLA DE SECCIONES
-- ===========================================================

CREATE TABLE IF NOT EXISTS {DB_SCHEMA}.formulario_seccion (
    id_seccion      BIGSERIAL PRIMARY KEY,
    codigo          VARCHAR(10)  NOT NULL,
    nombre          VARCHAR(150) NOT NULL,
    descripcion     TEXT,
    orden           SMALLINT     NOT NULL,
    activo          BOOLEAN      NOT NULL DEFAULT TRUE,

    CONSTRAINT uq_formulario_seccion_codigo
        UNIQUE (codigo),

    CONSTRAINT ck_formulario_seccion_orden
        CHECK (orden > 0)
);


-- ===========================================================
-- 3.2 TABLA DE VARIABLES
-- ===========================================================

CREATE TABLE IF NOT EXISTS {DB_SCHEMA}.formulario_variable (
    id_variable      BIGSERIAL PRIMARY KEY,
    id_seccion       BIGINT       NOT NULL,
    codigo           VARCHAR(30)  NOT NULL,
    etiqueta         VARCHAR(255) NOT NULL,
    tipo_control     VARCHAR(20)  NOT NULL,
    tipo_dato        VARCHAR(20)  NOT NULL,
    unidad_medida    VARCHAR(30),
    obligatorio      BOOLEAN      NOT NULL DEFAULT TRUE,
    orden            SMALLINT     NOT NULL,
    validacion_json  JSONB,
    activo           BOOLEAN      NOT NULL DEFAULT TRUE,

    CONSTRAINT fk_formulario_variable_seccion
        FOREIGN KEY (id_seccion)
        REFERENCES {DB_SCHEMA}.formulario_seccion (id_seccion)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT uq_formulario_variable_codigo
        UNIQUE (codigo),

    CONSTRAINT uq_formulario_variable_seccion_orden
        UNIQUE (id_seccion, orden),

    CONSTRAINT ck_formulario_variable_tipo_control
        CHECK (
            tipo_control IN (
                'select',
                'number',
                'text',
                'textarea',
                'date',
                'radio',
                'checkbox'
            )
        ),

    CONSTRAINT ck_formulario_variable_tipo_dato
        CHECK (
            tipo_dato IN (
                'catalogo',
                'decimal',
                'entero',
                'texto',
                'fecha',
                'booleano'
            )
        ),

    CONSTRAINT ck_formulario_variable_orden
        CHECK (orden > 0)
);


-- ===========================================================
-- 3.3 TABLA DE OPCIONES
-- ===========================================================

CREATE TABLE IF NOT EXISTS {DB_SCHEMA}.formulario_opcion (
    id_opcion             BIGSERIAL PRIMARY KEY,
    id_variable           BIGINT       NOT NULL,
    codigo                SMALLINT     NOT NULL,
    descripcion           VARCHAR(150) NOT NULL,
    nivel_accesibilidad   VARCHAR(30),
    orden                 SMALLINT     NOT NULL,
    activo                BOOLEAN      NOT NULL DEFAULT TRUE,

    CONSTRAINT fk_formulario_opcion_variable
        FOREIGN KEY (id_variable)
        REFERENCES {DB_SCHEMA}.formulario_variable (id_variable)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT uq_formulario_opcion_variable_codigo
        UNIQUE (id_variable, codigo),

    CONSTRAINT uq_formulario_opcion_variable_orden
        UNIQUE (id_variable, orden),

    CONSTRAINT ck_formulario_opcion_codigo
        CHECK (codigo > 0),

    CONSTRAINT ck_formulario_opcion_orden
        CHECK (orden > 0)
);


-- ===========================================================
-- 3.4 CABECERA DEL FORMULARIO EPNAS
-- ===========================================================

CREATE TABLE IF NOT EXISTS {DB_SCHEMA}.epnas_formulario (
    id_formulario          UUID PRIMARY KEY,
    id_usuario             BIGINT,
    fecha_registro         TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion    TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    version                INTEGER     NOT NULL DEFAULT 1,
    estado                 VARCHAR(20) NOT NULL DEFAULT 'BORRADOR',
    unicodigo              VARCHAR(20),
    establecimiento_id     BIGINT,
    observaciones          TEXT,

    CONSTRAINT ck_epnas_formulario_version
        CHECK (version >= 1),

    CONSTRAINT ck_epnas_formulario_estado
        CHECK (
            estado IN (
                'BORRADOR',
                'EN_PROCESO',
                'ENVIADO',
                'VALIDADO',
                'DEVUELTO',
                'ANULADO'
            )
        )
);


-- ===========================================================
-- 3.5 RESPUESTAS S03
--
-- IMPORTANTE:
-- Las variables tipo select almacenan id_opcion, no el código
-- SMALLINT. Esto permite FK real contra formulario_opcion.
-- ===========================================================

CREATE TABLE IF NOT EXISTS {DB_SCHEMA}.respuesta_s03 (
    id_respuesta_s03   BIGSERIAL PRIMARY KEY,
    id_formulario      UUID NOT NULL,

    s03_am01           BIGINT NOT NULL,
    s03_am02           BIGINT NOT NULL,
    s03_am03           BIGINT NOT NULL,
    s03_am04           BIGINT NOT NULL,
    s03_am05           NUMERIC(6,2) NOT NULL,
    s03_am06           BIGINT NOT NULL,

    creado_en          TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en     TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_respuesta_s03_formulario
        FOREIGN KEY (id_formulario)
        REFERENCES {DB_SCHEMA}.epnas_formulario (id_formulario)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT uq_respuesta_s03_formulario
        UNIQUE (id_formulario),

    CONSTRAINT fk_respuesta_s03_am01
        FOREIGN KEY (s03_am01)
        REFERENCES {DB_SCHEMA}.formulario_opcion (id_opcion)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_respuesta_s03_am02
        FOREIGN KEY (s03_am02)
        REFERENCES {DB_SCHEMA}.formulario_opcion (id_opcion)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_respuesta_s03_am03
        FOREIGN KEY (s03_am03)
        REFERENCES {DB_SCHEMA}.formulario_opcion (id_opcion)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_respuesta_s03_am04
        FOREIGN KEY (s03_am04)
        REFERENCES {DB_SCHEMA}.formulario_opcion (id_opcion)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_respuesta_s03_am06
        FOREIGN KEY (s03_am06)
        REFERENCES {DB_SCHEMA}.formulario_opcion (id_opcion)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT ck_respuesta_s03_am05
        CHECK (s03_am05 >= 0)
);


-- ===========================================================
-- 3.6 ÍNDICES
-- ===========================================================

CREATE INDEX IF NOT EXISTS ix_formulario_variable_id_seccion
    ON {DB_SCHEMA}.formulario_variable (id_seccion);

CREATE INDEX IF NOT EXISTS ix_formulario_opcion_id_variable
    ON {DB_SCHEMA}.formulario_opcion (id_variable);

CREATE INDEX IF NOT EXISTS ix_epnas_formulario_id_usuario
    ON {DB_SCHEMA}.epnas_formulario (id_usuario);

CREATE INDEX IF NOT EXISTS ix_epnas_formulario_unicodigo
    ON {DB_SCHEMA}.epnas_formulario (unicodigo);

CREATE INDEX IF NOT EXISTS ix_epnas_formulario_estado
    ON {DB_SCHEMA}.epnas_formulario (estado);

CREATE INDEX IF NOT EXISTS ix_respuesta_s03_id_formulario
    ON {DB_SCHEMA}.respuesta_s03 (id_formulario);


-- ===========================================================
-- 3.7 FUNCIÓN PARA ACTUALIZAR TIMESTAMPS
-- ===========================================================

CREATE OR REPLACE FUNCTION {DB_SCHEMA}.fn_actualizar_timestamp()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.fecha_actualizacion = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;


DROP TRIGGER IF EXISTS trg_epnas_formulario_actualizacion
ON {DB_SCHEMA}.epnas_formulario;

CREATE TRIGGER trg_epnas_formulario_actualizacion
BEFORE UPDATE
ON {DB_SCHEMA}.epnas_formulario
FOR EACH ROW
EXECUTE FUNCTION {DB_SCHEMA}.fn_actualizar_timestamp();


-- ===========================================================
-- 3.8 FUNCIÓN PARA VALIDAR QUE CADA OPCIÓN CORRESPONDA
--     A LA VARIABLE CORRECTA
-- ===========================================================

CREATE OR REPLACE FUNCTION {DB_SCHEMA}.fn_validar_respuesta_s03()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN

    IF NOT EXISTS (
        SELECT 1
        FROM {DB_SCHEMA}.formulario_opcion o
        JOIN {DB_SCHEMA}.formulario_variable v
          ON v.id_variable = o.id_variable
        WHERE o.id_opcion = NEW.s03_am01
          AND v.codigo = 's03_am01'
          AND o.activo = TRUE
          AND v.activo = TRUE
    ) THEN
        RAISE EXCEPTION
            's03_am01 contiene una opción que no pertenece a la variable s03_am01';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM {DB_SCHEMA}.formulario_opcion o
        JOIN {DB_SCHEMA}.formulario_variable v
          ON v.id_variable = o.id_variable
        WHERE o.id_opcion = NEW.s03_am02
          AND v.codigo = 's03_am02'
          AND o.activo = TRUE
          AND v.activo = TRUE
    ) THEN
        RAISE EXCEPTION
            's03_am02 contiene una opción que no pertenece a la variable s03_am02';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM {DB_SCHEMA}.formulario_opcion o
        JOIN {DB_SCHEMA}.formulario_variable v
          ON v.id_variable = o.id_variable
        WHERE o.id_opcion = NEW.s03_am03
          AND v.codigo = 's03_am03'
          AND o.activo = TRUE
          AND v.activo = TRUE
    ) THEN
        RAISE EXCEPTION
            's03_am03 contiene una opción que no pertenece a la variable s03_am03';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM {DB_SCHEMA}.formulario_opcion o
        JOIN {DB_SCHEMA}.formulario_variable v
          ON v.id_variable = o.id_variable
        WHERE o.id_opcion = NEW.s03_am04
          AND v.codigo = 's03_am04'
          AND o.activo = TRUE
          AND v.activo = TRUE
    ) THEN
        RAISE EXCEPTION
            's03_am04 contiene una opción que no pertenece a la variable s03_am04';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM {DB_SCHEMA}.formulario_opcion o
        JOIN {DB_SCHEMA}.formulario_variable v
          ON v.id_variable = o.id_variable
        WHERE o.id_opcion = NEW.s03_am06
          AND v.codigo = 's03_am06'
          AND o.activo = TRUE
          AND v.activo = TRUE
    ) THEN
        RAISE EXCEPTION
            's03_am06 contiene una opción que no pertenece a la variable s03_am06';
    END IF;

    RETURN NEW;
END;
$$;


DROP TRIGGER IF EXISTS trg_validar_respuesta_s03
ON {DB_SCHEMA}.respuesta_s03;

CREATE TRIGGER trg_validar_respuesta_s03
BEFORE INSERT OR UPDATE
ON {DB_SCHEMA}.respuesta_s03
FOR EACH ROW
EXECUTE FUNCTION {DB_SCHEMA}.fn_validar_respuesta_s03();


-- ===========================================================
-- 3.9 VISTA DE CATÁLOGOS PARA DJANGO
-- ===========================================================

CREATE OR REPLACE VIEW {DB_SCHEMA}.vw_catalogo_s03 AS
SELECT
    s.id_seccion,
    s.codigo AS seccion_codigo,
    s.nombre AS seccion_nombre,

    v.id_variable,
    v.codigo AS variable_codigo,
    v.etiqueta,
    v.tipo_control,
    v.tipo_dato,
    v.unidad_medida,
    v.obligatorio,
    v.orden AS variable_orden,
    v.validacion_json,

    o.id_opcion,
    o.codigo AS opcion_codigo,
    o.descripcion AS opcion_descripcion,
    o.nivel_accesibilidad,
    o.orden AS opcion_orden

FROM {DB_SCHEMA}.formulario_seccion s

JOIN {DB_SCHEMA}.formulario_variable v
    ON v.id_seccion = s.id_seccion

LEFT JOIN {DB_SCHEMA}.formulario_opcion o
    ON o.id_variable = v.id_variable
   AND o.activo = TRUE

WHERE
    s.codigo = 's03'
    AND s.activo = TRUE
    AND v.activo = TRUE

ORDER BY
    v.orden,
    o.orden NULLS FIRST;
"""


# ============================================================
# 4. CARGA DE CATÁLOGOS
# ============================================================

SQL_UPSERT_SECCION = f"""
INSERT INTO {DB_SCHEMA}.formulario_seccion (
    codigo,
    nombre,
    descripcion,
    orden,
    activo
)
VALUES (
    :codigo,
    :nombre,
    :descripcion,
    :orden,
    TRUE
)
ON CONFLICT (codigo)
DO UPDATE SET
    nombre = EXCLUDED.nombre,
    descripcion = EXCLUDED.descripcion,
    orden = EXCLUDED.orden,
    activo = TRUE
RETURNING id_seccion;
"""


SQL_UPSERT_VARIABLE = f"""
INSERT INTO {DB_SCHEMA}.formulario_variable (
    id_seccion,
    codigo,
    etiqueta,
    tipo_control,
    tipo_dato,
    unidad_medida,
    obligatorio,
    orden,
    validacion_json,
    activo
)
VALUES (
    :id_seccion,
    :codigo,
    :etiqueta,
    :tipo_control,
    :tipo_dato,
    :unidad_medida,
    :obligatorio,
    :orden,
    CAST(:validacion_json AS JSONB),
    TRUE
)
ON CONFLICT (codigo)
DO UPDATE SET
    id_seccion = EXCLUDED.id_seccion,
    etiqueta = EXCLUDED.etiqueta,
    tipo_control = EXCLUDED.tipo_control,
    tipo_dato = EXCLUDED.tipo_dato,
    unidad_medida = EXCLUDED.unidad_medida,
    obligatorio = EXCLUDED.obligatorio,
    orden = EXCLUDED.orden,
    validacion_json = EXCLUDED.validacion_json,
    activo = TRUE
RETURNING id_variable;
"""


SQL_UPSERT_OPCION = f"""
INSERT INTO {DB_SCHEMA}.formulario_opcion (
    id_variable,
    codigo,
    descripcion,
    nivel_accesibilidad,
    orden,
    activo
)
VALUES (
    :id_variable,
    :codigo,
    :descripcion,
    :nivel_accesibilidad,
    :orden,
    TRUE
)
ON CONFLICT (id_variable, codigo)
DO UPDATE SET
    descripcion = EXCLUDED.descripcion,
    nivel_accesibilidad = EXCLUDED.nivel_accesibilidad,
    orden = EXCLUDED.orden,
    activo = TRUE
RETURNING id_opcion;
"""


# ============================================================
# 5. EJECUCIÓN
# ============================================================

def crear_estructura():
    print("=" * 70)
    print("EPNAS - CREACIÓN DE ESTRUCTURA POSTGRESQL")
    print("=" * 70)
    print(f"Host   : {DB_HOST}")
    print(f"Base   : {DB_NAME}")
    print(f"Schema : {DB_SCHEMA}")
    print()

    with engine.begin() as conn:

        # ----------------------------------------------------
        # 5.1 Crear schema, tablas, índices, funciones y vistas
        # ----------------------------------------------------
        conn.execute(text(DDL))

        # ----------------------------------------------------
        # 5.2 Insertar / actualizar sección
        # ----------------------------------------------------
        resultado = conn.execute(
            text(SQL_UPSERT_SECCION),
            SECCION,
        )

        id_seccion = resultado.scalar_one()

        # ----------------------------------------------------
        # 5.3 Insertar / actualizar variables y opciones
        # ----------------------------------------------------
        for variable in VARIABLES:

            parametros_variable = {
                "id_seccion": id_seccion,
                "codigo": variable["codigo"],
                "etiqueta": variable["etiqueta"],
                "tipo_control": variable["tipo_control"],
                "tipo_dato": variable["tipo_dato"],
                "unidad_medida": variable["unidad_medida"],
                "obligatorio": variable["obligatorio"],
                "orden": variable["orden"],
                "validacion_json": variable["validacion_json"],
            }

            resultado = conn.execute(
                text(SQL_UPSERT_VARIABLE),
                parametros_variable,
            )

            id_variable = resultado.scalar_one()

            for codigo, descripcion, nivel in variable["opciones"]:
                conn.execute(
                    text(SQL_UPSERT_OPCION),
                    {
                        "id_variable": id_variable,
                        "codigo": codigo,
                        "descripcion": descripcion,
                        "nivel_accesibilidad": nivel,
                        "orden": codigo,
                    },
                )

        # ----------------------------------------------------
        # 5.4 Verificación
        # ----------------------------------------------------
        tablas = conn.execute(
            text(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = :schema
                  AND table_type = 'BASE TABLE'
                ORDER BY table_name;
                """
            ),
            {"schema": DB_SCHEMA},
        ).fetchall()

        total_variables = conn.execute(
            text(
                f"""
                SELECT COUNT(*)
                FROM {DB_SCHEMA}.formulario_variable
                WHERE id_seccion = :id_seccion;
                """
            ),
            {"id_seccion": id_seccion},
        ).scalar_one()

        total_opciones = conn.execute(
            text(
                f"""
                SELECT COUNT(*)
                FROM {DB_SCHEMA}.formulario_opcion o
                JOIN {DB_SCHEMA}.formulario_variable v
                  ON v.id_variable = o.id_variable
                WHERE v.id_seccion = :id_seccion;
                """
            ),
            {"id_seccion": id_seccion},
        ).scalar_one()

    print("Proceso finalizado correctamente.")
    print()
    print("Tablas creadas / verificadas:")

    for tabla in tablas:
        print(f"  - {DB_SCHEMA}.{tabla[0]}")

    print()
    print(f"Variables S03 cargadas : {total_variables}")
    print(f"Opciones S03 cargadas  : {total_opciones}")
    print(f"Vista disponible       : {DB_SCHEMA}.vw_catalogo_s03")
    print("=" * 70)


# ============================================================
# 6. PUNTO DE ENTRADA
# ============================================================

if __name__ == "__main__":
    crear_estructura()