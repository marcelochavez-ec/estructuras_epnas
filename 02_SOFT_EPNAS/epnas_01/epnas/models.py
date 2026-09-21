import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class FormularioSeccion(models.Model):
    id_seccion = models.BigAutoField(primary_key=True)
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    orden = models.SmallIntegerField()
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "formulario_seccion"
        ordering = ["orden"]
        verbose_name = "Sección del formulario"
        verbose_name_plural = "Secciones del formulario"

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class FormularioVariable(models.Model):
    TIPOS_CONTROL = [
        ("select", "Lista desplegable"),
        ("number", "Numérico"),
        ("text", "Texto"),
        ("date", "Fecha"),
        ("textarea", "Texto largo"),
        ("radio", "Botones de opción"),
        ("checkbox", "Casilla de verificación"),
    ]

    TIPOS_DATO = [
        ("catalogo", "Catálogo"),
        ("decimal", "Decimal"),
        ("entero", "Entero"),
        ("texto", "Texto"),
        ("fecha", "Fecha"),
        ("booleano", "Booleano"),
    ]

    id_variable = models.BigAutoField(primary_key=True)
    seccion = models.ForeignKey(
        FormularioSeccion,
        db_column="id_seccion",
        on_delete=models.CASCADE,
        related_name="variables",
    )
    codigo = models.CharField(max_length=30)
    etiqueta = models.CharField(max_length=255)
    tipo_control = models.CharField(max_length=20, choices=TIPOS_CONTROL)
    tipo_dato = models.CharField(max_length=20, choices=TIPOS_DATO)
    unidad_medida = models.CharField(max_length=30, null=True, blank=True)
    obligatorio = models.BooleanField(default=True)
    orden = models.SmallIntegerField()
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "formulario_variable"
        ordering = ["seccion__orden", "orden"]
        constraints = [
            models.UniqueConstraint(
                fields=["seccion", "codigo"],
                name="uq_variable_seccion_codigo",
            ),
            models.UniqueConstraint(
                fields=["seccion", "orden"],
                name="uq_variable_seccion_orden",
            ),
        ]
        verbose_name = "Variable"
        verbose_name_plural = "Variables"

    def __str__(self):
        return f"{self.codigo} - {self.etiqueta}"


class FormularioOpcion(models.Model):
    id_opcion = models.BigAutoField(primary_key=True)
    variable = models.ForeignKey(
        FormularioVariable,
        db_column="id_variable",
        on_delete=models.CASCADE,
        related_name="opciones",
    )
    codigo = models.SmallIntegerField()
    descripcion = models.CharField(max_length=150)
    nivel_accesibilidad = models.CharField(max_length=30, blank=True)
    orden = models.SmallIntegerField()
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "formulario_opcion"
        ordering = ["variable__orden", "orden"]
        constraints = [
            models.UniqueConstraint(
                fields=["variable", "codigo"],
                name="uq_opcion_variable_codigo",
            ),
            models.UniqueConstraint(
                fields=["variable", "orden"],
                name="uq_opcion_variable_orden",
            ),
        ]
        verbose_name = "Opción"
        verbose_name_plural = "Opciones"

    def __str__(self):
        return f"{self.variable.codigo} [{self.codigo}] {self.descripcion}"


class FormularioValidacion(models.Model):
    id_validacion = models.BigAutoField(primary_key=True)
    variable = models.ForeignKey(
        FormularioVariable,
        db_column="id_variable",
        on_delete=models.CASCADE,
        related_name="validaciones",
    )
    regla = models.CharField(max_length=80)
    detalle = models.TextField()
    parametros_json = models.JSONField(null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "formulario_validacion"
        constraints = [
            models.UniqueConstraint(
                fields=["variable", "regla"],
                name="uq_validacion_variable_regla",
            )
        ]
        verbose_name = "Validación"
        verbose_name_plural = "Validaciones"

    def __str__(self):
        return f"{self.variable.codigo} - {self.regla}"


class EpnasFormulario(models.Model):
    ESTADOS = [
        ("BORRADOR", "Borrador"),
        ("ENVIADO", "Enviado"),
        ("VALIDADO", "Validado"),
        ("ANULADO", "Anulado"),
    ]

    id_formulario = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_column="id_usuario",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="formularios_epnas",
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    version = models.PositiveIntegerField(default=1)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="BORRADOR")
    unicodigo = models.CharField(max_length=20, db_index=True)
    establecimiento_id = models.BigIntegerField(null=True, blank=True)
    observaciones = models.TextField(blank=True)

    class Meta:
        db_table = "epnas_formulario"
        ordering = ["-fecha_registro"]
        constraints = [
            models.CheckConstraint(
                condition=Q(estado__in=["BORRADOR", "ENVIADO", "VALIDADO", "ANULADO"]),
                name="ck_epnas_formulario_estado",
            )
        ]
        verbose_name = "Formulario EPNAS"
        verbose_name_plural = "Formularios EPNAS"

    def __str__(self):
        return f"{self.id_formulario} | {self.unicodigo} | {self.estado}"


class RespuestaS03(models.Model):
    id_respuesta_s03 = models.BigAutoField(primary_key=True)
    formulario = models.OneToOneField(
        EpnasFormulario,
        db_column="id_formulario",
        on_delete=models.CASCADE,
        related_name="respuesta_s03",
    )

    # Los select se guardan como FK reales a formulario_opcion.
    s03_am01 = models.ForeignKey(
        FormularioOpcion,
        db_column="s03_am01",
        on_delete=models.PROTECT,
        related_name="+",
    )
    s03_am02 = models.ForeignKey(
        FormularioOpcion,
        db_column="s03_am02",
        on_delete=models.PROTECT,
        related_name="+",
    )
    s03_am03 = models.ForeignKey(
        FormularioOpcion,
        db_column="s03_am03",
        on_delete=models.PROTECT,
        related_name="+",
    )
    s03_am04 = models.ForeignKey(
        FormularioOpcion,
        db_column="s03_am04",
        on_delete=models.PROTECT,
        related_name="+",
    )
    s03_am05 = models.DecimalField(max_digits=6, decimal_places=2)
    s03_am06 = models.ForeignKey(
        FormularioOpcion,
        db_column="s03_am06",
        on_delete=models.PROTECT,
        related_name="+",
    )

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "respuesta_s03"
        constraints = [
            models.CheckConstraint(
                condition=Q(s03_am05__gte=0),
                name="ck_respuesta_s03_am05_no_negativo",
            )
        ]
        verbose_name = "Respuesta S03"
        verbose_name_plural = "Respuestas S03"

    def clean(self):
        super().clean()
        esperadas = {
            "s03_am01": "s03_am01",
            "s03_am02": "s03_am02",
            "s03_am03": "s03_am03",
            "s03_am04": "s03_am04",
            "s03_am06": "s03_am06",
        }
        errores = {}

        for campo, codigo_variable in esperadas.items():
            opcion = getattr(self, campo, None)
            if opcion and opcion.variable.codigo != codigo_variable:
                errores[campo] = (
                    f"La opción seleccionada pertenece a {opcion.variable.codigo} "
                    f"y no a {codigo_variable}."
                )

        if errores:
            raise ValidationError(errores)

    def __str__(self):
        return f"S03 - {self.formulario_id}"
