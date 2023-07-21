from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class FormLogin(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )


class FormCadastro(forms.ModelForm):

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Senha'
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Confirmar Senha'
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
        ]
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
        }

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            erro_de_confirmacao_de_senha = ValidationError(
                'As Senhas digitadas são diferentes',
                code='invalid'
            )
            raise ValidationError({
                'password': erro_de_confirmacao_de_senha,
                'password2': [
                    erro_de_confirmacao_de_senha,
                ],
            })

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'O Email já está em uso', code='invalid',
            )

        return email
