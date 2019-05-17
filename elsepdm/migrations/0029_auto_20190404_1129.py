# Generated by Django 2.1.7 on 2019-04-04 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elsepdm', '0028_auto_20190324_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='componentasset',
            name='asset_type',
            field=models.CharField(choices=[('MODEL_ASSET', 'Model asset'), ('PREVIEW_ASSET', 'Preview asset'), ('B4W_ASSET', 'B4W asset'), ('TOUR_GIF_ASSET', 'Tour gif asset'), ('FRAMES_ASSET', 'Frames asset'), ('OBJ_ASSET', 'Obj asset')], max_length=255),
        ),
        migrations.AlterField(
            model_name='productasset',
            name='asset_type',
            field=models.CharField(choices=[('MODEL_ASSET', 'Model asset'), ('PREVIEW_ASSET', 'Preview asset'), ('B4W_ASSET', 'B4W asset'), ('TOUR_GIF_ASSET', 'Tour gif asset'), ('FRAMES_ASSET', 'Frames asset'), ('OBJ_ASSET', 'Obj asset')], max_length=255),
        ),
    ]
