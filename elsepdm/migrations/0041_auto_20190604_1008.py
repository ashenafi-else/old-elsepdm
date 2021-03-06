# Generated by Django 2.1.7 on 2019-06-04 10:08

import django.contrib.postgres.fields
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('elsepdm', '0040_auto_20190603_1346'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='materialimplementation',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='materialimplementation',
            name='color',
        ),
        migrations.RemoveField(
            model_name='materialimplementation',
            name='material',
        ),
        migrations.RemoveField(
            model_name='material',
            name='available_colors',
        ),
        migrations.AddField(
            model_name='material',
            name='colors_uuids',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True), default=list, size=None),
        ),
        migrations.DeleteModel(
            name='Color',
        ),
        migrations.DeleteModel(
            name='MaterialImplementation',
        ),
    ]
