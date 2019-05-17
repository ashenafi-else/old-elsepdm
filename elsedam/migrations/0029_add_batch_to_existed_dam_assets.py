import os
import uuid

from django.db import migrations, models
import django.db.models.deletion


def valid_uuid(uuid_string):
    try:
        validated_uuid = uuid.UUID(uuid_string)
    except:
        return False
    return True


def add_batch_to_dam_assets(apps, schema_editor):
    DamAssetBatch = apps.get_model('elsedam', 'DamAssetBatch')
    DamAsset = apps.get_model('elsedam', 'DamAsset')
    dam_assets = DamAsset.objects.all()
    for dam_asset in dam_assets:
        url = dam_asset.url if dam_asset.url else ''
        dir_name = os.path.basename(os.path.dirname(url))
        if valid_uuid(dir_name):
            batch, created = DamAssetBatch.objects.get_or_create(
                uuid=dir_name,
                resource_type='makemigrations',
                initiator='makemigrations',
            )
            dam_asset.batch = batch
        else:
            batch = DamAssetBatch.objects.create(
                resource_type='makemigrations',
                initiator='makemigrations',
            )
            dam_asset.batch = batch
            storage = dam_asset.group.location.storage
            storage = getattr(storage, storage.model_type)
            path = storage.generate_path(dam_asset)
            try:
                storage.put_by_url(path, dam_asset.url)
            except Exception as err:
                dam_asset.meta_info = str(err)
            else:
                location = getattr(dam_asset.location, dam_asset.location.model_type)
                url_parts = [storage.domain, location.container, storage.generate_path(dam_asset)]
                dam_asset.url = os.path.join(*url_parts)
        dam_asset.save()


class Migration(migrations.Migration):

    dependencies = [
        ('elsedam', '0028_auto_20190306_1307'),
    ]

    operations = [
        migrations.RunPython(add_batch_to_dam_assets, lambda apps, schema_editor: None),
        migrations.AlterField(
            model_name='damasset',
            name='batch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assets', to='elsedam.DamAssetBatch'),
        ),
    ]
