#!/usr/local/python27/bin/python
# coding: utf-8
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')
os.environ.setdefault("DJANGO_SETTINGS_MODULE","SaltRuler.settings")
from django.core.handlers.wsgi import WSGIHandler
import django
django.setup()
application = WSGIHandler()