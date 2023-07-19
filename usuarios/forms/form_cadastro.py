from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.forms_django import senha_forte


class RegisterForm(forms.ModelForm):

    senha = forms.CharField(
        required=True,
        validators=[senha_forte],
        label='Senha'
    )

    senha_repetida = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Repita a Senha'
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        labels = {
            'username': 'Username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'E-mail',
        }

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('senha')
        password2 = cleaned_data.get('senha_repetida')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Password and password2 must be equal',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ],
            })

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'User e-mail is already in use', code='invalid',
            )

        return email
