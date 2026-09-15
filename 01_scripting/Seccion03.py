%reset -f

# ============================================================
# Autor: Ing. Marcelo Chávez
# Consultor Especialista en Protección Social Banco Mundial
# Email: marcelo_chavez_ec@outlook.com
# ============================================================

# ============================================================
# CATÁLOGO - SECCIÓN S03
# ACCESO Y MOVILIZACIÓN
# ============================================================

import pandas as pd
from pathlib import Path


# ============================================================
# 1. CONFIGURACIÓN GENERAL
# ============================================================

ARCHIVO_ENTRADA = "02_data/EJEMPLO_SECCION_s03.xlsx"
ARCHIVO_SALIDA = "resultado_catalogos_s03.xlsx"

HOJA = "s03"
SECCION = "s03"

VARIABLES = [f"s03_am{i:02d}" for i in range(1, 7)]


# ============================================================
# 2. DEFINICIÓN MAESTRA DE VARIABLES Y CATÁLOGOS
# ============================================================

CONFIG_VARIABLES = {

    "s03_am01": {
        "orden": 1,
        "descripcion": "Medio de transporte",
        "tipo_control": "select",
        "unidad_medida": None,
        "opciones": [
            (1, "Terrestre", "Alta accesibilidad"),
            (2, "Fluvial", "Media accesibilidad"),
            (3, "Aéreo", "Baja accesibilidad")
        ]
    },

    "s03_am02": {
        "orden": 2,
        "descripcion": "Frecuencia de transporte",
        "tipo_control": "select",
        "unidad_medida": None,
        "opciones": [
            (1, "Diaria", "Alta accesibilidad"),
            (2, "2 veces al día", "Media accesibilidad"),
            (3, "1–2 veces por semana", "Baja accesibilidad"),
            (4, "Nunca", "Muy baja accesibilidad")
        ]
    },

    "s03_am03": {
        "orden": 3,
        "descripcion": "Número de proveedores de transporte",
        "tipo_control": "select",
        "unidad_medida": None,
        "opciones": [
            (1, "3 o más", "Alta accesibilidad"),
            (2, "2 proveedores", "Media accesibilidad"),
            (3, "1 proveedor", "Baja accesibilidad")
        ]
    },

    "s03_am04": {
        "orden": 4,
        "descripcion": "Costo mensual de pasajes",
        "tipo_control": "select",
        "unidad_medida": "USD",
        "opciones": [
            (1, "≤ USD 121.19", "Alta accesibilidad"),
            (2, "≥ USD 121.20", "Media accesibilidad")
        ]
    },

    "s03_am05": {
        "orden": 5,
        "descripcion": "Tiempo de viaje",
        "tipo_control": "number",
        "unidad_medida": "horas",
        "opciones": []
    },

    "s03_am06": {
        "orden": 6,
        "descripcion": "Tipo de vía",
        "tipo_control": "select",
        "unidad_medida": None,
        "opciones": [
            (1, "Primer orden", "Alta accesibilidad"),
            (2, "Segundo orden", "Media accesibilidad"),
            (3, "Tercer orden", "Baja accesibilidad")
        ]
    }
}


# ============================================================
# 3. VALIDACIÓN DEL ARCHIVO DE ENTRADA
# ============================================================

ruta_entrada = Path(ARCHIVO_ENTRADA)

if not ruta_entrada.exists():
    raise FileNotFoundError(
        f"No se encontró el archivo: {ARCHIVO_ENTRADA}"
    )


# ============================================================
# 4. LECTURA DEL ARCHIVO ORIGINAL
# ============================================================

df_original = pd.read_excel(
    ARCHIVO_ENTRADA,
    sheet_name=HOJA
)


# ============================================================
# 5. VALIDACIÓN DE VARIABLES OBLIGATORIAS
# ============================================================

variables_faltantes = sorted(
    set(VARIABLES) - set(df_original.columns)
)

