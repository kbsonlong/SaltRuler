# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DockerWeb', '0003_auto_20170412_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registry',
            name='auth',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
