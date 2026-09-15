# Modulo Seccion 03

## 1. Nombre del modulo

Arquitectura de catalogos para variables de la seccion S03.

## 2. Objetivo funcional

1. Definir la estructura oficial de variables y opciones cerradas de la seccion S03.
2. Construir un catalogo de codigos y categorias usable para PostgreSQL y Django.
3. Evitar una homologacion extensa en esta etapa, porque el objetivo inmediato es disenar la arquitectura del formulario.
4. Conservar frecuencias originales del Excel solo como diagnostico para reglas futuras.

## 3. Archivos modificados o creados

1. `01_scripting/Seccion03.py`
2. `04_docs/modulos/seccion03.md`

## 4. Flujo general paso a paso

1. El script inicia con `%reset -f` para limpiar objetos del entorno de Positron.
2. Define archivo de entrada, hoja, seccion y variables esperadas.
3. Valida que exista `02_data/EJEMPLO_SECCION_s03.xlsx`.
4. Lee la hoja `s03` sin modificar los datos originales.
5. Valida que existan las variables `s03_am01` a `s03_am06`.
6. Crea `df_variables` con la definicion funcional de cada variable.
7. Crea `df_opciones` con codigos y categorias oficiales por variable.
8. Crea `df_frecuencias_originales` con conteos de valores fuente solo para diagnostico.
9. Crea `df_modelo_bd` con una propuesta de tablas para PostgreSQL y Django.
10. Exporta todo en `resultado_catalogos_s03.xlsx`.

## 5. Entradas del modulo

1. Archivo: `02_data/EJEMPLO_SECCION_s03.xlsx`.
2. Hoja: `s03`.
3. Variables obligatorias:
   1. `s03_am01`
   2. `s03_am02`
   3. `s03_am03`
   4. `s03_am04`
   5. `s03_am05`
   6. `s03_am06`

## 6. Salidas del modulo

1. Archivo: `resultado_catalogos_s03.xlsx`.
2. Hoja `01_original`: datos fuente sin alteracion.
3. Hoja `02_variables`: variables del formulario con seccion, orden, tipo de control y descripcion.
4. Hoja `03_opciones`: catalogo largo con `id_opcion`, `seccion`, `variable`, `codigo`, `categoria`, `orden` y `activo`.
5. Hoja `04_frecuencias_origen`: conteo de valores originales por variable.
6. Hoja `05_modelo_bd`: propuesta de tablas relacionales para formulario.

## 7. Fuentes de datos utilizadas

1. Fuente local Excel: `02_data/EJEMPLO_SECCION_s03.xlsx`.
2. No se consulta API ni base de datos.
3. No aplica schema.tabla porque el script todavia no carga informacion en PostgreSQL.

## 8. Reglas de negocio aplicadas

1. `s03_am01` usa solo las categorias `Sí` y `No`.
2. `s03_am02` usa solo `Terrestre`, `Fluvial` y `Aéreo`.
3. `s03_am03` queda reducido a cuatro categorias: `En minutos`, `Veces al día`, `En horas` y `Sin transporte público`.
4. `s03_am04` usa cuatro rangos: `Hasta 1 hora`, `De 1 a 2 horas`, `De 2 a 4 horas` y `Más de 4 horas`.
5. `s03_am05` usa solo `Urbano` y `Rural`; cuando se defina una regla de migracion, `No aplica` debe tratarse como `Urbano`.
6. `s03_am06` usa solo `Primer orden`, `Segundo orden` y `Tercer orden`; el resto no forma parte del catalogo oficial.
7. Las categorias se escriben con primera letra mayuscula y resto minuscula cuando corresponde.
8. En esta version no se fuerza la homologacion del Excel hacia los catalogos; se separa arquitectura de catalogo y limpieza de datos.
9. El campo `seccion` se almacena en minuscula como `s03` para mantener consistencia con el nombre de la hoja y las variables.

## 9. Logica UI

1. El modulo no crea interfaz visual.
2. La tabla `df_variables` define que todas las variables se comportan como controles tipo `select`.
3. La tabla `df_opciones` contiene las opciones que luego puede leer Django para renderizar listas desplegables.

## 10. Logica server

1. El modulo no tiene logica server Shiny.
2. El procesamiento se ejecuta como script Python en Positron.
3. La salida esperada para backend es una estructura tabular que puede migrarse a PostgreSQL.

## 11. Consultas SQL o logica ETL relevante

1. No se ejecutan consultas SQL.
2. La logica ETL principal crea tablas de arquitectura con `pd.DataFrame`.
3. La frecuencia original se calcula con `value_counts` para analizar la distancia entre el dato fuente y el catalogo oficial.

## 12. Dependencias

1. Python.
2. `pandas`.
3. `openpyxl`.
4. `pathlib`, dependencia estandar de Python.

## 13. Validaciones realizadas

1. Se valida existencia del archivo fuente.
2. Se valida presencia de las seis variables obligatorias.
3. Se conserva una hoja de frecuencias originales para revisar casos como textos combinados, `NR` o `NO APLICA`.

## 14. Pruebas sugeridas o ejecutadas

1. No ejecutada: corrida completa desde consola, porque Python no esta disponible en PATH en este host.
2. Sugerida: correr `01_scripting/Seccion03.py` desde Positron.
3. Sugerida: revisar `03_opciones` para confirmar codigos antes de crear tablas PostgreSQL.
4. Sugerida: revisar `04_frecuencias_origen` solo como insumo de limpieza posterior.

## 15. Riesgos, supuestos y consideraciones de rendimiento

1. El script define catalogos oficiales, no limpia exhaustivamente el dato historico.
2. El codigo de cada opcion se define como entero por variable; la llave tecnica `id_opcion` evita colisiones entre variables.
3. El modelo recomendado es relacional con tablas de catalogo, no una tabla plana con textos repetidos.
4. El archivo de salida se reemplaza si ya existe.

## 16. Cambios realizados en esta tarea

1. Se reemplazo el enfoque de homologacion extensa por arquitectura de catalogos.
2. Se corrigio `s03_am01` para usar `Sí` con tilde y `No`.
3. Se definio `s03_am02` solo con `Terrestre`, `Fluvial` y `Aéreo`.
4. Se redujo `s03_am03` a cuatro categorias maximas.
5. Se dejo `s03_am05` solo con `Urbano` y `Rural`.
6. Se dejo `s03_am06` solo con `Primer orden`, `Segundo orden` y `Tercer orden`.
7. Se agrego una propuesta de tablas para Django/PostgreSQL.
8. Se ajusto el valor de `seccion` a `s03` en minuscula y se corrigio su uso en la tabla de frecuencias.

## 17. Pendientes o recomendaciones futuras

1. Confirmar codigos numericos finales antes de cargar PostgreSQL.
2. Definir si la tabla `respuesta_s03` guardara solo codigos o tambien el valor textual original como trazabilidad.
3. Crear en una siguiente etapa el DDL PostgreSQL y los modelos Django equivalentes.
