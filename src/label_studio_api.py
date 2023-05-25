from pathlib import Path

import yaml

from src.label_studio_instance import LabelStudioInstance


class LabelStudioApi:
    @classmethod
    def create_azure_storage_connections_from_configuration_file(cls, configuration_file):
        with Path(configuration_file).open("r") as file:
            configuration = yaml.load(file, Loader=yaml.FullLoader)

        project_id = configuration["label-studio"]["project-id"]
        host = configuration["label-studio"]["host"]
        port = configuration["label-studio"]["port"]
        api_token = configuration["label-studio"]["api-token"]

        label_studio_instance = LabelStudioInstance(host, port, api_token)

        for connection in configuration["connections"]["source"]:
            label_studio_instance.create_source_azure_storage_connection(
                project_id=project_id,
                connection_name=connection["name"],
                description=connection["description"],
                storage_account=connection["azure-storage"]["account-name"],
                storage_account_key=connection["azure-storage"]["account-key"],
                container=connection["azure-storage"]["container"],
                prefix=connection["azure-storage"]["prefix"],
            )

        for connection in configuration["connections"]["target"]:
            label_studio_instance.create_target_azure_storage_connection(
                project_id=project_id,
                connection_name=connection["name"],
                description=connection["description"],
                storage_account=connection["azure-storage"]["account-name"],
                storage_account_key=connection["azure-storage"]["account-key"],
                container=connection["azure-storage"]["container"],
                prefix=connection["azure-storage"]["prefix"],
            )
