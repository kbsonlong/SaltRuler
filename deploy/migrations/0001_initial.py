# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='files_history',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=30)),
                ('active', models.CharField(max_length=30)),
                ('path', models.CharField(max_length=300)),
                ('active_time', models.DateTimeField()),
                ('remote_server', models.CharField(max_length=300)),
                ('url', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('headImg', models.ImageField(upload_to=b'./upload/')),
            ],
        ),
    ]
