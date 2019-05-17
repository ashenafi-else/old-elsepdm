# Generated by Django 2.0 on 2018-12-17 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elsedam', '0024_create_default_brand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='azurestorage',
            name='account_key',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='azurestorage',
            name='account_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='azurestorage',
            name='container',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='azurestoragelocation',
            name='container',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='storage',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='elsedam.Brand'),
        ),
        migrations.AlterField(
            model_name='storage',
            name='model_type',
            field=models.CharField(default='storage', max_length=255),
        ),
        migrations.AlterField(
            model_name='storage',
            name='storage_type',
            field=models.CharField(choices=[('public', 'Public'), ('private', 'Private'), ('buffered', 'Buffered')], max_length=255),
        ),
        migrations.AlterField(
            model_name='storagelocation',
            name='model_type',
            field=models.CharField(default='storagelocation', max_length=255),
        ),
        migrations.AlterField(
            model_name='storagelocation',
            name='path',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='storagelocation',
            name='storage',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='locations', to='elsedam.Storage'),
        ),
    ]
