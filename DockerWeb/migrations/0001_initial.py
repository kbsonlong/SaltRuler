# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='registry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=100)),
                ('version', models.IntegerField(verbose_name=10)),
                ('status', models.IntegerField(verbose_name=5)),
                ('isactive', models.IntegerField(verbose_name=5)),
                ('auth', models.CharField(max_length=30)),
            ],
        ),
    ]