if variables_faltantes:
    raise ValueError(
        f"Faltan variables obligatorias en el Excel: "
        f"{variables_faltantes}"
    )


# ============================================================
# 6. TABLA MAESTRA DE VARIABLES
# ============================================================

df_variables = pd.DataFrame([
    {
        "seccion": SECCION,
        "variable": variable,
        "orden": config["orden"],
        "descripcion": config["descripcion"],
        "tipo_control": config["tipo_control"],
        "unidad_medida": config["unidad_medida"],
        "obligatorio": True
    }
    for variable, config in CONFIG_VARIABLES.items()
]).sort_values("orden").reset_index(drop=True)


# ============================================================
# 7. TABLA MAESTRA DE OPCIONES
# ============================================================

df_opciones = pd.DataFrame([
    {
        "seccion": SECCION,
        "variable": variable,
        "codigo": codigo,
        "descripcion": descripcion,
        "nivel_accesibilidad": nivel_accesibilidad,
        "orden": codigo
    }
    for variable, config in CONFIG_VARIABLES.items()
    for codigo, descripcion, nivel_accesibilidad in config["opciones"]
])


# ============================================================
# 8. IDENTIFICADOR TÉCNICO DE CADA OPCIÓN
# ============================================================

if not df_opciones.empty:

    df_opciones["id_opcion"] = (
        df_opciones["variable"]
        + "_"
        + df_opciones["codigo"]
        .astype(str)
        .str.zfill(2)
    )

    df_opciones = df_opciones[
        [
            "id_opcion",
            "seccion",
            "variable",
            "codigo",
            "descripcion",
            "nivel_accesibilidad",
            "orden"
        ]
    ].sort_values(
        ["variable", "orden"]
    ).reset_index(drop=True)


# ============================================================
# 9. VALIDACIONES INTERNAS DEL CATÁLOGO
# ============================================================

variables_configuradas = set(CONFIG_VARIABLES)

variables_no_configuradas = sorted(
    set(VARIABLES) - variables_configuradas
)

variables_configuradas_extra = sorted(
    variables_configuradas - set(VARIABLES)
)

if variables_no_configuradas:
    raise ValueError(
        f"Variables sin configuración: "
        f"{variables_no_configuradas}"
    )

if variables_configuradas_extra:
    raise ValueError(
        f"Existen variables configuradas que no pertenecen a S03: "
        f"{variables_configuradas_extra}"
    )


variables_select_sin_opciones = [
    variable
    for variable, config in CONFIG_VARIABLES.items()
    if (
        config["tipo_control"] == "select"
        and not config["opciones"]
    )
]

if variables_select_sin_opciones:
    raise ValueError(
        f"Variables tipo select sin opciones: "
        f"{variables_select_sin_opciones}"
    )


if not df_opciones.empty and df_opciones["id_opcion"].duplicated().any():

    ids_duplicados = (
        df_opciones.loc[
            df_opciones["id_opcion"].duplicated(keep=False),
            "id_opcion"
        ]
        .drop_duplicates()
        .tolist()
    )

    raise ValueError(
        f"Existen identificadores de opción duplicados: "
        f"{ids_duplicados}"
    )


# ============================================================
# 10. FRECUENCIAS DE LOS VALORES ORIGINALES
# ============================================================

df_frecuencias_originales = pd.concat(
    [
        (
            df_original[variable]
            .astype("string")
            .str.strip()
            .value_counts(dropna=False)
            .rename_axis("valor_original")
            .reset_index(name="frecuencia")
            .assign(
                seccion=SECCION,
                variable=variable
            )
        )
        for variable in VARIABLES
    ],
    ignore_index=True
)


df_frecuencias_originales = df_frecuencias_originales[
    [
        "seccion",
        "variable",
        "valor_original",
        "frecuencia"
    ]
].sort_values(
    ["variable", "frecuencia"],
    ascending=[True, False]
).reset_index(drop=True)


