# Generated by Django 4.2.4 on 2023-09-01 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_configuracoes_periodo_inscricao_aberto_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inscricao',
            name='cadeira_feita',
        ),
    ]
