from django.urls import path
from . import views

app_name = "exames"

urlpatterns = [
    path("tipos/", views.listar_tipos, name="listar_tipos"),
    path("tipos/novo/", views.criar_tipo, name="criar_tipo"),
    path("tipos/<int:id>/editar/", views.editar_tipo, name="editar_tipo"),
    path("tipos/<int:id>/excluir/", views.excluir_tipo, name="excluir_tipo"),
]