# ============================================================
# 11. REGLAS DE VALIDACIÓN PARA EL FORMULARIO
# ============================================================

df_validaciones = pd.DataFrame([
    {
        "seccion": SECCION,
        "variable": "s03_am01",
        "regla": "valor_catalogado",
        "detalle": "Debe seleccionarse una opción válida del catálogo de medio de transporte."
    },
    {
        "seccion": SECCION,
        "variable": "s03_am02",
        "regla": "valor_catalogado",
        "detalle": "Debe seleccionarse una opción válida del catálogo de frecuencia de transporte."
    },
    {
        "seccion": SECCION,
        "variable": "s03_am03",
        "regla": "valor_catalogado",
        "detalle": "Debe seleccionarse una opción válida del catálogo de proveedores de transporte."
    },
    {
        "seccion": SECCION,
        "variable": "s03_am04",
        "regla": "valor_catalogado",
        "detalle": "Debe seleccionarse el rango correspondiente al costo mensual de pasajes."
    },
    {
        "seccion": SECCION,
        "variable": "s03_am05",
        "regla": "numero_no_negativo",
        "detalle": "El tiempo de viaje debe registrarse numéricamente en horas y ser mayor o igual a cero."
    },
    {
        "seccion": SECCION,
        "variable": "s03_am06",
        "regla": "valor_catalogado",
        "detalle": "Debe seleccionarse una opción válida del catálogo de tipo de vía."
    }
])


# ============================================================
# 12. PROPUESTA DE MODELO RELACIONAL
# ============================================================

df_modelo_bd = pd.DataFrame([
    {
        "tabla": "formulario_seccion",
        "proposito":
            "Almacena las secciones que conforman el formulario."
    },
    {
        "tabla": "formulario_variable",
        "proposito":
            "Almacena las variables, etiquetas, orden, unidad de medida y tipo de control."
    },
    {
        "tabla": "formulario_opcion",
        "proposito":
            "Almacena las opciones cerradas, códigos y niveles de accesibilidad de cada variable."
    },
    {
        "tabla": "formulario_validacion",
        "proposito":
            "Almacena reglas de validación asociadas a las variables del formulario."
    },
    {
        "tabla": "respuesta_s03",
        "proposito":
            "Almacena las respuestas operativas correspondientes a la sección Acceso y Movilización."
    }
])


# ============================================================
# 13. CONTROL EN CONSOLA
# ============================================================

print("\n" + "=" * 70)
print("CATÁLOGO DE VARIABLES - S03")
print("=" * 70)
print(df_variables.to_string(index=False))

print("\n" + "=" * 70)
print("CATÁLOGO DE OPCIONES - S03")
print("=" * 70)
print(df_opciones.to_string(index=False))

print("\n" + "=" * 70)
print("ARCHIVO DE SALIDA")
print("=" * 70)
print(ARCHIVO_SALIDA)


# ============================================================
# 14. EXPORTACIÓN A EXCEL
# ============================================================

with pd.ExcelWriter(
    ARCHIVO_SALIDA,
    engine="openpyxl"
) as writer:

    df_original.to_excel(
        writer,
        sheet_name="01_original",
        index=False
    )

    df_variables.to_excel(
        writer,
        sheet_name="02_variables",
        index=False
    )

    df_opciones.to_excel(
        writer,
        sheet_name="03_opciones",
        index=False
    )

    df_frecuencias_originales.to_excel(
        writer,
        sheet_name="04_frecuencias_origen",
        index=False
    )

    df_validaciones.to_excel(
        writer,
        sheet_name="05_validaciones",
        index=False
    )

    df_modelo_bd.to_excel(
        writer,
        sheet_name="06_modelo_bd",
        index=False
    )


# ============================================================
# 15. RESULTADO FINAL
# ============================================================

print("\n" + "=" * 70)
print("PROCESO FINALIZADO CORRECTAMENTE")
print("=" * 70)
print(f"Archivo generado: {ARCHIVO_SALIDA}")
