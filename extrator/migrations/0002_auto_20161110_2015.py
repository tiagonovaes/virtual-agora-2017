# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-10 22:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extrator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tabelaranking',
            name='betweenness',
            field=models.FloatField(verbose_name='Betweenness'),
        ),
        migrations.AlterField(
            model_name='tabelaranking',
            name='closeness',
            field=models.FloatField(verbose_name='Closeness'),
        ),
    ]
