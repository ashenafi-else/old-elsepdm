# Generated by Django 2.1.7 on 2019-04-19 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elsepdm', '0030_shoepairsettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoePairSettingsProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Shoe pair settings',
                'verbose_name_plural': 'Shoe pair settings',
                'proxy': True,
                'indexes': [],
            },
            bases=('elsepdm.shoepairsettings',),
        ),
    ]
