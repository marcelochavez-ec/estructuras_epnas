# Generada para el proyecto EPNAS 01.
import uuid

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="FormularioSeccion",
            fields=[
                ("id_seccion", models.BigAutoField(primary_key=True, serialize=False)),
                ("codigo", models.CharField(max_length=10, unique=True)),
                ("nombre", models.CharField(max_length=150)),
                ("descripcion", models.TextField(blank=True)),
                ("orden", models.SmallIntegerField()),
                ("activo", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Sección del formulario",
                "verbose_name_plural": "Secciones del formulario",
                "db_table": "formulario_seccion",
                "ordering": ["orden"],
            },
        ),
        migrations.CreateModel(
            name="EpnasFormulario",
            fields=[
                ("id_formulario", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("fecha_registro", models.DateTimeField(auto_now_add=True)),
                ("fecha_actualizacion", models.DateTimeField(auto_now=True)),
                ("version", models.PositiveIntegerField(default=1)),
                ("estado", models.CharField(choices=[("BORRADOR", "Borrador"), ("ENVIADO", "Enviado"), ("VALIDADO", "Validado"), ("ANULADO", "Anulado")], default="BORRADOR", max_length=20)),
                ("unicodigo", models.CharField(db_index=True, max_length=20)),
                ("establecimiento_id", models.BigIntegerField(blank=True, null=True)),
                ("observaciones", models.TextField(blank=True)),
                ("usuario", models.ForeignKey(blank=True, db_column="id_usuario", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="formularios_epnas", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "Formulario EPNAS",
                "verbose_name_plural": "Formularios EPNAS",
                "db_table": "epnas_formulario",
                "ordering": ["-fecha_registro"],
            },
        ),
        migrations.CreateModel(
            name="FormularioVariable",
            fields=[
                ("id_variable", models.BigAutoField(primary_key=True, serialize=False)),
                ("codigo", models.CharField(max_length=30)),
                ("etiqueta", models.CharField(max_length=255)),
                ("tipo_control", models.CharField(choices=[("select", "Lista desplegable"), ("number", "Numérico"), ("text", "Texto"), ("date", "Fecha"), ("textarea", "Texto largo"), ("radio", "Botones de opción"), ("checkbox", "Casilla de verificación")], max_length=20)),
                ("tipo_dato", models.CharField(choices=[("catalogo", "Catálogo"), ("decimal", "Decimal"), ("entero", "Entero"), ("texto", "Texto"), ("fecha", "Fecha"), ("booleano", "Booleano")], max_length=20)),
                ("unidad_medida", models.CharField(blank=True, max_length=30, null=True)),
                ("obligatorio", models.BooleanField(default=True)),
                ("orden", models.SmallIntegerField()),
                ("activo", models.BooleanField(default=True)),
                ("seccion", models.ForeignKey(db_column="id_seccion", on_delete=django.db.models.deletion.CASCADE, related_name="variables", to="epnas.formularioseccion")),
            ],
            options={
                "verbose_name": "Variable",
                "verbose_name_plural": "Variables",
                "db_table": "formulario_variable",
                "ordering": ["seccion__orden", "orden"],
            },
        ),
        migrations.CreateModel(
            name="FormularioOpcion",
            fields=[
                ("id_opcion", models.BigAutoField(primary_key=True, serialize=False)),
                ("codigo", models.SmallIntegerField()),
                ("descripcion", models.CharField(max_length=150)),
                ("nivel_accesibilidad", models.CharField(blank=True, max_length=30)),
                ("orden", models.SmallIntegerField()),
                ("activo", models.BooleanField(default=True)),
                ("variable", models.ForeignKey(db_column="id_variable", on_delete=django.db.models.deletion.CASCADE, related_name="opciones", to="epnas.formulariovariable")),
            ],
            options={
                "verbose_name": "Opción",
                "verbose_name_plural": "Opciones",
                "db_table": "formulario_opcion",
                "ordering": ["variable__orden", "orden"],
            },
        ),
        migrations.CreateModel(
            name="FormularioValidacion",
            fields=[
                ("id_validacion", models.BigAutoField(primary_key=True, serialize=False)),
                ("regla", models.CharField(max_length=80)),
                ("detalle", models.TextField()),
                ("parametros_json", models.JSONField(blank=True, null=True)),
                ("activo", models.BooleanField(default=True)),
                ("variable", models.ForeignKey(db_column="id_variable", on_delete=django.db.models.deletion.CASCADE, related_name="validaciones", to="epnas.formulariovariable")),
            ],
            options={
                "verbose_name": "Validación",
                "verbose_name_plural": "Validaciones",
                "db_table": "formulario_validacion",
            },
        ),
        migrations.CreateModel(
            name="RespuestaS03",
            fields=[
                ("id_respuesta_s03", models.BigAutoField(primary_key=True, serialize=False)),
                ("s03_am05", models.DecimalField(decimal_places=2, max_digits=6)),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
                ("actualizado_en", models.DateTimeField(auto_now=True)),
                ("formulario", models.OneToOneField(db_column="id_formulario", on_delete=django.db.models.deletion.CASCADE, related_name="respuesta_s03", to="epnas.epnasformulario")),
                ("s03_am01", models.ForeignKey(db_column="s03_am01", on_delete=django.db.models.deletion.PROTECT, related_name="+", to="epnas.formularioopcion")),
                ("s03_am02", models.ForeignKey(db_column="s03_am02", on_delete=django.db.models.deletion.PROTECT, related_name="+", to="epnas.formularioopcion")),
                ("s03_am03", models.ForeignKey(db_column="s03_am03", on_delete=django.db.models.deletion.PROTECT, related_name="+", to="epnas.formularioopcion")),
                ("s03_am04", models.ForeignKey(db_column="s03_am04", on_delete=django.db.models.deletion.PROTECT, related_name="+", to="epnas.formularioopcion")),
                ("s03_am06", models.ForeignKey(db_column="s03_am06", on_delete=django.db.models.deletion.PROTECT, related_name="+", to="epnas.formularioopcion")),
            ],
            options={
                "verbose_name": "Respuesta S03",
                "verbose_name_plural": "Respuestas S03",
                "db_table": "respuesta_s03",
            },
        ),
        migrations.AddConstraint(
            model_name="formulariovariable",
            constraint=models.UniqueConstraint(fields=("seccion", "codigo"), name="uq_variable_seccion_codigo"),
        ),
        migrations.AddConstraint(
            model_name="formulariovariable",
            constraint=models.UniqueConstraint(fields=("seccion", "orden"), name="uq_variable_seccion_orden"),
        ),
        migrations.AddConstraint(
            model_name="formularioopcion",
            constraint=models.UniqueConstraint(fields=("variable", "codigo"), name="uq_opcion_variable_codigo"),
        ),
        migrations.AddConstraint(
            model_name="formularioopcion",
            constraint=models.UniqueConstraint(fields=("variable", "orden"), name="uq_opcion_variable_orden"),
        ),
        migrations.AddConstraint(
            model_name="formulariovalidacion",
            constraint=models.UniqueConstraint(fields=("variable", "regla"), name="uq_validacion_variable_regla"),
        ),
        migrations.AddConstraint(
            model_name="epnasformulario",
            constraint=models.CheckConstraint(condition=models.Q(("estado__in", ["BORRADOR", "ENVIADO", "VALIDADO", "ANULADO"])), name="ck_epnas_formulario_estado"),
        ),
        migrations.AddConstraint(
            model_name="respuestas03",
            constraint=models.CheckConstraint(condition=models.Q(("s03_am05__gte", 0)), name="ck_respuesta_s03_am05_no_negativo"),
        ),
    ]
