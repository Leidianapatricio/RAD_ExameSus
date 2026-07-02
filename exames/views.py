from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import TipoExameForm
from .models import TipoExame


def listar_tipos(request):
    pesquisa = request.GET.get("q")
    tipos = TipoExame.objects.all().order_by("nome")

    if pesquisa:
        tipos = tipos.filter(nome__icontains=pesquisa)

    paginator = Paginator(tipos, 10)
    page = request.GET.get("page")
    tipos = paginator.get_page(page)

    return render(request, "exames/listar.html", {
        "tipos": tipos,
        "pesquisa": pesquisa,
    })


def criar_tipo(request):
    form = TipoExameForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de exame cadastrado com sucesso.")
            return redirect("exames:listar_tipos")

    return render(request, "exames/form.html", {
        "form": form,
        "titulo": "Novo Tipo de Exame",
        "descricao": "Cadastre um tipo de exame disponível no sistema.",
    })


def editar_tipo(request, id):
    tipo = get_object_or_404(TipoExame, id=id)
    form = TipoExameForm(request.POST or None, instance=tipo)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de exame atualizado com sucesso.")
            return redirect("exames:listar_tipos")

    return render(request, "exames/form.html", {
        "form": form,
        "titulo": "Editar Tipo de Exame",
        "descricao": "Atualize as informações do tipo de exame.",
    })


def excluir_tipo(request, id):
    tipo = get_object_or_404(TipoExame, id=id)

    if request.method == "POST":
        tipo.delete()
        messages.success(request, "Tipo de exame excluído com sucesso.")

    return redirect("exames:listar_tipos")