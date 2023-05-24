from unittest import TestCase, mock
from unittest.mock import patch, call

from src.label_studio_api import LabelStudioApi
from src.label_studio_instance import LabelStudioInstance


class StorageConnectionsTests(TestCase):
    @patch("requests.post")
    def test_create_source_storage_connection(self, post_mock):
        # Given
        label_studio_instance = LabelStudioInstance(
            host="label_studio_host",
            port="label_studio_port",
            api_token="label_studio_api_token",
        )
        # When
        label_studio_instance.create_source_azure_storage_connection(
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
        label_studio_instance = LabelStudioInstance(
            host="label_studio_host",
            port="label_studio_port",
            api_token="label_studio_api_token",
        )
        # When
        label_studio_instance.create_target_azure_storage_connection(
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

    # @patch.object(LabelStudioInstance, "create_target_azure_storage_connection")
    # @patch.object(LabelStudioInstance, "create_source_azure_storage_connection")
    @patch("src.label_studio_api.LabelStudioInstance", autospec=True)
    def test_create_storage_connections_from_configuration_file(
            self,
            LabelStudioInstanceMock,
    ):
        # Given
        label_studio_instance = mock.MagicMock()
        LabelStudioInstanceMock.return_value = label_studio_instance
        # When
        LabelStudioApi.create_azure_storage_connections_from_configuration_file(
            configuration_file="test/helpers/azure_storage_configuration_mock.yaml"
        )
        # Then
        LabelStudioInstanceMock.assert_called_once_with("localhost", 8080, "api token")
        self.assertEqual(label_studio_instance.create_source_azure_storage_connection.call_count, 2)
        label_studio_instance.create_source_azure_storage_connection.assert_has_calls([
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

        label_studio_instance.create_target_azure_storage_connection.assert_called_once_with(
            project_id=1234,
            connection_name="target connection",
            description="connection description",
            storage_account="storage account name",
            storage_account_key="storage account key",
            container="container_name",
            prefix="destination/folder",
        )
