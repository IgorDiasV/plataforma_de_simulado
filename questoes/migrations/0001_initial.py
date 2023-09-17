# Generated by Django 4.2.2 on 2023-09-17 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("usuarios", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Assunto",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("nome_assunto", models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Questao",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("curso", models.TextField(default="Não Cadastrado")),
                ("origem", models.TextField(default="Outros")),
                ("ano", models.BigIntegerField(default=-1, null=True)),
                ("pergunta", models.TextField(default="none")),
                ("alternativa_a", models.TextField(default="none")),
                ("alternativa_b", models.TextField(default="none")),
                ("alternativa_c", models.TextField(default="none")),
                ("alternativa_d", models.TextField(default="none")),
                ("alternativa_e", models.TextField(default="none")),
                ("alternativa_correta", models.CharField(max_length=1)),
                ("assuntos", models.ManyToManyField(to="questoes.assunto")),
                (
                    "autor",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="usuarios.usuario",
                    ),
                ),
            ],
        ),
    ]
