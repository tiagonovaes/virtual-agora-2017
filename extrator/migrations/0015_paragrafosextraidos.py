# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-24 19:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extrator', '0014_dadosmapeamentoeextracao_extracaoparagrafosetapa1'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParagrafosExtraidos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paragrafo', models.TextField(verbose_name='Paragrafo')),
                ('protofrase', models.TextField(verbose_name='Proto-Frase')),
                ('arquivo', models.TextField(verbose_name='arquivo')),
                ('dataHora', models.TextField(verbose_name='Data_Hora')),
            ],
        ),
    ]
