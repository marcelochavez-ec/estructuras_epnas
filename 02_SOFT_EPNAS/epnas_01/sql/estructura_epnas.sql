-- Referencia conceptual del modelo EPNAS 01.
-- La fuente de verdad ejecutable son las migraciones Django.

CREATE SCHEMA IF NOT EXISTS epnas;

-- Relaciones principales:
-- formulario_seccion 1 ---- N formulario_variable
-- formulario_variable 1 -- N formulario_opcion
-- formulario_variable 1 -- N formulario_validacion
-- auth_user 1 ----------- N epnas_formulario
-- epnas_formulario 1 ----- 1 respuesta_s03
-- respuesta_s03 N -------- 1 formulario_opcion (por cada campo select)

-- Para inspeccionar las tablas tras migrar:
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema = 'epnas'
ORDER BY table_name;
