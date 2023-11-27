# Generated by Django 4.2.4 on 2023-09-01 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_remove_inscricao_cadeira_feita'),
    ]

    operations = [
        migrations.CreateModel(
            name='CadeiraConcluida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cadeira', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.cadeira')),
                ('estudante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.estudante')),
            ],
        ),
    ]
