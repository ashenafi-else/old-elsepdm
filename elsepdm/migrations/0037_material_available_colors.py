# Generated by Django 2.1.7 on 2019-05-24 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elsecmh', '0031_auto_20190516_1505'),
        ('elsepdm', '0036_auto_20190516_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='available_colors',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='elsecmh.Color'),
        ),
    ]