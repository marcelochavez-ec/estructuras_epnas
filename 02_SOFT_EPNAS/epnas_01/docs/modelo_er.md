# Modelo entidad-relación — EPNAS 01 / S03

## Tablas de configuración

- `formulario_seccion`: define las secciones del formulario.
- `formulario_variable`: define variables, etiqueta, tipo de control, tipo de dato, unidad, obligatoriedad y orden.
- `formulario_opcion`: catálogo de opciones de las variables tipo `select`.
- `formulario_validacion`: reglas de validación normalizadas por variable.

## Tablas operativas

- `epnas_formulario`: cabecera de cada formulario, con UUID, usuario, estado, versión, unicódigo y auditoría temporal.
- `respuesta_s03`: una fila por formulario para la sección S03.

## Relaciones

```text
formulario_seccion (1) ────< (N) formulario_variable
formulario_variable (1) ───< (N) formulario_opcion
formulario_variable (1) ───< (N) formulario_validacion

AUTH_USER (1) ──────────────< (N) epnas_formulario

epnas_formulario (1) ─────── (1) respuesta_s03

formulario_opcion (1) <────── (N) respuesta_s03.s03_am01
formulario_opcion (1) <────── (N) respuesta_s03.s03_am02
formulario_opcion (1) <────── (N) respuesta_s03.s03_am03
formulario_opcion (1) <────── (N) respuesta_s03.s03_am04
formulario_opcion (1) <────── (N) respuesta_s03.s03_am06
```

La diferencia principal respecto al esquema gráfico aproximado es que los campos `select` de `respuesta_s03` son **claves foráneas reales** hacia `formulario_opcion`, en lugar de guardar únicamente un `SMALLINT` sin integridad referencial. Esto protege la consistencia de las respuestas.
