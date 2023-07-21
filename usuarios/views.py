from django.shortcuts import render, redirect
from .forms import FormCadastro
from django.urls import reverse
from django.http import Http404
from usuarios.models import Usuario


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
