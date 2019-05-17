import os

from azure.storage.blob import (
    ContentSettings,
    BlockBlobService,
)


class StorageService(object):

    def put_by_stream(self, path, stream, content_type):
        raise NotImplemented

    def put_by_url(self, path, file_url):
        raise NotImplemented

    def remove(self, path):
        raise NotImplemented

    def generate_path(self, dam_asset):
        raise NotImplemented

    def generate_url(self, dam_asset):
        raise NotImplemented


class AzureService(StorageService):
    def put_by_stream(self, path, stream, content_type):
        blob_service = BlockBlobService(
            account_name=self.account_name,
            account_key=self.account_key,
        )
        if not blob_service.exists(self.container):
            blob_service.create_container(self.container)
        blob_service.create_blob_from_stream(
            self.container,
            path,
            stream,
            content_settings=ContentSettings(content_type=content_type)
        )

    def put_by_url(self, path, file_url):
        blob_service = BlockBlobService(
            account_name=self.account_name,
            account_key=self.account_key,
        )
        if not blob_service.exists(self.container):
            blob_service.create_container(self.container)
        blob_service.copy_blob(
            self.container,
            path,
            file_url,
        )

    def remove(self, path):
        blob_service = BlockBlobService(
            account_name=self.account_name,
            account_key=self.account_key,
        )
        blob_service.delete_blob(
            self.container,
            path
        )

    def generate_path(self, dam_asset):
        filename = dam_asset.filename
        relative_path = dam_asset.relative_path or ''
        if dam_asset.extension:
            filename = dam_asset.filename + dam_asset.extension
        path_parts = [
            dam_asset.location.path,
            dam_asset.batch.resource_type,
            str(dam_asset.batch.uuid),
            relative_path,
            filename,
        ]
        return os.path.join(*path_parts)

    def generate_url(self, dam_asset):
        url_parts = [
            self.domain,
            dam_asset.location.child_location.container,
            self.generate_path(dam_asset).replace(os.sep, '/'),
        ]
        return '/'.join(part.strip('/') for part in url_parts)
