from django.db import models
from elsedam.services import (
    AzureService,
    StorageService,
)
from elsepublic.models import Base
from django.contrib.postgres.fields import ArrayField


class Brand(Base):
    brand_external_id = models.CharField(
        unique=True,
        max_length=64,
        help_text='Middleware id',
    )
    is_default = models.BooleanField(default=False)


class Storage(Base, StorageService):
    TYPE_PUBLIC = 'public'
    TYPE_PRIVATE = 'private'
    TYPE_BUFFERED = 'buffered'

    STORAGE_TYPES = (
        (TYPE_PUBLIC, 'Public'),
        (TYPE_PRIVATE, 'Private'),
        (TYPE_BUFFERED, 'Buffered')
    )

    brand = models.ForeignKey(Brand, null=True, on_delete=models.DO_NOTHING)
    domain = models.CharField(max_length=255, null=False)
    storage_type = models.CharField(choices=STORAGE_TYPES, max_length=255)
    is_default = models.BooleanField(default=False)
    model_type = models.CharField(default='storage', max_length=255)

    def save(self, keep_deleted=False, **kwargs):
        self.model_type = self.__class__.__name__.lower()
        super(Storage, self).save(keep_deleted, **kwargs)

    @property
    def child_storage(self):
        if self.model_type != 'storage':
            return getattr(self, self.model_type)
        return None


class StorageLocation(Base):
    path = models.CharField(max_length=255, null=True)
    storage = models.ForeignKey(
        Storage,
        null=True,
        related_name='locations',
        on_delete=models.DO_NOTHING,
    )
    model_type = models.CharField(default='storagelocation', max_length=255)

    @property
    def child_location(self):
        if self.model_type != 'storagelocation':
            return getattr(self, self.model_type)
        return None

    @property
    def full_path(self):
        raise NotImplemented

    def save(self, keep_deleted=False, **kwargs):
        self.model_type = self.__class__.__name__.lower()
        super(StorageLocation, self).save(keep_deleted, **kwargs)


class AzureStorage(Storage, AzureService):
    account_name = models.CharField(max_length=255)
    account_key = models.CharField(max_length=255)
    container = models.CharField(max_length=255)
    storage_timeout = models.IntegerField(null=True, blank=True)


class AzureStorageLocation(StorageLocation):
    container = models.CharField(max_length=255)

    @property
    def full_path(self):
        return '{}/{}'.format(self.container, self.path)


class StorageGroup(Base):
    file_extensions = ArrayField(models.CharField(max_length=200), blank=True)
    mime_types = ArrayField(models.CharField(max_length=200), blank=True)
    name = models.CharField(verbose_name='Name', max_length=64)
    tags = ArrayField(models.CharField(max_length=200), blank=True)
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={'is_default': True},
    )
    location = models.ForeignKey(
        StorageLocation,
        related_name='storage_groups',
        null=True,
        on_delete=models.DO_NOTHING,
    )


class BaseAsset(Base):
    filename = models.CharField(max_length=255)
    extension = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=255)
    size = models.BigIntegerField()
    tags = ArrayField(models.CharField(max_length=200), blank=True)
    file = models.FileField(null=True, blank=True)
    brand_id = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        abstract = True


class CdnDamAsset(models.Model):
    """
    Class for working with cdn dam assets

    .. deprecated

        Deprecated for the reason of architecture changes
    """
    UPLOADING_STATE = 'uploading'
    UPLOADED_STATE = 'uploaded'
    FAILED_STATE = 'failed_to_upload'

    STATES = (
        (UPLOADING_STATE, 'Uploading'),
        (UPLOADED_STATE, 'Uploaded'),
        (FAILED_STATE, 'FailedToUpload')
    )

    cdn_url = models.CharField(max_length=255)
    state = models.CharField(max_length=64, choices=STATES)


