from django.urls import path

from . import views

app_name = "epnas"

urlpatterns = [
    path("health/", views.health, name="health"),
    path("", views.inicio, name="inicio"),
    path("s03/nuevo/", views.nuevo_s03, name="nuevo_s03"),
    path("s03/<uuid:pk>/", views.detalle_s03, name="detalle_s03"),
    path("s03/<uuid:pk>/editar/", views.editar_s03, name="editar_s03"),
]
