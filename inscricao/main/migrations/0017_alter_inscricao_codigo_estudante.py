# Generated by Django 4.2.4 on 2023-11-13 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_alter_inscricao_codigo_estudante'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inscricao',
            name='codigo_estudante',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]