class DamAsset(BaseAsset):
    UPLOADING_STATE = 'uploading'
    UPLOADED_STATE = 'uploaded'
    FAILED_STATE = 'failed_to_upload'
    FAILED_REMOVE_STATE = 'failed_to_remove'

    STATES = (
        (UPLOADING_STATE, 'Uploading'),
        (UPLOADED_STATE, 'Uploaded'),
        (FAILED_STATE, 'FailedToUpload'),
        (FAILED_REMOVE_STATE, 'FailedToRemove'),
    )

    batch = models.ForeignKey(
        'DamAssetBatch',
        related_name='assets',
        on_delete=models.CASCADE,
    )
    state = models.CharField(max_length=255, choices=STATES)
    description = models.TextField(verbose_name='About', blank=True)
    temporary = models.BooleanField(verbose_name='Temporary', default=False)
    group = models.ForeignKey(
        StorageGroup,
        related_name='assets',
        on_delete=models.DO_NOTHING,
        null=True,
    )
    url = models.URLField(null=True)
    location = models.ForeignKey(
        StorageLocation,
        related_name='assets',
        null=True,
        on_delete=models.DO_NOTHING,
    )
    meta_info = models.TextField(null=True, blank=True)
    relative_path = models.CharField(max_length=255, null=True, blank=True)

    def generate_path(self, dir_name=None):
        if not dir_name:
            dir_name = str(self.uuid)
        filename = self.filename
        if self.extension:
            filename = self.filename + self.extension
        url_parts = [
            self.location.path,
            self.resource_type,
            dir_name,
            filename,
        ]
        return '/'.join(part.strip('/') for part in url_parts)

    def generate_url(self, dir_name):
        if not dir_name:
            dir_name = str(self.uuid)
        filename = self.filename
        if self.extension:
            filename = self.filename + self.extension
        url_parts = [
            self.location.storage.domain,
            self.location.child_location.full_path,
            self.resource_type,
            dir_name,
            filename,
        ]
        return '/'.join(part.strip('/') for part in url_parts)


class BufferedDamAsset(Base):
    BUFFERING_STATE = 'buffering'
    BUFFERED_STATE = 'buffered'
    FAILED_STATE = 'failed_to_buffer'
    FAILED_REMOVE_STATE = 'failed_to_remove'

    STATES = (
        (BUFFERING_STATE, 'Buffering'),
        (BUFFERED_STATE, 'Buffered'),
        (FAILED_STATE, 'FailedToBuffer'),
        (FAILED_REMOVE_STATE, 'FailedToRemove'),
    )

    buffer_url = models.CharField(max_length=255)
    state = models.CharField(
        max_length=64,
        choices=STATES,
        default=BUFFERING_STATE,
    )
    last_request = models.DateTimeField(null=True, blank=True, auto_now=True)
    for_removing = models.BooleanField(default=False)
    dam_asset = models.OneToOneField(
        DamAsset,
        related_name='buffered_asset',
        on_delete=models.DO_NOTHING,
        null=True,
    )
    buffer_path = models.CharField(max_length=255, null=True)
    location = models.ForeignKey(
        StorageLocation,
        related_name='buffered_assets',
        null=True,
        on_delete=models.DO_NOTHING,
    )
    meta_info = models.TextField(null=True, blank=True)

    def generate_path(self):
        filename = self.dam_asset.filename
        if self.dam_asset.extension:
            filename = self.dam_asset.filename + self.dam_asset.extension
        url_parts = [self.location.path, self.dam_asset.resource_type,
                     str(self.dam_asset.uuid), filename]
        return '/'.join(part.strip('/') for part in url_parts)

    def generate_url(self):
        filename = self.dam_asset.filename
        if self.dam_asset.extension:
            filename = self.dam_asset.filename + self.dam_asset.extension
        url_parts = [
            self.location.storage.domain,
            self.location.child_location.full_path,
            self.dam_asset.resource_type,
            str(self.dam_asset.uuid),
            filename,
        ]
        return '/'.join(part.strip('/') for part in url_parts)


class DamAssetRequest(Base):
    buffered_asset = models.ForeignKey(
        BufferedDamAsset,
        related_name='requests',
        on_delete=models.DO_NOTHING,
        null=True,
    )


class DamAssetBatch(Base):
    resource_type = models.CharField(max_length=255)
    initiator = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
