# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-17 15:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Layout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='版型名稱', max_length=32)),
                ('identifier', models.SlugField(db_index=False, help_text='版型識別碼', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='範本名稱', max_length=32)),
                ('author', models.CharField(help_text='範本作者', max_length=32)),
                ('description', models.TextField(blank=True, help_text='範本說明文字')),
                ('path', models.FilePathField(help_text='範本檔案位置', match='\\.mustache$', max_length=128, path='/opt/weekly', recursive=True)),
            ],
        ),
        migrations.AddField(
            model_name='layout',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='templates.Template'),
        ),
    ]
