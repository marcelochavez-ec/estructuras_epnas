from django.core.management.base import BaseCommand
from django.db import transaction

from epnas.models import (
    FormularioOpcion,
    FormularioSeccion,
    FormularioValidacion,
    FormularioVariable,
)


CATALOGO = {
    "s03_am01": {
        "orden": 1,
        "etiqueta": "Medio de transporte",
        "tipo_control": "select",
        "tipo_dato": "catalogo",
        "unidad_medida": None,
        "opciones": [
            (1, "Terrestre", "Alta accesibilidad"),
            (2, "Fluvial", "Media accesibilidad"),
            (3, "Aéreo", "Baja accesibilidad"),
        ],
        "validacion": ("valor_catalogado", "Debe seleccionarse una opción válida del catálogo de medio de transporte."),
    },
    "s03_am02": {
        "orden": 2,
        "etiqueta": "Frecuencia de transporte",
        "tipo_control": "select",
        "tipo_dato": "catalogo",
        "unidad_medida": None,
        "opciones": [
            (1, "Diaria", "Alta accesibilidad"),
            (2, "2 veces al día", "Media accesibilidad"),
            (3, "1–2 veces por semana", "Baja accesibilidad"),
            (4, "Nunca", "Muy baja accesibilidad"),
        ],
        "validacion": ("valor_catalogado", "Debe seleccionarse una opción válida del catálogo de frecuencia de transporte."),
    },
    "s03_am03": {
        "orden": 3,
        "etiqueta": "Número de proveedores de transporte",
        "tipo_control": "select",
        "tipo_dato": "catalogo",
        "unidad_medida": None,
        "opciones": [
            (1, "3 o más", "Alta accesibilidad"),
            (2, "2 proveedores", "Media accesibilidad"),
            (3, "1 proveedor", "Baja accesibilidad"),
        ],
        "validacion": ("valor_catalogado", "Debe seleccionarse una opción válida del catálogo de proveedores de transporte."),
    },
    "s03_am04": {
        "orden": 4,
        "etiqueta": "Costo mensual de pasajes",
        "tipo_control": "select",
        "tipo_dato": "catalogo",
        "unidad_medida": "USD",
        "opciones": [
            (1, "≤ USD 121.19", "Alta accesibilidad"),
            (2, "≥ USD 121.20", "Media accesibilidad"),
        ],
        "validacion": ("valor_catalogado", "Debe seleccionarse el rango correspondiente al costo mensual de pasajes."),
    },
    "s03_am05": {
        "orden": 5,
        "etiqueta": "Tiempo de traslado (horas)",
        "tipo_control": "number",
        "tipo_dato": "decimal",
        "unidad_medida": "horas",
        "opciones": [],
        "validacion": ("numero_no_negativo", "El tiempo de viaje debe registrarse numéricamente en horas y ser mayor o igual a cero."),
    },
    "s03_am06": {
        "orden": 6,
        "etiqueta": "Orden de vía principal",
        "tipo_control": "select",
        "tipo_dato": "catalogo",
        "unidad_medida": None,
        "opciones": [
            (1, "Primer orden", "Alta accesibilidad"),
            (2, "Segundo orden", "Media accesibilidad"),
            (3, "Tercer orden", "Baja accesibilidad"),
        ],
        "validacion": ("valor_catalogado", "Debe seleccionarse una opción válida del catálogo de tipo de vía."),
    },
}


class Command(BaseCommand):
    help = "Crea o actualiza el catálogo de la sección S03 de EPNAS."

    @transaction.atomic
    def handle(self, *args, **options):
        seccion, _ = FormularioSeccion.objects.update_or_create(
            codigo="s03",
            defaults={
                "nombre": "Acceso y Movilización",
                "descripcion": "Sección S03 del formulario EPNAS.",
                "orden": 3,
                "activo": True,
            },
        )

        for codigo_variable, cfg in CATALOGO.items():
            variable, _ = FormularioVariable.objects.update_or_create(
                seccion=seccion,
                codigo=codigo_variable,
                defaults={
                    "etiqueta": cfg["etiqueta"],
                    "tipo_control": cfg["tipo_control"],
                    "tipo_dato": cfg["tipo_dato"],
                    "unidad_medida": cfg["unidad_medida"],
                    "obligatorio": True,
                    "orden": cfg["orden"],
                    "activo": True,
                },
            )

            codigos_activos = []
            for orden, (codigo, descripcion, nivel) in enumerate(cfg["opciones"], start=1):
                codigos_activos.append(codigo)
                FormularioOpcion.objects.update_or_create(
                    variable=variable,
                    codigo=codigo,
                    defaults={
                        "descripcion": descripcion,
                        "nivel_accesibilidad": nivel,
                        "orden": orden,
                        "activo": True,
                    },
                )

            if codigos_activos:
                variable.opciones.exclude(codigo__in=codigos_activos).update(activo=False)

            regla, detalle = cfg["validacion"]
            FormularioValidacion.objects.update_or_create(
                variable=variable,
                regla=regla,
                defaults={
                    "detalle": detalle,
                    "parametros_json": {"min": 0} if regla == "numero_no_negativo" else None,
                    "activo": True,
                },
            )

        self.stdout.write(self.style.SUCCESS("Catálogo S03 cargado/actualizado correctamente."))
