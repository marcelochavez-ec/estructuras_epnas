from django import forms

from .models import FormularioOpcion


class SeccionS03Form(forms.Form):
    unicodigo = forms.CharField(
        label="Unicódigo del establecimiento",
        max_length=20,
        widget=forms.TextInput(attrs={"placeholder": "Ej. 000123"}),
    )
    establecimiento_id = forms.IntegerField(
        label="ID del establecimiento",
        required=False,
        min_value=1,
    )
    observaciones = forms.CharField(
        label="Observaciones",
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
    )

    s03_am01 = forms.ModelChoiceField(
        label="Medio de transporte",
        queryset=FormularioOpcion.objects.none(),
        empty_label="Seleccione...",
    )
    s03_am02 = forms.ModelChoiceField(
        label="Frecuencia de transporte",
        queryset=FormularioOpcion.objects.none(),
        empty_label="Seleccione...",
    )
    s03_am03 = forms.ModelChoiceField(
        label="Número de proveedores de transporte",
        queryset=FormularioOpcion.objects.none(),
        empty_label="Seleccione...",
    )
    s03_am04 = forms.ModelChoiceField(
        label="Costo mensual de pasajes",
        queryset=FormularioOpcion.objects.none(),
        empty_label="Seleccione...",
    )
    s03_am05 = forms.DecimalField(
        label="Tiempo de traslado (horas)",
        min_value=0,
        max_digits=6,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
    )
    s03_am06 = forms.ModelChoiceField(
        label="Orden de vía principal",
        queryset=FormularioOpcion.objects.none(),
        empty_label="Seleccione...",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for campo in ["s03_am01", "s03_am02", "s03_am03", "s03_am04", "s03_am06"]:
            self.fields[campo].queryset = (
                FormularioOpcion.objects
                .filter(variable__codigo=campo, variable__activo=True, activo=True)
                .select_related("variable")
                .order_by("orden")
            )

        for campo in self.fields.values():
            clase = "form-control"
            if isinstance(campo.widget, forms.Select):
                clase += " form-select"
            campo.widget.attrs.setdefault("class", clase)
