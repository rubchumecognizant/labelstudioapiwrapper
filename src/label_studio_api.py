from pathlib import Path
import requests

import yaml


class LabelStudioApi:
    def __init__(self, host, port, api_token):
        self.host = host
        self.port = port
        self.api_token = api_token

    def create_source_azure_storage_connection(
            self,
            project_id,
            connection_name,
            storage_account,
            storage_account_key,
            container,
            **payload_parameters
    ):
        return requests.post(
            url=f"http://{self.host}:{self.port}/api/storages/azure",
            headers={
                "Authorization": f"Token {self.api_token}",
                "Content-Type": "application/json",
            },
            json={
                "project": project_id,
                "title": connection_name,
                "account_name": storage_account,
                "account_key": storage_account_key,
                "container": container,
                "use_blob_urls": True,
                "presign_ttl": 0,
                **payload_parameters
            }
        )

    def create_target_azure_storage_connection(
            self,
            project_id,
            connection_name,
            storage_account,
            storage_account_key,
            container,
            **payload_parameters
    ):
        return requests.post(
            url=f"http://{self.host}:{self.port}/api/storages/export/azure",
            headers={
                "Authorization": f"Token {self.api_token}",
                "Content-Type": "application/json",
            },
            json={
                "project": project_id,
                "title": connection_name,
                "account_name": storage_account,
                "account_key": storage_account_key,
                "container": container,
                "use_blob_urls": True,
                **payload_parameters
            }
        )

    @classmethod
    def create_azure_storage_connections_from_configuration_file(cls, configuration_file):
        with Path(configuration_file).open("r") as file:
            configuration = yaml.load(file, Loader=yaml.FullLoader)

        project_id = configuration["label-studio"]["project-id"]
        host = configuration["label-studio"]["host"]
        port = configuration["label-studio"]["port"]
        api_token = configuration["label-studio"]["api-token"]

        label_studio_api = cls(host, port, api_token)

        for connection in configuration["connections"]["source"]:
            label_studio_api.create_source_azure_storage_connection(
                project_id=project_id,
                connection_name=connection["name"],
                description=connection["description"],
                storage_account=connection["azure-storage"]["account-name"],
                storage_account_key=connection["azure-storage"]["account-key"],
                container=connection["azure-storage"]["container"],
                prefix=connection["azure-storage"]["prefix"],
            )

        for connection in configuration["connections"]["target"]:
            label_studio_api.create_target_azure_storage_connection(
                project_id=project_id,
                connection_name=connection["name"],
                description=connection["description"],
                storage_account=connection["azure-storage"]["account-name"],
                storage_account_key=connection["azure-storage"]["account-key"],
                container=connection["azure-storage"]["container"],
                prefix=connection["azure-storage"]["prefix"],
            )
