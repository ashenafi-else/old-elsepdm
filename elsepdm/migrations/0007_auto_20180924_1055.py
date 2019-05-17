# Generated by Django 2.0 on 2018-09-24 10:55

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('elsepdm', '0006_auto_20180924_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='damasset',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Creation date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='damasset',
            name='name',
            field=models.CharField(default='', max_length=64, verbose_name='Name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='damasset',
            name='resource_type',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='damasset',
            name='temporary',
            field=models.BooleanField(default=False, verbose_name='Temporary'),
        ),
        migrations.AddField(
            model_name='damasset',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
