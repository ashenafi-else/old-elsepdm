# Generated by Django 2.0 on 2018-09-27 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elsepdm', '0010_auto_20180927_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='activity_log',
            field=models.TextField(null=True),
        ),
    ]