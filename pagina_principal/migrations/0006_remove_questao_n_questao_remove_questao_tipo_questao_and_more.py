# Generated by Django 4.2.2 on 2023-07-21 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
        ('pagina_principal', '0005_alter_simulado_titulo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questao',
            name='n_questao',
        ),
        migrations.RemoveField(
            model_name='questao',
            name='tipo_questao',
        ),
        migrations.AddField(
            model_name='questao',
            name='autor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='usuarios.usuario'),
        ),
        migrations.AddField(
            model_name='simulado',
            name='autor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='usuarios.usuario'),
        ),
    ]