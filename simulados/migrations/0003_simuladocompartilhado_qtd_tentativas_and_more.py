# Generated by Django 4.2.2 on 2023-08-03 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulados', '0002_simulado_compartilhado_alter_simulado_autor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='simuladocompartilhado',
            name='qtd_tentativas',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='simuladocompartilhado',
            name='tempo_de_prova',
            field=models.IntegerField(default=0),
        ),
    ]