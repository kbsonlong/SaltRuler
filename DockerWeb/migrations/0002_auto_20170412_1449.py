# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DockerWeb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registry',
            name='isactive',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='registry',
            name='name',
            field=models.CharField(unique=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='registry',
            name='status',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='registry',
            name='version',
            field=models.IntegerField(),
        ),
    ]
