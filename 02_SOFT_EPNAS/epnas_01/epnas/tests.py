from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import FormularioOpcion, FormularioSeccion, FormularioVariable


class ModeloCatalogoTest(TestCase):
    def test_relacion_seccion_variable_opcion(self):
        seccion = FormularioSeccion.objects.create(
            codigo="s03", nombre="Acceso y Movilización", orden=3
        )
        variable = FormularioVariable.objects.create(
            seccion=seccion,
            codigo="s03_am01",
            etiqueta="Medio de transporte",
            tipo_control="select",
            tipo_dato="catalogo",
            orden=1,
        )
        opcion = FormularioOpcion.objects.create(
            variable=variable,
            codigo=1,
            descripcion="Terrestre",
            nivel_accesibilidad="Alta accesibilidad",
            orden=1,
        )
        self.assertEqual(opcion.variable.seccion.codigo, "s03")
