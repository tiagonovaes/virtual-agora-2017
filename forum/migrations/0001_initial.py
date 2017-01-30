# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-15 17:57
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('projetos', '__first__'),
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('projeto', models.ForeignKey(max_length=50, on_delete=django.db.models.deletion.CASCADE, to='projetos.Projeto')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'categoria',
                'verbose_name_plural': 'categorias',
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'curtir',
                'verbose_name_plural': 'curtires',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name=b'T\xc3\xadtulo')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Texto')),
                ('pub_date', models.DateTimeField(verbose_name=b'Data de publica\xc3\xa7\xc3\xa3o')),
                ('published', models.CharField(default=b'N\xc3\xa3o', max_length=3, verbose_name=b'Publicado?')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Category')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 't\xf3pico',
                'verbose_name_plural': 't\xf3picos',
            },
        ),
        migrations.CreateModel(
            name='TopicAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(verbose_name=b'')),
                ('answer_date', models.DateTimeField(editable=False)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.Topic')),
            ],
            options={
                'verbose_name': 'resposta',
                'verbose_name_plural': 'respostas',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(default=b'username', max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='topic_user', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('topic_answer', models.ManyToManyField(related_name='topic_answer', through='forum.TopicAnswer', to='forum.Topic')),
                ('topic_answer_like', models.ManyToManyField(related_name='topic_answer_like', through='forum.Like', to='forum.TopicAnswer')),
            ],
            options={
                'verbose_name': 'usu\xe1rio',
                'verbose_name_plural': 'usu\xe1rios',
            },
        ),
        migrations.AddField(
            model_name='topicanswer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.User'),
        ),
        migrations.AddField(
            model_name='like',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.TopicAnswer'),
        ),
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.User'),
        ),
    ]
