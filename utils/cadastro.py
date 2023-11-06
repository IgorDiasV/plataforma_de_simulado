import re
from django.core.exceptions import ValidationError


def senhar_forte(senha):
    regex = re.compile(r'^.{8,}$')

    if not regex.match(senha):
        raise ValidationError((
            'A senha precisa conter no mínimo 8 caracteres'
        ),
            code='invalid'
        )