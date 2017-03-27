# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0002_auto_20170324_0949'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='file_history',
            new_name='files_history',
        ),
    ]
