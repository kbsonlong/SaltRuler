# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetmanage',
            name='cputype_num',
            field=models.IntegerField(default=0, verbose_name=20),
        ),
        migrations.AlterField(
            model_name='assetmanage',
            name='memsize_num',
            field=models.IntegerField(default=0, verbose_name=20),
        ),
    ]
