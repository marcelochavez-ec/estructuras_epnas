from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SeccionS03Form
from .models import EpnasFormulario
from .services import guardar_s03


def health(request):
    return JsonResponse({"status": "ok", "app": "epnas_01"})


@login_required
def inicio(request):
    formularios = (
        EpnasFormulario.objects
        .filter(usuario=request.user)
        .select_related("usuario")[:20]
    )
    return render(request, "epnas/inicio.html", {"formularios": formularios})


@login_required
def nuevo_s03(request):
    if request.method == "POST":
        form = SeccionS03Form(request.POST)
        if form.is_valid():
            instancia = guardar_s03(
                cleaned_data=form.cleaned_data,
                usuario=request.user,
            )
            return redirect("epnas:detalle_s03", pk=instancia.pk)
    else:
        form = SeccionS03Form()

    return render(
        request,
        "epnas/s03_form.html",
        {"form": form, "titulo": "Nueva respuesta - Sección S03"},
    )


@login_required
def editar_s03(request, pk):
    instancia = get_object_or_404(
        EpnasFormulario.objects.select_related("usuario"),
        pk=pk,
        usuario=request.user,
    )

    try:
        respuesta = instancia.respuesta_s03
    except Exception:
        respuesta = None

    inicial = {
        "unicodigo": instancia.unicodigo,
        "establecimiento_id": instancia.establecimiento_id,
        "observaciones": instancia.observaciones,
    }

    if respuesta:
        inicial.update(
            {
                "s03_am01": respuesta.s03_am01_id,
                "s03_am02": respuesta.s03_am02_id,
                "s03_am03": respuesta.s03_am03_id,
                "s03_am04": respuesta.s03_am04_id,
                "s03_am05": respuesta.s03_am05,
                "s03_am06": respuesta.s03_am06_id,
            }
        )

    if request.method == "POST":
        form = SeccionS03Form(request.POST)
        if form.is_valid():
            instancia = guardar_s03(
                cleaned_data=form.cleaned_data,
                usuario=request.user,
                instancia=instancia,
            )
            return redirect("epnas:detalle_s03", pk=instancia.pk)
    else:
        form = SeccionS03Form(initial=inicial)

    return render(
        request,
        "epnas/s03_form.html",
        {"form": form, "titulo": "Editar respuesta - Sección S03"},
    )


@login_required
def detalle_s03(request, pk):
    instancia = get_object_or_404(
        EpnasFormulario.objects.select_related("usuario"),
        pk=pk,
        usuario=request.user,
    )
    respuesta = getattr(instancia, "respuesta_s03", None)

    return render(
        request,
        "epnas/s03_detalle.html",
        {"registro": instancia, "respuesta": respuesta},
    )
