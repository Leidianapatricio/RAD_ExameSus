from unidades.models import UnidadeSaude, Profissional
from exames.models import Exame, TipoExame
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from usuarios.models import Usuario




def home(request):
    return render(request, "home.html")


def login_view(request):
    if request.method == "POST":
        perfil_login = request.POST.get("perfil_login")
        cpf = request.POST.get("cpf")
        identificador = request.POST.get("identificador")
        senha = request.POST.get("senha")

        if perfil_login == "CIDADAO":
            try:
                usuario = Usuario.objects.get(cpf=cpf, perfil="CIDADAO")
                login(request, usuario.user)
                return redirect("core:dashboard_cidadao")
            except Usuario.DoesNotExist:
                messages.error(request, "Cidadão não encontrado.")
                return redirect("core:login")

        if perfil_login == "PROFISSIONAL_ADMIN":
            user = authenticate(
                request,
                username=identificador,
                password=senha
            )

            if user is not None and user.is_superuser:
                login(request, user)
                return redirect("core:dashboard_admin")

            cpf_limpo = identificador.replace(".", "").replace("-", "")

            user = authenticate(
                request,
                username=cpf_limpo,
                password=senha
            )

            if user is not None:
                try:
                    usuario = Usuario.objects.get(user=user, perfil="PROFISSIONAL")
                    login(request, user)
                    return redirect("core:dashboard_profissional")
                except Usuario.DoesNotExist:
                    messages.error(request, "Profissional não encontrado.")
                    return redirect("core:login")

            messages.error(request, "Usuário/CPF ou senha inválidos.")
            return redirect("core:login")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Você saiu do sistema.")
    return redirect("core:login")


def dashboard_admin(request):
    contexto = {
        "total_usuarios": Usuario.objects.count(),
        "total_unidades": UnidadeSaude.objects.count(),
        "total_profissionais": Profissional.objects.count(),
        "total_tipos_exames": TipoExame.objects.count(),
    }

    return render(request, "dashboard/admin.html", contexto)


def dashboard_cidadao(request):
    return render(request, "dashboard/cidadao.html")


def dashboard_profissional(request):
    return render(request, "dashboard/profissional.html")


def relatorios(request):
    status = request.GET.get("status")
    unidade_id = request.GET.get("unidade")
    tipo_id = request.GET.get("tipo")

    exames = Exame.objects.all()

    if status:
        exames = exames.filter(status=status)

    if unidade_id:
        exames = exames.filter(unidade_id=unidade_id)

    contexto = {
        "total_usuarios": Usuario.objects.count(),
        "total_unidades": UnidadeSaude.objects.count(),
        "total_profissionais": Profissional.objects.count(),
        "total_exames": exames.count(),
        "exames": exames,
        "unidades": UnidadeSaude.objects.all(),
        "tipos": TipoExame.objects.all(),
        "status_choices": Exame.STATUS_CHOICES,
        "status_selecionado": status,
        "unidade_selecionada": unidade_id,
        "tipo_selecionado": tipo_id,
    }

    return render(request, "relatorio/relatorios.html", contexto)