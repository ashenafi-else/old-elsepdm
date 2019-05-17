# Generated by Django 2.0 on 2018-09-27 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elsepdm', '0009_auto_20180925_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elsepdm.Brand'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_hierarchy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elsepdm.ProductHierarchy'),
        ),
    ]
