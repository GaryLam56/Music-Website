# -*- coding: utf-8 -*-
# Generated by Django 1.10a1 on 2016-06-22 20:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0008_album_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folder_name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='song',
            name='folder',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='music.Folder'),
            preserve_default=False,
        ),
    ]
