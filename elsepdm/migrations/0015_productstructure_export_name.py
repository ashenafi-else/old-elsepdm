# Generated by Django 2.0 on 2018-09-28 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elsepdm', '0014_auto_20180928_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='productstructure',
            name='export_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]