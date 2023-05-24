from unittest import TestCase
from unittest.mock import patch, call

from src.label_studio_api import LabelStudioApi


class StorageConnectionsTests(TestCase):
    @patch("requests.post")
    def test_create_source_storage_connection(self, post_mock):
        # Given
        label_studio_api = LabelStudioApi(
            host="label_studio_host",
            port="label_studio_port",
            api_token="label_studio_api_token",
        )
        # When
        label_studio_api.create_source_azure_storage_connection(
            project_id=1234,
            connection_name="connection name",
            description="connection description",
            storage_account="storage account name",
            storage_account_key="storage account key",
            container="container_name",
            prefix="path/to/content",
        )
        # Then
        post_mock.assert_called_once_with(
            url="http://label_studio_host:label_studio_port/api/storages/azure",
            headers={
                "Authorization": "Token label_studio_api_token",
                "Content-Type": "application/json",
            },
            json={
                "project": 1234,
                "title": "connection name",
                "account_name": "storage account name",
                "account_key": "storage account key",
                "container": "container_name",
                "presign_ttl": 0,
                "use_blob_urls": True,
                "prefix": "path/to/content",
                "description": "connection description",
            }
        )

    @patch("requests.post")
    def test_create_target_storage_connection(self, post_mock):
        # Given
        label_studio_api = LabelStudioApi(
            host="label_studio_host",
            port="label_studio_port",
            api_token="label_studio_api_token",
        )
        # When
        label_studio_api.create_target_azure_storage_connection(
            project_id=1234,
            connection_name="connection name",
            description="connection description",
            storage_account="storage account name",
            storage_account_key="storage account key",
            container="container_name",
            prefix="path/to/content",
        )
        # Then
        post_mock.assert_called_once_with(
            url="http://label_studio_host:label_studio_port/api/storages/export/azure",
            headers={
                "Authorization": "Token label_studio_api_token",
                "Content-Type": "application/json",
            },
            json={
                "project": 1234,
                "title": "connection name",
                "account_name": "storage account name",
                "account_key": "storage account key",
                "container": "container_name",
                "use_blob_urls": True,
                "prefix": "path/to/content",
                "description": "connection description",
            }
        )

    @patch("src.label_studio_api.LabelStudioApi.create_target_azure_storage_connection")
    @patch("src.label_studio_api.LabelStudioApi.create_source_azure_storage_connection")
    def test_create_storage_connections_from_configuration_file(
            self,
            create_source_azure_storage_connection_mock,
            create_target_azure_storage_connection_mock,
    ):
        # Given
        label_studio_api = LabelStudioApi(
            host="label_studio_host",
            port="label_studio_port",
            api_token="label_studio_api_token",
        )
        # When
        label_studio_api.create_azure_storage_connections_from_configuration_file(
            configuration_file="test/helpers/azure_storage_configuration.yaml"
        )
        # Then
        self.assertEqual(create_source_azure_storage_connection_mock.call_count, 2)
        create_source_azure_storage_connection_mock.assert_has_calls([
            call(
                project_id=1234,
                connection_name="connection name",
                description="connection description",
                storage_account="storage account name",
                storage_account_key="storage account key",
                container="container_name",
                prefix="source/folder",
            ),
            call(
                project_id=1234,
                connection_name="another connection",
                description="connection description",
                storage_account="storage account name",
                storage_account_key="storage account key",
                container="another container_name",
                prefix="source/folder",
            )
        ])

        create_target_azure_storage_connection_mock.assert_called_once_with(
            project_id=1234,
            connection_name="target connection",
            description="connection description",
            storage_account="storage account name",
            storage_account_key="storage account key",
            container="container_name",
            prefix="destination/folder",
        )
