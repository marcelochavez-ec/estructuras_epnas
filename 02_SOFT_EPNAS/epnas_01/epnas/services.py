from django.db import transaction

from .models import EpnasFormulario, RespuestaS03


@transaction.atomic
def guardar_s03(*, cleaned_data, usuario, instancia=None):
    if instancia is None:
        instancia = EpnasFormulario(usuario=usuario)

    instancia.unicodigo = cleaned_data["unicodigo"].strip()
    instancia.establecimiento_id = cleaned_data.get("establecimiento_id")
    instancia.observaciones = cleaned_data.get("observaciones", "").strip()
    instancia.estado = "ENVIADO"
    instancia.save()

    respuesta, _ = RespuestaS03.objects.update_or_create(
        formulario=instancia,
        defaults={
            "s03_am01": cleaned_data["s03_am01"],
            "s03_am02": cleaned_data["s03_am02"],
            "s03_am03": cleaned_data["s03_am03"],
            "s03_am04": cleaned_data["s03_am04"],
            "s03_am05": cleaned_data["s03_am05"],
            "s03_am06": cleaned_data["s03_am06"],
        },
    )
    respuesta.full_clean()
    respuesta.save()

    return instancia
