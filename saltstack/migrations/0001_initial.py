# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SaltServer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('idc', models.CharField(max_length=100, verbose_name='\u6240\u5c5e\u673a\u623f')),
                ('url', models.URLField(max_length=100, verbose_name='URL\u5730\u5740')),
                ('username', models.CharField(max_length=50, verbose_name='\u7528\u6237\u540d')),
                ('password', models.CharField(max_length=50, verbose_name='\u5bc6\u7801')),
                ('role', models.CharField(default=b'Master', max_length=20, verbose_name='\u89d2\u8272', choices=[(b'Master', b'Master'), (b'Backend', b'Backend')])),
            ],
            options={
                'verbose_name': 'Salt\u670d\u52a1\u5668',
                'verbose_name_plural': 'Salt\u670d\u52a1\u5668\u5217\u8868',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client', models.CharField(max_length=20, verbose_name='\u6267\u884c\u65b9\u5f0f', blank=True)),
                ('fun', models.CharField(max_length=50, verbose_name='\u547d\u4ee4')),
                ('arg', models.CharField(max_length=255, verbose_name='\u53c2\u6570', blank=True)),
                ('tgt_type', models.CharField(max_length=20, verbose_name='\u76ee\u6807\u7c7b\u578b')),
                ('jid', models.CharField(max_length=50, verbose_name='\u4efb\u52a1\u53f7', blank=True)),
                ('minions', models.CharField(max_length=500, verbose_name='\u76ee\u6807\u4e3b\u673a', blank=True)),
                ('result', models.TextField(verbose_name='\u8fd4\u56de\u7ed3\u679c', blank=True)),
                ('user', models.CharField(max_length=50, verbose_name='\u64cd\u4f5c\u7528\u6237')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='\u6267\u884c\u65f6\u95f4')),
                ('server', models.ForeignKey(verbose_name='\u6240\u5c5eSalt\u670d\u52a1\u5668', to='saltstack.SaltServer')),
            ],
            options={
                'verbose_name': '\u90e8\u7f72\u7ed3\u679c',
                'verbose_name_plural': '\u90e8\u7f72\u7ed3\u679c',
            },
        ),
        migrations.CreateModel(
            name='SvnProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='\u9879\u76ee\u540d\u79f0', blank=True)),
                ('host', models.CharField(max_length=50, verbose_name='\u9879\u76ee\u4e3b\u673a')),
                ('path', models.CharField(max_length=200, verbose_name='\u9879\u76ee\u6839\u8def\u5f84')),
                ('target', models.CharField(max_length=50, verbose_name='\u9879\u76ee\u76ee\u5f55')),
                ('script', models.CharField(max_length=50, verbose_name='\u9879\u76ee\u542f\u52a8\u811a\u672c')),
                ('url', models.CharField(max_length=200, verbose_name='SVN\u5730\u5740')),
                ('username', models.CharField(max_length=40, verbose_name='SVN\u8d26\u53f7')),
                ('password', models.CharField(max_length=40, verbose_name='SVN\u5bc6\u7801', blank=True)),
                ('status', models.CharField(default='\u65b0\u5efa', max_length=40, verbose_name='\u72b6\u6001')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('info', models.TextField(max_length=500, verbose_name='\u4fe1\u606f', blank=True)),
                ('salt_server', models.ForeignKey(verbose_name='\u6240\u5c5eSalt\u670d\u52a1\u5668', to='saltstack.SaltServer')),
            ],
            options={
                'verbose_name': 'SVN\u9879\u76ee',
                'verbose_name_plural': 'SVN\u9879\u76ee\u5217\u8868',
            },
        ),
        migrations.AlterUniqueTogether(
            name='svnproject',
            unique_together=set([('host', 'path', 'target')]),
        ),
    ]
