# Generated by Django 2.0 on 2018-10-02 14:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('elsepdm', '0016_auto_20180928_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='productrevision',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
