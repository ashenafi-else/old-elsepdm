# Generated by Django 2.1.7 on 2019-05-24 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elsepdm', '0038_auto_20190524_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configurationelement',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='active_material', to='elsepdm.Material'),
        ),
    ]