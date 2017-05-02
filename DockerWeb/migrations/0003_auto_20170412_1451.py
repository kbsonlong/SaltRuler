# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DockerWeb', '0002_auto_20170412_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registry',
            name='isactive',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='registry',
            name='status',
            field=models.IntegerField(null=True),
        ),
    ]
