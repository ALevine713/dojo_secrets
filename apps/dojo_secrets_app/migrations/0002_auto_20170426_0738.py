# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-26 14:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dojo_secrets_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='sectret',
            new_name='secret',
        ),
    ]