import requests


class LabelStudioInstance:
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
