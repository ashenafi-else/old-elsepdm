# Generated by Django 2.0 on 2019-01-28 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elsepdm', '0022_default_values_for_components_and_elements'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='revision_number',
            new_name='active_revision',
        ),
        migrations.AlterField(
            model_name='productcomponent',
            name='name',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='productelement',
            name='active_color',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='productelement',
            name='active_material',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='productelement',
            name='name',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='productstructure',
            name='name',
            field=models.CharField(default='', max_length=64),
        ),
    ]
