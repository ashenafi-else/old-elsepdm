# Generated by Django 2.0 on 2018-10-09 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elsedam', '0007_damasset_product_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='damassetrequest',
            name='asset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='elsedam.BufferedDamAsset'),
        ),
    ]
