from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from .models import (
    EpnasFormulario,
    FormularioOpcion,
    FormularioSeccion,
    FormularioValidacion,
    FormularioVariable,
    RespuestaS03,
)


class FormularioVariableInline(TabularInline):
    model = FormularioVariable
    extra = 0
    fields = ("codigo", "etiqueta", "tipo_control", "tipo_dato", "obligatorio", "orden", "activo")


@admin.register(FormularioSeccion)
class FormularioSeccionAdmin(ModelAdmin):
    list_display = ("codigo", "nombre", "orden", "activo")
    search_fields = ("codigo", "nombre")
    list_filter = ("activo",)
    inlines = [FormularioVariableInline]


@admin.register(FormularioVariable)
class FormularioVariableAdmin(ModelAdmin):
    list_display = ("codigo", "etiqueta", "seccion", "tipo_control", "tipo_dato", "obligatorio", "orden", "activo")
    search_fields = ("codigo", "etiqueta")
    list_filter = ("seccion", "tipo_control", "tipo_dato", "obligatorio", "activo")


@admin.register(FormularioOpcion)
class FormularioOpcionAdmin(ModelAdmin):
    list_display = ("variable", "codigo", "descripcion", "nivel_accesibilidad", "orden", "activo")
    search_fields = ("variable__codigo", "descripcion")
    list_filter = ("variable__seccion", "variable", "nivel_accesibilidad", "activo")


@admin.register(FormularioValidacion)
class FormularioValidacionAdmin(ModelAdmin):
    list_display = ("variable", "regla", "activo")
    search_fields = ("variable__codigo", "regla", "detalle")
    list_filter = ("activo", "regla")


class RespuestaS03Inline(TabularInline):
    model = RespuestaS03
    extra = 0
    max_num = 1


@admin.register(EpnasFormulario)
class EpnasFormularioAdmin(ModelAdmin):
    list_display = ("id_formulario", "unicodigo", "usuario", "estado", "version", "fecha_registro")
    search_fields = ("id_formulario", "unicodigo", "usuario__username")
    list_filter = ("estado", "version", "fecha_registro")
    readonly_fields = ("id_formulario", "fecha_registro", "fecha_actualizacion")
    inlines = [RespuestaS03Inline]


@admin.register(RespuestaS03)
class RespuestaS03Admin(ModelAdmin):
    list_display = ("id_respuesta_s03", "formulario", "s03_am05", "creado_en", "actualizado_en")
    search_fields = ("formulario__id_formulario", "formulario__unicodigo")
