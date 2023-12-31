# Generated by Django 4.2.4 on 2023-09-07 08:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_delete_inscricao'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inscricao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_inscricao', models.DateTimeField(auto_now_add=True)),
                ('feito', models.BooleanField(default=False)),
                ('cadeira', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.cadeira')),
                ('estudante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.estudante')),
            ],
        ),
    ]
