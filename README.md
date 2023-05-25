# Label Studio API Wrapper
Helper package for configuring and Label Studio with the use of its API.

## Installation
```bash
pip install poetry
poetry install
```

## Usage
You can use the package as a CLI tool or as a Python package.
In any case, you can create a configuration file in yaml format to store your credentials and other settings.
For example:
```yaml
label-studio:
  host: localhost
  port: 8080
  api-token: api-token-as-it-appears-in-label-studio
  project-id: 1

connections:
  source:
    - name: Test source connection
      description: Connection from library
      azure-storage:
        account-name: account-name-as-it-appears-on-azure
        account-key: account-key-as-appears-on-azure
        container: documents
        prefix: path/to/images
  target:
    - name: Test target connection
      description: Target connection from library
      azure-storage:
        account-name: account-name-as-it-appears-on-azure
        account-key: account-key-as-appears-on-azure
        container: documents
        prefix: path/to/image/annotations
```

Then you can use it like this:
```bash
create-connections azure_storage_configuration.yaml
```
