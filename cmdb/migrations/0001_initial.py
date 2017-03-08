# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assetmanage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('asset_num', models.CharField(unique=True, max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('server_ip', models.CharField(unique=True, max_length=20)),
                ('remote_ip', models.CharField(max_length=20)),
                ('data_center', models.CharField(max_length=50)),
                ('room_num', models.CharField(max_length=20)),
                ('rack_num', models.CharField(max_length=20)),
                ('system_type', models.CharField(default=b'-', max_length=20)),
                ('cputype_num', models.CharField(default=b'-', max_length=20)),
                ('disksize_num', models.CharField(default=b'-', max_length=20)),
                ('memsize_num', models.CharField(default=b'-', max_length=20)),
                ('disk_raid', models.CharField(default=b'-', max_length=20)),
                ('card_type_num', models.CharField(default=b'-', max_length=20)),
                ('power_num', models.CharField(default=b'-', max_length=20)),
                ('service_num', models.CharField(unique=True, max_length=50)),
                ('buy_time', models.CharField(default=b'-', max_length=50)),
                ('expiration_time', models.CharField(default=b'-', max_length=50)),
                ('note', models.CharField(default=b'-', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Hostinfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('local_ip', models.CharField(unique=True, max_length=20)),
                ('app', models.CharField(default=b'-', max_length=50)),
                ('host_note', models.CharField(default=b'-', max_length=200)),
                ('host_ip', models.ForeignKey(related_name='asset_set', to='cmdb.Assetmanage')),
            ],
        ),
    ]
