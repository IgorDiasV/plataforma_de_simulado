
import re
from django.core.exceptions import ValidationError


def senha_forte(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'A senha precisa conter, uma ou mais letras minusculas, '
            'uma ou mais letras maiusculas,'
            'um ou mais números e pelo menos 8 caracteres'
        ))
    
    