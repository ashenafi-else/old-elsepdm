# Generated by Django 2.0 on 2018-09-14 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elsepdm', '0004_auto_20180914_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templateproduct',
            name='dam_asset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elsepdm.DamAsset'),
        ),
    ]