# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='file_history',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=30)),
                ('active', models.CharField(max_length=30)),
                ('path', models.CharField(max_length=300)),
                ('active_time', models.DateTimeField()),
            ],
        ),
        migrations.DeleteModel(
            name='Upload',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
