# Generated by Django 2.0 on 2018-09-14 13:56

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('elsepdm', '0003_auto_20180914_1338'),
    ]

    operations = [
        migrations.CreateModel(
            name='DamAsset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(editable=False, unique=True)),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('resource_type', models.CharField(max_length=255)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('temporary', models.BooleanField(default=False, verbose_name='Temporary')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='asset',
            name='creation_date',
        ),
        migrations.RemoveField(
            model_name='asset',
            name='resource_type',
        ),
        migrations.RemoveField(
            model_name='asset',
            name='temporary',
        ),
        migrations.AlterField(
            model_name='asset',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AddField(
            model_name='asset',
            name='dam_asset',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='elsepdm.DamAsset'),
            preserve_default=False,
        ),
    ]
