from django.shortcuts import render, redirect
from .forms import FormCadastro, FormLogin
from django.urls import reverse
from django.http import Http404
from usuarios.models import Usuario
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def cadastro_view(request):
    cadastro_armazenado = request.session.get('cadastro_armazenado', None)
    form = FormCadastro(cadastro_armazenado)

    return render(request, 'usuarios/cadastro_view.html', {
        'form': form,
        'form_action': reverse('usuarios:salvar_cadastro'),
    })


def salvar_cadastro(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['cadastro_armazenado'] = POST
    form = FormCadastro(POST)

    if form.is_valid():
        usuario = form.save(commit=False)
        usuario.username = usuario.email
        usuario.set_password(usuario.password)
        usuario.save()
        Usuario.objects.create(user=usuario, is_teacher=POST['is_teacher'])
        # messages.success(request, 'Your user is created, please log in.')

        del (request.session['cadastro_armazenado'])
        return redirect(reverse('home'))

    return redirect('usuarios:cadastro')


def login_view(request):
    form = FormLogin()
    return render(request, 'usuarios/login.html', {
        'form': form,
        'form_action': reverse('usuarios:realizar_login')
    })


def realizar_login(request):
    if not request.POST:
        raise Http404()

    form = FormLogin(request.POST)

    if form.is_valid():
        usuario_autenticado = authenticate(
            username=form.cleaned_data.get('email', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if usuario_autenticado is not None:

            login(request, usuario_autenticado)

    return redirect(reverse('home'))


@login_required(login_url='usuarios:login', redirect_field_name='next')
def logout_view(request):
    if request.method == 'GET':
        return redirect('home')
    else:
        if request.POST.get('username') != request.user.username:
            return redirect('usuarios:login')
        logout(request)
        return redirect('usuarios:login')
