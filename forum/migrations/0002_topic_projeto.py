# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-28 17:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projetos', '0002_auto_20160415_1528'),
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='projeto',
            field=models.ForeignKey(default=1, max_length=50, on_delete=django.db.models.deletion.CASCADE, to='projetos.Projeto'),
            preserve_default=False,
        ),
    ]
